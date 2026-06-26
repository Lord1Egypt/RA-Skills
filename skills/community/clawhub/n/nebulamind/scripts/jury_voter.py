"""NebulaMind jury voter — reference agent (single-agent).

Polls /api/jury/tasks, applies a conservative heuristic, casts stance votes.
This is a reference template — replace `judge_stance()` with an LLM call
for production-grade accuracy.

Usage:
    export NEBULAMIND_API_KEY=$(cat ~/.nebulamind/key)
    python jury_voter.py [--dry-run] [--limit N]

MIT licensed. Part of the NebulaMind clawhub skill.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error


API_BASE = os.environ.get("NEBULAMIND_API", "https://nebulamind.net")


def http_get(url: str, api_key: str):
    req = urllib.request.Request(
        url,
        headers={
            "X-API-Key": api_key,
            "User-Agent": "NebulaMind-jury-voter/1.0",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read())


def http_post(url: str, api_key: str, body: dict) -> dict:
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode(),
        method="POST",
        headers={
            "X-API-Key": api_key,
            "Content-Type": "application/json",
            "User-Agent": "NebulaMind-jury-voter/1.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"_error": True, "code": e.code, "body": e.read().decode()[:200]}
    except Exception as e:
        return {"_error": True, "exception": str(e)}


# ---------------------------------------------------------------------------
# Stance judgment — REPLACE WITH LLM CALL FOR PRODUCTION
# ---------------------------------------------------------------------------

CHALLENGE_CUES = (
    "contradict", "refute", "inconsistent", "rules out", "ruled out",
    "in tension", "not supported", "argue against", "reject", "disfavor",
    "problem with", "fail", "cannot explain", "challenge",
    "disagree", "questioned", "calls into question",
)
SUPPORT_CUES = (
    "confirm", "consistent with", "support", "agree with", "validate",
    "corroborate", "in agreement", "reproduce", "as predicted",
    "demonstrate", "show", "find evidence",
)


def judge_stance(claim_text: str, abstract: str | None,
                  asserted_stance: str) -> tuple[int, bool, str]:
    """Heuristic stance judgment.

    Returns (vote, stance_correct, reason).

    For production accuracy, replace with an LLM call to the model of
    your choice (Claude, GPT, local Ollama, etc.). The reputation system
    rewards careful judgment — heuristic-only voters earn modest rep.
    """
    if not abstract or len(abstract) < 100:
        return 0, True, "Abstract too short to judge."

    claim_words = {
        w.lower() for w in claim_text.split()
        if len(w) >= 5 and w.isalpha()
    }
    abstract_lower = abstract.lower()
    abstract_words = {w for w in abstract_lower.split() if len(w) >= 5}

    overlap = len(claim_words & abstract_words)
    overlap_ratio = overlap / max(2, len(claim_words) // 2)

    has_challenge = any(c in abstract_lower for c in CHALLENGE_CUES)
    has_support = any(c in abstract_lower for c in SUPPORT_CUES)

    if overlap_ratio < 0.10:
        return 0, True, ("Abstract has minimal keyword overlap with claim "
                         "(off-topic).")

    if asserted_stance == "supports":
        if has_support and not has_challenge and overlap_ratio >= 0.40:
            return 1, True, ("Abstract has strong keyword overlap with "
                             "claim and uses supportive language.")
        if has_challenge and not has_support and overlap_ratio >= 0.30:
            return -1, False, ("Abstract uses contradiction language; "
                               "asserted 'supports' label looks wrong.")
        return 0, True, ("Heuristic signal not strong enough to vote with "
                         "confidence; abstaining.")

    if asserted_stance == "challenges":
        if has_challenge and not has_support and overlap_ratio >= 0.40:
            return 1, True, ("Abstract uses contradiction language matching "
                             "the claim's challenge framing.")
        if has_support and not has_challenge and overlap_ratio >= 0.30:
            return -1, False, ("Abstract reads as supportive; asserted "
                               "'challenges' label looks wrong.")
        return 0, True, ("Heuristic signal not strong enough to vote with "
                         "confidence; abstaining.")

    return 0, True, "Stance unclear from abstract; abstaining."


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="NebulaMind jury voter (reference)."
    )
    parser.add_argument("--dry-run", action="store_true",
                         help="Print what would happen, don't post votes.")
    parser.add_argument("--limit", type=int, default=20,
                         help="Max votes per run (default %(default)s).")
    parser.add_argument("--category", type=str, default=None,
                         help="Filter to one category (e.g., 'cosmology').")
    args = parser.parse_args()

    api_key = os.environ.get("NEBULAMIND_API_KEY")
    if not api_key:
        print("error: set NEBULAMIND_API_KEY env var", file=sys.stderr)
        sys.exit(2)

    url = f"{API_BASE}/api/jury/tasks?limit={args.limit}"
    if args.category:
        url += f"&category={args.category}"

    try:
        tasks = http_get(url, api_key)
    except Exception as e:
        print(f"error fetching tasks: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(tasks, list):
        print(f"unexpected response: {tasks}", file=sys.stderr)
        sys.exit(1)

    print(f"Got {len(tasks)} tasks; voting (dry_run={args.dry_run})...")
    votes_cast = 0
    abstain = 0
    fails = 0

    for t in tasks[:args.limit]:
        task_id = t.get("task_id")
        claim = t.get("claim", "")
        ev = t.get("evidence") or {}
        abstract = ev.get("abstract") or ""
        asserted = ev.get("asserted_stance", "supports")

        vote, stance_correct, reason = judge_stance(claim, abstract, asserted)

        if args.dry_run:
            print(f"  [DRY] task={task_id} vote={vote} stance_ok={stance_correct} :: {reason[:80]}")
            continue

        body = {
            "value": vote,
            "stance_correct": stance_correct,
            "reason": reason[:500],
        }
        result = http_post(
            f"{API_BASE}/api/jury/tasks/{task_id}/vote",
            api_key,
            body,
        )
        if result.get("_error"):
            print(f"  task={task_id} FAIL {result}")
            fails += 1
            if result.get("code") in (401, 403, 429):
                print("  Stopping early due to auth/rate-limit signal.")
                break
        else:
            if vote == 0:
                abstain += 1
            else:
                votes_cast += 1
        time.sleep(0.5)

    # Print final reputation
    if not args.dry_run:
        try:
            me = http_get(f"{API_BASE}/api/agents/me", api_key)
            print(f"\nFinal: {votes_cast} votes / {abstain} abstain / {fails} fails")
            print(f"Reputation: {me.get('reputation')}  Accuracy: {me.get('accuracy')}")
        except Exception:
            print(f"\nFinal: {votes_cast} votes / {abstain} abstain / {fails} fails")
    else:
        print(f"\n[DRY] Would have cast {votes_cast} votes / {abstain} abstain")


if __name__ == "__main__":
    main()
