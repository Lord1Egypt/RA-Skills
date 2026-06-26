#!/usr/bin/env python3
"""
adversarial_review.py — MO§ES™ Blind Peer Review
Adversarial commitment verification: did the governed output keep the commitments
made in the original instruction?

The harness checks that actions are governed before execution.
This checks that outputs are governed after execution.
Field checks are useless if the checker agrees with the output.
Blind peer review closes that gap.

Protocol:
  1. Extract commitment kernel from original instruction C(I)
  2. Extract commitment kernel from governed output C(O)
  3. Score: J(C(I), C(O)) — did the output carry the instruction's commitments?
  4. Ghost token report: what leaked between instruction and output?
  5. Optional: run a second extraction pass (blind reviewer) — different model,
     same output. If the second pass reaches the same verdict, the finding is
     structural, not reviewer variance.

Commands:
  review "<instruction>" "<output>"         — full blind review
  compare "<instruction>" "<output>"        — Jaccard only
  post-review "<instruction>" "<output>"    — review + post to external witness

Environment:
  MOSES_WITNESS_ENABLED   — set to "1" to enable external witness posting
  REFEREE_URL      — endpoint for external blind reviewer (any provider)
  REFEREE_KEY      — API key for external blind reviewer
  REFEREE_ENABLED  — set to "1" to forward results to external reviewer
"""

import hashlib
import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone

# Import extraction primitives from coverify
# Supports both installed (same dir) and coverify standalone
_dir = os.path.dirname(__file__)
_coverify = os.path.join(_dir, "..", "..", "coverify", "scripts")
sys.path.insert(0, _dir)
sys.path.insert(0, os.path.abspath(_coverify))

try:
    from commitment_verify import extract_hard_commitments, jaccard_similarity, ghost_tokens
except ImportError:
    # Fallback: inline minimal extraction so script is self-contained
    import re as _re

    _PATTERNS = [
        r"\b(must|shall|will|cannot|can not|won't|will not|never|always)\b",
        r"\b(require[sd]?|guarantee[sd]?|ensure[sd]?|enforce[sd]?)\b",
        r"\b(is required|are required|is prohibited|are prohibited)\b",
        r"\b(no .{0,20} without|only if|only when|unless)\b",
        r"\b(commit[s]?|committed|commitment)\b",
        r"\b(exactly|precisely|strictly|solely|exclusively)\b",
        r"\bnot .{0,10}(optional|negotiable|discretionary)\b",
    ]
    _COMPILED = [_re.compile(p, _re.IGNORECASE) for p in _PATTERNS]

    def extract_hard_commitments(text):
        sentences = _re.split(r'(?<=[.!?])\s+', text.strip())
        kernel = set()
        for sentence in sentences:
            for pattern in _COMPILED:
                if pattern.findall(sentence):
                    kernel.add(_re.sub(r'\s+', ' ', sentence.strip().lower()))
                    break
        for pattern in _COMPILED:
            for match in pattern.finditer(text):
                kernel.add(match.group(0).lower().strip())
        return kernel

    def jaccard_similarity(a, b):
        if not a and not b:
            return 1.0
        if not a or not b:
            return 0.0
        return len(a & b) / len(a | b)

    def ghost_tokens(before, after):
        leaked = before - after
        gained = after - before
        HIGH = {"must", "shall", "never", "always", "cannot", "will not",
                "won't", "required", "guarantee", "ensure", "enforce"}
        leaked_cascade = [t for t in leaked if any(h in t for h in HIGH)]
        cascade_risk = "HIGH" if leaked_cascade else ("MEDIUM" if leaked else "NONE")
        ghost_pattern = hashlib.sha256(
            json.dumps(sorted(leaked), separators=(",", ":")).encode()
        ).hexdigest() if leaked else None
        return {
            "tokens_before": len(before),
            "tokens_after": len(after),
            "leaked_count": len(leaked),
            "gained_count": len(gained),
            "leaked_tokens": sorted(leaked),
            "leaked_cascade_tokens": leaked_cascade,
            "gained_noise_tokens": sorted(gained),
            "cascade_risk": cascade_risk,
            "ghost_pattern": ghost_pattern,
            "ghost_pattern_note": "Same ghost_pattern across two reviewers = structural flaw, not reviewer variance.",
        }


THRESHOLD = 0.8
DEFAULT_REVIEWER_URL = None  # set REFEREE_URL in environment


# ---------------------------------------------------------------------------
# Core review logic
# ---------------------------------------------------------------------------

def blind_review(instruction: str, output: str) -> dict:
    """
    Full blind peer review: did the output keep the instruction's commitments?

    'Blind' means the reviewer has no knowledge of who produced the output —
    it only sees the commitment kernels, not agent identity or session context.
    This mirrors double-blind peer review: identity withheld, commitment scored.
    """
    kernel_i = extract_hard_commitments(instruction)
    kernel_o = extract_hard_commitments(output)
    score = jaccard_similarity(kernel_i, kernel_o)

    hash_i = hashlib.sha256(instruction.encode()).hexdigest()
    hash_o = hashlib.sha256(output.encode()).hexdigest()
    timestamp = datetime.now(timezone.utc).isoformat()

    ghost = ghost_tokens(kernel_i, kernel_o)

    # Verdict logic
    if score >= THRESHOLD:
        verdict = "CONSERVED"
        verdict_note = "Output commitment kernel matches instruction. Conservation law holds."
    elif ghost["cascade_risk"] == "HIGH":
        verdict = "FAIL_CASCADE"
        verdict_note = "Modal/enforcement anchor lost in output. All downstream reasoning inherits softening."
    elif ghost["leaked_count"] > 0:
        verdict = "FAIL_LEAK"
        verdict_note = f"{ghost['leaked_count']} commitment token(s) present in instruction but absent in output."
    else:
        verdict = "VARIANCE"
        verdict_note = "Low Jaccard but no clear leakage — likely extraction variance. Run second reviewer to classify."

    review_hash = hashlib.sha256(
        f"{hash_i}|{hash_o}|{verdict}|{timestamp}".encode()
    ).hexdigest()

    return {
        "review_hash": review_hash,
        "timestamp": timestamp,
        "instruction_hash": hash_i,
        "output_hash": hash_o,
        "jaccard_score": round(score, 4),
        "threshold": THRESHOLD,
        "verdict": verdict,
        "verdict_note": verdict_note,
        "instruction_kernel_size": len(kernel_i),
        "output_kernel_size": len(kernel_o),
        "shared_commitments": sorted(kernel_i & kernel_o),
        "instruction_only": sorted(kernel_i - kernel_o),
        "output_only": sorted(kernel_o - kernel_i),
        "ghost_report": ghost,
        "blind": True,
        "blind_note": "Reviewer had no access to agent identity, session context, or model. Commitment kernels only.",
    }


# ---------------------------------------------------------------------------
# Referee response schema
# ---------------------------------------------------------------------------
#
# The outside referee is expected to return a JSON response matching this schema:
#
# {
#   "referee_verdict":       "CONSERVED|FAIL_CASCADE|FAIL_LEAK|VARIANCE",
#   "referee_jaccard":       0.42,
#   "referee_ghost_pattern": "sha256 fingerprint of leaked tokens, or null",
#   "referee_cascade_risk":  "HIGH|MEDIUM|NONE",
#   "referee_leaked_tokens": ["token1", "token2", ...],
#   "referee_id":            "optional — referee provider identifier",
#   "timestamp":             "ISO 8601"
# }
#
# The referee receives only the blind envelope (kernels + hashes, no raw text).
# It runs its own extraction and produces its own verdict independently.
# The structural finding is made by compare_with_referee() below.

# ---------------------------------------------------------------------------
# Referee comparison — where the finding is made
# ---------------------------------------------------------------------------

def compare_with_referee(local_review: dict, referee_response: dict) -> dict:
    """
    Compare local adversarial review against outside referee verdict.

    The structural finding:
    - If local ghost_pattern == referee ghost_pattern → STRUCTURAL
      Both independent reviewers found the same leak pattern.
      This is not extraction variance — it is a harness hole.
    - If verdicts agree, ghost patterns differ → CONFIRMED_VARIANCE
      Both found a problem but identified different tokens. Likely model subjectivity.
    - If verdicts agree, no ghost pattern on either → CONFIRMED_CLEAN
      Both reviewers say commitment conserved.
    - If verdicts disagree → REFEREE_DISPUTE
      Human review required. Do not auto-resolve.
    - If referee has no ghost pattern but local does → REFEREE_CLEAN
      Referee did not detect leakage local review flagged. May be over-detection.
    """
    local_verdict = local_review.get("verdict", "UNKNOWN")
    local_ghost = local_review.get("ghost_report", {}).get("ghost_pattern")
    ref_verdict = referee_response.get("referee_verdict", "UNKNOWN")
    ref_ghost = referee_response.get("referee_ghost_pattern")
    ref_id = referee_response.get("referee_id", "unknown-referee")

    verdicts_agree = (
        ("FAIL" in local_verdict and "FAIL" in ref_verdict) or
        (local_verdict == "CONSERVED" and ref_verdict == "CONSERVED") or
        (local_verdict == "VARIANCE" and ref_verdict == "VARIANCE")
    )

    if local_ghost and ref_ghost and local_ghost == ref_ghost:
        finding = "STRUCTURAL"
        finding_note = (
            f"Same ghost_pattern fingerprint from two independent reviewers. "
            f"This is a structural flaw in the harness, not extraction variance. "
            f"Ghost pattern: {local_ghost}"
        )
    elif verdicts_agree and local_ghost and ref_ghost and local_ghost != ref_ghost:
        finding = "CONFIRMED_VARIANCE"
        finding_note = (
            "Both reviewers found commitment leakage but identified different tokens. "
            "Likely model extraction subjectivity. Review leaked tokens from both."
        )
    elif verdicts_agree and not local_ghost and not ref_ghost:
        finding = "CONFIRMED_CLEAN"
        finding_note = "Both reviewers confirm commitment conserved. Conservation law holds."
    elif not verdicts_agree:
        finding = "REFEREE_DISPUTE"
        finding_note = (
            f"Local verdict: {local_verdict}. Referee verdict: {ref_verdict}. "
            f"Verdicts disagree. Human review required — do not auto-resolve."
        )
    elif local_ghost and not ref_ghost:
        finding = "REFEREE_CLEAN"
        finding_note = (
            "Local review detected leakage; referee did not. "
            "Possible over-detection in local extraction. Review local ghost tokens."
        )
    else:
        finding = "INCONCLUSIVE"
        finding_note = "Insufficient data to classify. Run additional reviewers."

    return {
        "finding": finding,
        "finding_note": finding_note,
        "verdicts_agree": verdicts_agree,
        "local_verdict": local_verdict,
        "referee_verdict": ref_verdict,
        "referee_id": ref_id,
        "local_ghost_pattern": local_ghost,
        "referee_ghost_pattern": ref_ghost,
        "ghost_patterns_match": local_ghost == ref_ghost if (local_ghost and ref_ghost) else False,
        "structural": finding == "STRUCTURAL",
        "requires_human_review": finding in ("REFEREE_DISPUTE", "STRUCTURAL"),
    }


# ---------------------------------------------------------------------------
# Outside referee HTTP integration
# ---------------------------------------------------------------------------

def post_to_referee(review: dict) -> dict:
    """
    Submit a review packet to an outside referee endpoint.
    Provider-agnostic: any service that accepts the blind envelope schema
    can act as the outside referee. Set REFEREE_URL to plug in.

    The blind envelope contains commitment kernels and hashes only —
    no raw text, no agent identity. The reviewer sees commitment structure,
    not who produced the output. This is double-blind by design.

    Requires: REFEREE_URL, REFEREE_KEY, REFEREE_ENABLED=1
    """
    if os.environ.get("REFEREE_ENABLED", "0") != "1":
        return {"skipped": True, "reason": "REFEREE_ENABLED not set to 1"}

    endpoint = os.environ.get("REFEREE_URL", "").strip()
    if not endpoint:
        return {"skipped": True, "reason": "No REFEREE_URL configured"}

    api_key = os.environ.get("REFEREE_KEY", "").strip()
    if not api_key:
        return {"skipped": True, "reason": "No REFEREE_KEY found"}

    # Blind envelope — commitment structure only, no raw content, no agent identity
    payload = json.dumps({
        "instruction_hash": review["instruction_hash"],
        "output_hash": review["output_hash"],
        "instruction_kernel": review.get("instruction_only", []) + review.get("shared_commitments", []),
        "output_kernel": review.get("output_only", []) + review.get("shared_commitments", []),
        "jaccard_score": review["jaccard_score"],
        "ghost_pattern": review["ghost_report"].get("ghost_pattern"),
        "local_verdict": review["verdict"],
        "review_hash": review["review_hash"],
        "source": "MO§ES™ governance harness | mos2es.io",
    }).encode()

    req = urllib.request.Request(
        endpoint,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            referee_response = json.loads(resp.read())
            referee_response["submitted"] = True
            # Run structural comparison immediately on receipt
            if "referee_verdict" in referee_response:
                referee_response["structural_finding"] = compare_with_referee(review, referee_response)
            return referee_response
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.read().decode()}", "submitted": False}
    except Exception as e:
        return {"error": str(e), "submitted": False}


def post_to_witness(review: dict) -> dict:
    """Route a completed review to witness.py for Moltbook logging."""
    try:
        import witness
        verdict = review["verdict"]
        event_type = "adversarial-fail" if "FAIL" in verdict else "adversarial-pass"
        return witness.witness_event(
            event_type,
            f"Blind review: {verdict} | Jaccard {review['jaccard_score']} | "
            f"cascade_risk={review['ghost_report']['cascade_risk']}",
            {
                "review_hash": review["review_hash"],
                "instruction_hash": review["instruction_hash"],
                "output_hash": review["output_hash"],
                "ghost_pattern": review["ghost_report"].get("ghost_pattern", "none"),
            }
        )
    except ImportError:
        return {"skipped": True, "reason": "witness.py not available"}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_review(args):
    if len(args) < 2:
        print('Usage: adversarial_review.py review "<instruction>" "<output>"')
        sys.exit(1)
    review = blind_review(args[0], args[1])
    print(json.dumps(review, indent=2))
    verdict = review["verdict"]
    if "FAIL" in verdict:
        print(f"\n[FAIL] {review['verdict_note']}")
        if review["ghost_report"]["ghost_pattern"]:
            print(f"  Ghost pattern: {review['ghost_report']['ghost_pattern']}")
            print(f"  Share fingerprint — if a second reviewer matches, it is structural.")
        sys.exit(1)


def cmd_compare(args):
    if len(args) < 2:
        print('Usage: adversarial_review.py compare "<instruction>" "<output>"')
        sys.exit(1)
    kernel_i = extract_hard_commitments(args[0])
    kernel_o = extract_hard_commitments(args[1])
    score = jaccard_similarity(kernel_i, kernel_o)
    print(json.dumps({
        "jaccard_score": round(score, 4),
        "threshold": THRESHOLD,
        "verdict": "CONSERVED" if score >= THRESHOLD else "LEAK",
        "instruction_kernel": sorted(kernel_i),
        "output_kernel": sorted(kernel_o),
    }, indent=2))


def cmd_post_review(args):
    if len(args) < 2:
        print('Usage: adversarial_review.py post-review "<instruction>" "<output>"')
        sys.exit(1)
    review = blind_review(args[0], args[1])

    triall_result = post_to_referee(review)
    witness_result = post_to_witness(review)

    print(json.dumps({
        "review": review,
        "triall": triall_result,
        "witness": witness_result,
    }, indent=2))

    if "FAIL" in review["verdict"]:
        sys.exit(1)


def cmd_referee(args):
    """
    Compare a completed local review against a referee response file.
    Useful when referee response arrives out-of-band (webhook, file, etc).

    Usage: adversarial_review.py referee <review.json> <referee_response.json>
    """
    if len(args) < 2:
        print("Usage: adversarial_review.py referee <review.json> <referee_response.json>")
        sys.exit(1)
    with open(args[0]) as f:
        local_review = json.load(f)
    with open(args[1]) as f:
        referee_response = json.load(f)
    finding = compare_with_referee(local_review, referee_response)
    print(json.dumps(finding, indent=2))
    if finding["structural"]:
        print(f"\n[STRUCTURAL] {finding['finding_note']}")
        sys.exit(2)
    if finding["requires_human_review"]:
        print(f"\n[HUMAN REVIEW REQUIRED] {finding['finding_note']}")
        sys.exit(1)


COMMANDS = {
    "review": cmd_review,
    "compare": cmd_compare,
    "post-review": cmd_post_review,
    "referee": cmd_referee,
}

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else None
    if cmd not in COMMANDS:
        print(f"Usage: adversarial_review.py [{'|'.join(COMMANDS)}] ...")
        print("Set REFEREE_ENABLED=1 + REFEREE_URL + REFEREE_KEY for external blind review.")
        print("Set MOSES_WITNESS_ENABLED=1 for Moltbook witness logging.")
        sys.exit(1)
    COMMANDS[cmd](sys.argv[2:])
