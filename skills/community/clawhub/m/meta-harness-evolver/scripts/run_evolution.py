#!/usr/bin/env python3
"""
Meta-Harness Evolution Loop — Main Entry Point

Runs the full Meta-Harness outer loop for Hoss:
  1. Read prior candidates from ~/hoss-evolution/candidates/
  2. Spawn proposer sub-agent to propose a new harness
  3. Validate the proposed candidate
  4. Evaluate against benchmark
  5. Log results
  6. Post summary to Discord

Usage:
  python3 run_evolution.py [--candidate-num N]

Exit codes:
  0 = success (candidate evaluated)
  1 = skipped (no valid candidate produced)
  2 = error
"""

import argparse
import json
import os
import subprocess
import sys
import textwrap
import time
from datetime import datetime
from pathlib import Path

WORKSPACE = Path.home() / "hoss-evolution"
CANDIDATES_DIR = WORKSPACE / "candidates"
BEST_DIR = WORKSPACE / "best" / "current"
SCRIPTS_DIR = Path(__file__).parent


def get_next_candidate_num() -> int:
    """Find the next candidate number."""
    if not CANDIDATES_DIR.exists():
        CANDIDATES_DIR.mkdir(parents=True, exist_ok=True)
        return 1
    existing = [int(d.name.split("_")[1]) for d in CANDIDATES_DIR.iterdir()
                if d.is_dir() and d.name.startswith("candidate_")]
    return max(existing, default=0) + 1


def get_best_candidate() -> dict | None:
    """Get the best candidate's scores."""
    scores_file = BEST_DIR / "eval_scores.json"
    if scores_file.exists():
        return json.loads(scores_file.read_text())
    return None


def run_proposer(candidate_num: int) -> dict:
    """
    Spawn the proposer sub-agent to propose a harness modification.
    Returns dict with 'success', 'candidate_dir', and 'reasoning'.
    """
    import uuid

    candidate_dir = CANDIDATES_DIR / f"candidate_{candidate_num}"
    candidate_dir.mkdir(parents=True, exist_ok=True)
    (candidate_dir / "harness").mkdir(exist_ok=True)
    (candidate_dir / "traces").mkdir(exist_ok=True)

    # Read evolution history for context
    history = []
    for d in sorted(CANDIDATES_DIR.iterdir(), key=lambda x: x.name):
        if d.name == f"candidate_{candidate_num}":
            continue
        if d.is_dir():
            scores_file = d / "eval_scores.json"
            if scores_file.exists():
                history.append({
                    "candidate": d.name,
                    "scores": json.loads(scores_file.read_text())
                })

    best = get_best_candidate()

    # Spawn the sub-agent
    agent_session_id = str(uuid.uuid4())[:8]

    proposer_task = f"""You are the Meta-Harness Proposer for Hoss (OpenClaw agent).

Your job: Propose ONE targeted harness modification based on evolution history.

## Your Workspace
- Evolution history: ~/hoss-evolution/candidates/
- Current best harness: ~/hoss-evolution/best/current/
- Your output: ~/hoss-evolution/candidates/candidate_{candidate_num}/harness/

## What You Must Do

1. Read ALL prior candidates from ~/hoss-evolution/candidates/ (sorted by number)
2. Read the current best from ~/hoss-evolution/best/current/
3. Identify patterns: what's working? What's failing?
4. Propose ONE targeted, specific edit to ONE of these files:
   - SOUL.md (core identity/personality)
   - IDENTITY.md (role, voice, tone)
   - AGENTS.md (sub-agent coordination)
   - TOOLS.md (tool configs — DO NOT change credentials/secrets)
   - HEARTBEAT.md (check priorities/thresholds)
   - MEMORY.md (memory structure — rarely change this)

5. Copy the current best harness files to your output dir
6. Apply your targeted edit to the ONE file you chose
7. Write a BRIEF reasoning trace to ~/hoss-evolution/candidates/candidate_{candidate_num}/proposer_reasoning.md
   explaining: what you changed, why, what you expect to improve

## Constraints
- Do NOT do wholesale rewrites — one targeted edit max
- Do NOT change git safety rules or credential values
- Do NOT touch files outside the harness spec
- If you see no clear improvement path, write your reasoning and make ONE small edit anyway

## History Summary
Total prior candidates: {len(history)}
Best score so far: {best['final_score'] if best else 'N/A'}

## Output Format
Write your modified file to ~/hoss-evolution/candidates/candidate_{candidate_num}/harness/<FILENAME>
Write reasoning to ~/hoss-evolution/candidates/candidate_{candidate_num}/proposer_reasoning.md

Start now. Read the history first, then propose.
"""

    print(f"[PROPOSER] Spawning sub-agent for candidate_{candidate_num}...")
    print(f"[PROPOSER] History: {len(history)} prior candidates")

    try:
        from openclaw.sessions import sessions_spawn
        result = sessions_spawn(
            task=proposer_task,
            label=f"harness-proposer-{agent_session_id}",
            runtime="subagent",
            mode="run",
            run_timeout_seconds=300,
        )
        print(f"[PROPOSER] Sub-agent returned: {result}")
        return {"success": True, "candidate_dir": str(candidate_dir), "agent_result": result}
    except Exception as e:
        print(f"[PROPOSER] Error spawning sub-agent: {e}")
        # Fall back: copy current best as a no-op candidate
        return {"success": False, "candidate_dir": str(candidate_dir), "error": str(e)}


def validate_candidate(candidate_dir: Path) -> bool:
    """Lightweight validation before running full benchmark."""
    print(f"[VALIDATE] Checking {candidate_dir}/harness/...")

    harness_dir = candidate_dir / "harness"
    required_files = ["SOUL.md", "IDENTITY.md", "AGENTS.md", "TOOLS.md"]
    for f in required_files:
        fp = harness_dir / f
        if not fp.exists():
            print(f"[VALIDATE] Missing required file: {f}")
            return False

    # Basic sanity checks
    for md_file in harness_dir.glob("*.md"):
        content = md_file.read_text()
        if len(content) < 50:
            print(f"[VALIDATE] WARNING: {md_file.name} seems too short ({len(content)} chars)")

    print("[VALIDATE] OK")
    return True


def evaluate_candidate(candidate_dir: Path) -> dict:
    """Run the benchmark against the candidate harness."""
    print(f"[EVALUATE] Running benchmark for {candidate_dir.name}...")
    eval_script = SCRIPTS_DIR / "evaluate.py"

    result = subprocess.run(
        [sys.executable, str(eval_script), str(candidate_dir)],
        capture_output=True,
        text=True,
        timeout=600,
    )

    if result.returncode != 0:
        print(f"[EVALUATE] Error: {result.stderr}")
        return {"error": result.stderr, "scores": {}}

    try:
        scores = json.loads(result.stdout.strip().split("\n")[-1])
        return scores
    except Exception as e:
        print(f"[EVALUATE] Failed to parse scores: {e}")
        return {"error": str(e), "scores": {}}


def update_best(candidate_dir: Path, scores: dict):
    """Update the best harness if this candidate is better."""
    best_scores_file = BEST_DIR / "eval_scores.json"
    best_harness_dir = BEST_DIR / "harness"

    current_best = None
    if best_scores_file.exists():
        current_best = json.loads(best_scores_file.read_text())["final_score"]

    new_score = scores.get("final_score", 0)

    if current_best is None or new_score > current_best:
        print(f"[BEST] New best! {new_score} > {current_best}")
        # Copy candidate harness to best
        BEST_DIR.mkdir(parents=True, exist_ok=True)
        best_harness_dir.mkdir(parents=True, exist_ok=True)

        import shutil
        candidate_harness = candidate_dir / "harness"
        for f in candidate_harness.iterdir():
            shutil.copy2(f, best_harness_dir / f.name)

        # Copy scores
        with open(best_scores_file, "w") as sf:
            json.dump(scores, sf, indent=2)

        # Note the winner
        with open(BEST_DIR / "winner_note.md", "w") as wn:
            wn.write(f"# Best Harness — {datetime.now().isoformat()}\n\n")
            wn.write(f"Winner: {candidate_dir.name}\n")
            wn.write(f"Score: {new_score}\n")
            wn.write(f"Improvement over previous: {new_score - (current_best or 0):+.2f}\n")
    else:
        print(f"[BEST] No update. Current best: {current_best}, this candidate: {new_score}")


def log_evolution(candidate_num: int, candidate_dir: Path, scores: dict, proposer_ok: bool):
    """Append to the evolution log."""
    log_file = WORKSPACE / "evolution_log.jsonl"
    entry = {
        "timestamp": datetime.now().isoformat(),
        "candidate": f"candidate_{candidate_num}",
        "candidate_dir": str(candidate_dir),
        "proposer_success": proposer_ok,
        "scores": scores,
        "final_score": scores.get("final_score", 0),
    }
    with open(log_file, "a") as lf:
        lf.write(json.dumps(entry) + "\n")


def post_to_discord(candidate_num: int, candidate_dir: Path, scores: dict, proposer_ok: bool):
    """Post summary to #research Discord channel."""
    print("[DISCORD] Posting to #research...")
    post_script = SCRIPTS_DIR / "post_to_research.py"

    result = subprocess.run(
        [sys.executable, str(post_script), str(candidate_num), str(candidate_dir),
         str(scores.get("final_score", 0)), str(int(proposer_ok))],
        capture_output=True,
        text=True,
        timeout=30,
    )

    if result.returncode != 0:
        print(f"[DISCORD] Failed: {result.stderr}")
    else:
        print(f"[DISCORD] Posted successfully")


def main():
    parser = argparse.ArgumentParser(description="Meta-Harness Evolution Loop")
    parser.add_argument("--candidate-num", type=int, default=None,
                        help="Candidate number (default: auto)")
    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"Meta-Harness Evolution — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    candidate_num = args.candidate_num or get_next_candidate_num()
    print(f"[MAIN] Candidate: {candidate_num}")

    # Step 1: Run proposer
    proposer_result = run_proposer(candidate_num)
    candidate_dir = Path(proposer_result["candidate_dir"])

    if not proposer_result["success"]:
        print(f"[MAIN] Proposer failed: {proposer_result.get('error')}")
        print("[MAIN] Skipping this iteration.")
        sys.exit(1)

    # Step 2: Validate
    if not validate_candidate(candidate_dir):
        print("[MAIN] Validation failed. Skipping.")
        sys.exit(1)

    # Step 3: Evaluate
    scores = evaluate_candidate(candidate_dir)
    if not scores or "error" in scores:
        print(f"[MAIN] Evaluation failed: {scores.get('error')}")
        sys.exit(1)

    # Step 4: Log eval scores to candidate dir
    scores_file = candidate_dir / "eval_scores.json"
    with open(scores_file, "w") as sf:
        json.dump(scores, sf, indent=2)
    print(f"[MAIN] Scores: {json.dumps(scores, indent=2)}")

    # Step 5: Update best if needed
    update_best(candidate_dir, scores)

    # Step 6: Log evolution
    log_evolution(candidate_num, candidate_dir, scores, proposer_result["success"])

    # Step 7: Post to Discord
    post_to_discord(candidate_num, candidate_dir, scores, proposer_result["success"])

    print(f"\n[MAIN] Done! Candidate {candidate_num} evaluated: {scores.get('final_score')}")
    print(f"{'='*60}\n")

    sys.exit(0)


if __name__ == "__main__":
    main()
