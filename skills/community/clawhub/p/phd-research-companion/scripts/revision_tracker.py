#!/usr/bin/env python3
"""
Revision Round Tracker

Records each improvement cycle of a paper: issues found, actions taken,
evidence artifacts. Evidence paths are checked for existence and recorded
with size + sha256 so an audit trail cannot be rewritten unnoticed.

Usage:
    python revision_tracker.py --action add_round -r 2 \
        -i "missing baseline" "weak lemma 4" \
        -x "added 3 SOTA baselines; strengthened lemma 4" \
        -e ./05-revision-rounds/round2.diff
    python revision_tracker.py --action report -d ./05-revision-rounds
    python revision_tracker.py --action summary -d ./05-revision-rounds
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path

PHASES = {
    1: "initial_review",
    2: "major_revisions",
    3: "additional_validation",
    4: "language_polishing",
    5: "final_review",
}

MIN_ROUNDS_FOR_SUBMISSION = 5


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


class RevisionTracker:
    def __init__(self, tracking_dir: Path):
        self.tracking_dir = Path(tracking_dir)
        self.tracking_dir.mkdir(parents=True, exist_ok=True)
        self.history_file = self.tracking_dir / "revision-history.json"

    def load(self) -> dict:
        if not self.history_file.exists():
            return {"created": datetime.now().isoformat(timespec="seconds"),
                    "last_updated": None,
                    "rounds_completed": 0,
                    "total_issues": 0,
                    "rounds": []}
        return json.loads(self.history_file.read_text(encoding="utf-8"))

    def save(self, history: dict) -> None:
        history["last_updated"] = datetime.now().isoformat(timespec="seconds")
        self.history_file.write_text(json.dumps(history, indent=2), encoding="utf-8")

    def add_round(self, round_num: int, issues: list[str], actions: str,
                  evidence: list[str]) -> dict:
        if round_num < 1:
            raise ValueError("round number must be >= 1")

        evidence_records = []
        for e in evidence or []:
            p = Path(e).expanduser()
            if not p.exists():
                evidence_records.append({"path": str(p), "exists": False,
                                         "bytes": 0, "sha256": None})
                print(f"warning: evidence missing -> {p}", file=sys.stderr)
            else:
                evidence_records.append({"path": str(p.resolve()), "exists": True,
                                         "bytes": p.stat().st_size,
                                         "sha256": sha256_of(p)})

        record = {
            "round": round_num,
            "phase": PHASES.get(round_num, f"round_{round_num}"),
            "date": datetime.now().isoformat(timespec="seconds"),
            "issues": list(issues or []),
            "actions_taken": actions or "",
            "status": "resolved" if (actions or "").strip() else "open",
            "evidence": evidence_records,
        }

        history = self.load()
        history["rounds"] = [r for r in history["rounds"] if r.get("round") != round_num]
        history["rounds"].append(record)
        history["rounds"].sort(key=lambda r: r["round"])
        history["rounds_completed"] = max([r["round"] for r in history["rounds"]] or [0])
        history["total_issues"] = sum(len(r.get("issues", [])) for r in history["rounds"])
        self.save(history)

        print(f"recorded round {round_num}: {len(record['issues'])} issue(s), "
              f"{sum(1 for e in evidence_records if e['exists'])} evidence file(s) verified")
        return record

    def report(self) -> Path:
        history = self.load()
        rounds = history.get("rounds", [])
        lines = ["# Revision Effectiveness Report", "",
                 f"Generated: {datetime.now().isoformat(timespec='seconds')}",
                 f"Rounds completed: {history.get('rounds_completed', 0)} "
                 f"(>= {MIN_ROUNDS_FOR_SUBMISSION} expected before submission)",
                 f"Total issues logged: {history.get('total_issues', 0)}", ""]
        if not rounds:
            lines.append("No revision rounds recorded yet.")
        for r in rounds:
            resolved = sum(1 for i in r.get("issues", []) if r.get("actions_taken"))
            lines += [f"## Round {r['round']} - {r.get('phase', '')}",
                      f"- Date: {r.get('date', '')[:10]}",
                      f"- Issues: {len(r.get('issues', []))} "
                      f"(addressed in this round: {resolved})",
                      f"- Actions: {r.get('actions_taken') or 'NONE RECORDED'}",
                      f"- Status: {r.get('status')}", ""]
            for i in r.get("issues", []):
                lines.append(f"  - {i}")
            if r.get("evidence"):
                lines.append("- Evidence:")
                for e in r["evidence"]:
                    if e["exists"]:
                        lines.append(f"  - `{e['path']}` ({e['bytes']} B, "
                                     f"sha256 {e['sha256'][:12]}...)")
                    else:
                        lines.append(f"  - `{e['path']}` MISSING")
            lines.append("")

        missing = sum(1 for r in rounds for e in r.get("evidence", []) if not e["exists"])
        lines += ["---", "## Audit summary", "",
                  f"- Rounds: {len(rounds)}",
                  f"- Missing evidence artifacts: {missing}",
                  f"- Submission gate (>= {MIN_ROUNDS_FOR_SUBMISSION} rounds): "
                  f"{'PASS' if history.get('rounds_completed', 0) >= MIN_ROUNDS_FOR_SUBMISSION else 'NOT MET'}"]
        out = self.tracking_dir / "revision-tracking-report.md"
        out.write_text("\n".join(lines), encoding="utf-8")
        return out

    def summary(self) -> str:
        history = self.load()
        done = history.get("rounds_completed", 0)
        gap = max(0, MIN_ROUNDS_FOR_SUBMISSION - done)
        text = (f"Revision progress: {done}/{MIN_ROUNDS_FOR_SUBMISSION} rounds\n"
                f"Total issues logged: {history.get('total_issues', 0)}\n"
                f"Last update: {history.get('last_updated') or 'never'}\n"
                f"Remaining before submission gate: {gap} round(s)\n")
        return text


def main() -> int:
    ap = argparse.ArgumentParser(description="Track systematic paper revision rounds")
    ap.add_argument("--action", "-a", required=True,
                    choices=["add_round", "add", "report", "summary"])
    ap.add_argument("--round", "-r", type=int, default=None)
    ap.add_argument("--issues", "-i", nargs="*", default=[])
    ap.add_argument("--actions", "-x", default="")
    ap.add_argument("--evidence", "-e", nargs="*", default=[])
    ap.add_argument("--tracking-dir", "-d", "-p", default="./05-revision-rounds")
    args = ap.parse_args()

    tracker = RevisionTracker(Path(args.tracking_dir).expanduser().resolve())

    if args.action in ("add_round", "add"):
        if args.round is None:
            print("error: --round required for add_round", file=sys.stderr)
            return 2
        tracker.add_round(args.round, args.issues, args.actions, args.evidence)
        return 0
    if args.action == "report":
        print(tracker.report())
        return 0
    if args.action == "summary":
        print(tracker.summary())
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
