#!/usr/bin/env python3
"""
Post evolution results to Discord #research channel.

Usage:
  python3 post_to_research.py <candidate_num> <candidate_dir> <score> <proposer_success>
"""

import sys
import json
from pathlib import Path
from datetime import datetime

WORKSPACE = Path.home() / "hoss-evolution"
DISCORD_CHANNEL_ID = "1487319587316957244"  # #research


def get_history_summary() -> str:
    """Get evolution history from log."""
    log_file = WORKSPACE / "evolution_log.jsonl"
    if not log_file.exists():
        return "No prior history."

    entries = []
    with open(log_file) as f:
        for line in f:
            try:
                entries.append(json.loads(line.strip()))
            except:
                pass

    if not entries:
        return "No prior history."

    # Show last 5 entries
    recent = entries[-5:]
    lines = []
    for e in recent:
        ts = datetime.fromisoformat(e["timestamp"]).strftime("%m-%d %H:%M")
        lines.append(f"  • {e['candidate']}: {e['final_score']}/100")

    return "\n".join(lines) if lines else "No prior history."


def get_best_score() -> float:
    """Get the current best score."""
    best_file = WORKSPACE / "best" / "current" / "eval_scores.json"
    if best_file.exists():
        return json.loads(best_file.read_text()).get("final_score", 0)
    return 0


def get_proposer_reasoning(candidate_dir: Path) -> str:
    """Read the proposer's reasoning trace."""
    reasoning_file = candidate_dir / "proposer_reasoning.md"
    if reasoning_file.exists():
        content = reasoning_file.read_text()
        # Truncate if too long
        if len(content) > 500:
            return content[:500] + "..."
        return content
    return "No reasoning trace found."


def get_change_summary(candidate_dir: Path) -> str:
    """Diff harness files vs best to show what changed."""
    best_dir = WORKSPACE / "best" / "current" / "harness"
    candidate_harness = candidate_dir / "harness"

    changes = []
    for f in candidate_harness.glob("*.md"):
        best_file = best_dir / f.name
        if not best_file.exists():
            changes.append(f"  + {f.name} (new)")
        else:
            best_content = best_file.read_text()
            cand_content = f.read_text()
            if best_content != cand_content:
                # Simple diff summary
                best_lines = len(best_content.split("\n"))
                cand_lines = len(cand_content.split("\n"))
                diff = cand_lines - best_lines
                sign = "+" if diff > 0 else ""
                changes.append(f"  ~ {f.name} ({sign}{diff} lines)")

    if not changes:
        return "  (no diff — identical to current best)"

    return "\n".join(changes[:5])  # Limit to 5 changes


def build_message(candidate_num: int, candidate_dir: Path, score: float, proposer_ok: bool) -> str:
    """Build the Discord message."""

    best_score = get_best_score()
    delta = score - best_score
    delta_str = f"+{delta:.1f}" if delta > 0 else f"{delta:.1f}"

    history = get_history_summary()
    reasoning = get_proposer_reasoning(candidate_dir)
    changes = get_change_summary(candidate_dir)

    candidate_dir = Path(candidate_dir)

    emoji = "🔺" if delta > 0 else "🔻" if delta < 0 else "➡️"
    status = "NEW BEST!" if score > best_score else "no change" if score == best_score else f"{delta_str} vs best"

    msg = f"""**⚡ Meta-Harness Evolution — Nightly Report**

**Candidate:** `candidate_{candidate_num}`
**Score:** `{score}/100` {emoji} {status}
**Proposer:** {"✅ Success" if proposer_ok else "❌ Failed"}

---

**What Changed:**
{changes}

---

**Proposer's Reasoning:**
{reasoning}

---

**Recent History:**
{history}

---

_Posted {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} CDT_"""

    return msg


def main():
    if len(sys.argv) < 5:
        print("Usage: post_to_research.py <candidate_num> <candidate_dir> <score> <proposer_success>")
        sys.exit(1)

    candidate_num = sys.argv[1]
    candidate_dir = Path(sys.argv[2])
    score = float(sys.argv[3])
    proposer_ok = bool(int(sys.argv[4]))

    message = build_message(candidate_num, candidate_dir, score, proposer_ok)

    # Use openclaw message tool via subprocess
    # In production this would use the message tool directly
    # For now we print and can be triggered via the message tool in the main session

    print("DISCORD_MESSAGE:")
    print(message)
    print("END_DISCORD_MESSAGE")

    # Actually send via openclaw
    import subprocess
    result = subprocess.run(
        ["openclaw", "message", "--channel", "discord",
         "--target", DISCORD_CHANNEL_ID, "--message", message],
        capture_output=True,
        text=True,
        timeout=30,
    )

    if result.returncode != 0:
        print(f"Failed to send Discord message: {result.stderr}")
        sys.exit(1)

    print("Posted to #research successfully")


if __name__ == "__main__":
    main()
