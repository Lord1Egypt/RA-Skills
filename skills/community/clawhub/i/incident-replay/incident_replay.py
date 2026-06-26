#!/usr/bin/env python3
"""
Incident Replay — Timeline Reconstruction & Analysis
======================================================
Reconstruct what happened leading to a failure, extract decision chains
from logs, classify root causes, and manage an incident database.

Usage:
    from incident_replay import Analyzer
    analyzer = Analyzer(config)
    timeline = analyzer.build_timeline(snapshots)
    incident = analyzer.create_incident(timeline, triggers, classification="config_error")

CLI:
    python3 incident_replay.py --config incident_config.json --analyze snap1.json snap2.json
    python3 incident_replay.py --config incident_config.json --incidents
    python3 incident_replay.py --config incident_config.json --incident INC-001
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

# Import sibling module types
try:
    from incident_capture import (
        Capturer, FileChange, Snapshot, TriggerHit, _load_config, _get, _matches_any
    )
except ImportError:
    # Allow standalone import for type checking
    def _load_config(path):  # type: ignore
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Config not found: {path}")
        if not path.endswith(".json"):
            raise ValueError(f"Config must be a .json file: {path}")
        if os.path.getsize(path) > 1_000_000:
            raise ValueError(f"Config file too large (>1MB): {path}")
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _get(cfg, name, default=None):  # type: ignore
        if isinstance(cfg, dict):
            return cfg.get(name, default)
        return getattr(cfg, name, default)

    def _matches_any(path, patterns):  # type: ignore
        import fnmatch as _fn
        name = os.path.basename(path)
        return any(_fn.fnmatch(path, p) or _fn.fnmatch(name, p) for p in patterns)


# ── Data Structures ───────────────────────────────────────────────────────

@dataclass
class TimelineEvent:
    timestamp: str
    event_type: str  # "snapshot", "file_change", "trigger", "decision"
    description: str
    details: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "event_type": self.event_type,
            "description": self.description,
            "details": self.details,
        }


@dataclass
class DecisionPoint:
    timestamp: str
    source_file: str
    line_number: int
    text: str
    decision_type: str  # "action", "reason", "choice"

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "source": self.source_file,
            "line": self.line_number,
            "text": self.text,
            "type": self.decision_type,
        }


@dataclass
class Incident:
    id: str
    created: str
    title: str
    severity: str  # "critical", "high", "medium", "low"
    root_cause: str  # category key
    root_cause_description: str
    timeline: List[TimelineEvent]
    triggers: List[dict]
    file_changes: List[dict]
    decisions: List[DecisionPoint]
    remediation: List[str]
    notes: str = ""
    resolved: bool = False

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "created": self.created,
            "title": self.title,
            "severity": self.severity,
            "root_cause": self.root_cause,
            "root_cause_description": self.root_cause_description,
            "timeline": [e.to_dict() for e in self.timeline],
            "triggers": self.triggers,
            "file_changes": self.file_changes,
            "decisions": [d.to_dict() for d in self.decisions],
            "remediation": self.remediation,
            "notes": self.notes,
            "resolved": self.resolved,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Incident":
        return cls(
            id=d["id"],
            created=d.get("created", ""),
            title=d.get("title", ""),
            severity=d.get("severity", "medium"),
            root_cause=d.get("root_cause", "unknown"),
            root_cause_description=d.get("root_cause_description", ""),
            timeline=[
                TimelineEvent(**e) for e in d.get("timeline", [])
            ],
            triggers=d.get("triggers", []),
            file_changes=d.get("file_changes", []),
            decisions=[
                DecisionPoint(**dp) for dp in d.get("decisions", [])
            ],
            remediation=d.get("remediation", []),
            notes=d.get("notes", ""),
            resolved=d.get("resolved", False),
        )


# ── Analyzer ──────────────────────────────────────────────────────────────

class Analyzer:
    """Timeline reconstruction, decision extraction, and incident management."""

    def __init__(self, config: Any):
        self.config = config
        self.data_dir = _get(config, "DATA_DIR", "incident_data")
        self.incidents_dir = os.path.join(self.data_dir, _get(config, "INCIDENTS_DIR", "incidents"))
        self.snapshots_dir = os.path.join(self.data_dir, _get(config, "SNAPSHOTS_DIR", "snapshots"))
        self.root_causes = _get(config, "ROOT_CAUSE_CATEGORIES", {})
        self.decision_markers = _get(config, "DECISION_MARKERS", [])
        self.log_files = _get(config, "LOG_FILES", ["*.log"])
        self.max_log_lines = _get(config, "MAX_LOG_LINES", 10000)
        self.timeline_depth = _get(config, "TIMELINE_DEPTH", 10)
        self.significant_threshold = _get(config, "SIGNIFICANT_CHANGE_THRESHOLD", 5)

    def build_timeline(
        self,
        snapshots: List[Any],
        triggers: Optional[List[dict]] = None,
        changes: Optional[List[Any]] = None,
    ) -> List[TimelineEvent]:
        """Build a chronological timeline from snapshots, triggers, and changes."""
        events: list[TimelineEvent] = []

        # Snapshot events
        for snap in snapshots:
            if hasattr(snap, "timestamp"):
                ts = snap.timestamp
                fc = snap.file_count
                label = snap.label
            else:
                ts = snap.get("timestamp", "")
                fc = snap.get("file_count", 0)
                label = snap.get("label", "")
            events.append(TimelineEvent(
                timestamp=ts,
                event_type="snapshot",
                description=f"Snapshot '{label}': {fc} files",
                details={"label": label, "file_count": fc},
            ))

        # File change events
        if changes:
            for ch in changes:
                if hasattr(ch, "to_dict"):
                    d = ch.to_dict()
                    path = ch.path
                    ctype = ch.change_type
                else:
                    d = ch
                    path = ch.get("path", "")
                    ctype = ch.get("change_type", "")
                events.append(TimelineEvent(
                    timestamp="",  # changes don't have timestamps
                    event_type="file_change",
                    description=f"{ctype}: {path}",
                    details=d if isinstance(d, dict) else {},
                ))

        # Trigger events
        if triggers:
            for t in triggers:
                if hasattr(t, "to_dict"):
                    d = t.to_dict()
                else:
                    d = t
                events.append(TimelineEvent(
                    timestamp="",
                    event_type="trigger",
                    description=f"[{d.get('severity', 'medium').upper()}] {d.get('trigger', d.get('trigger_name', ''))}",
                    details=d,
                ))

        # Sort by timestamp (empty timestamps go to end)
        events.sort(key=lambda e: e.timestamp or "9999")
        return events

    def extract_decisions(self, snapshot: Any) -> List[DecisionPoint]:
        """Extract decision points from log files in a snapshot."""
        decisions: list[DecisionPoint] = []
        files = snapshot.files if hasattr(snapshot, "files") else {}

        for path, entry in files.items():
            if not _matches_any(path, self.log_files):
                continue
            content = entry.content if hasattr(entry, "content") else entry.get("content")
            if not content:
                continue

            lines = content.splitlines()
            for i, line in enumerate(lines[:self.max_log_lines]):
                for pattern in self.decision_markers:
                    try:
                        match = re.search(pattern, line, re.I)
                        if match:
                            # Try to extract a timestamp from the line
                            ts_match = re.match(
                                r"(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2})", line
                            )
                            ts = ts_match.group(1) if ts_match else ""

                            # Categorise the decision type
                            lower = pattern.lower()
                            if "reason" in lower or "because" in lower:
                                dtype = "reason"
                            elif "action" in lower or "step" in lower:
                                dtype = "action"
                            else:
                                dtype = "choice"

                            decisions.append(DecisionPoint(
                                timestamp=ts,
                                source_file=path,
                                line_number=i + 1,
                                text=match.group(0)[:500],
                                decision_type=dtype,
                            ))
                    except re.error:
                        continue

        return decisions

    def classify_root_cause(
        self,
        changes: List[Any],
        triggers: List[dict],
        decisions: List[DecisionPoint],
    ) -> Tuple[str, str, List[str]]:
        """
        Heuristic root cause classification.
        Returns (category, description, remediation_steps).
        """
        # Count signals
        config_changes = 0
        deletions = 0
        crash_signals = 0
        external_signals = 0

        for ch in changes:
            path = ch.path if hasattr(ch, "path") else ch.get("path", "")
            ctype = ch.change_type if hasattr(ch, "change_type") else ch.get("change_type", "")
            if ctype == "deleted":
                deletions += 1
            if ctype == "modified" and any(
                p in path.lower()
                for p in ["config", ".cfg", ".ini", ".yaml", ".yml", ".env"]
            ):
                config_changes += 1

        for t in triggers:
            sev = t.get("severity", "") if isinstance(t, dict) else getattr(t, "severity", "")
            name = t.get("trigger", t.get("trigger_name", "")) if isinstance(t, dict) else getattr(t, "trigger_name", "")
            if "crash" in name.lower() or "traceback" in name.lower():
                crash_signals += 1
            if "external" in name.lower() or "timeout" in name.lower():
                external_signals += 1

        # Classification logic
        if config_changes > 0 and crash_signals > 0:
            category = "config_error"
        elif deletions > self.significant_threshold:
            category = "data_corruption"
        elif external_signals > 0:
            category = "external_failure"
        elif crash_signals > 0 and config_changes == 0:
            category = "logic_error"
        elif len(changes) > self.significant_threshold * 2 and crash_signals == 0:
            category = "drift"
        else:
            category = "unknown"

        cat_info = self.root_causes.get(category, {})
        description = cat_info.get("description", "Unknown root cause")
        remediation = cat_info.get("remediation", [])

        return category, description, remediation

    def create_incident(
        self,
        title: str,
        timeline: List[TimelineEvent],
        triggers: List[dict],
        file_changes: List[Any],
        decisions: List[DecisionPoint],
        severity: Optional[str] = None,
        root_cause: Optional[str] = None,
        notes: str = "",
    ) -> Incident:
        """Create and persist a new incident."""
        now = datetime.now(timezone.utc)

        # Auto-determine severity from triggers if not provided
        if severity is None:
            sev_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
            best = "low"
            for t in triggers:
                s = t.get("severity", "low") if isinstance(t, dict) else getattr(t, "severity", "low")
                if sev_order.get(s, 3) < sev_order.get(best, 3):
                    best = s
            severity = best

        # Auto-classify if not provided
        if root_cause is None:
            root_cause, rc_desc, remediation = self.classify_root_cause(
                file_changes, triggers, decisions
            )
        else:
            cat_info = self.root_causes.get(root_cause, {})
            rc_desc = cat_info.get("description", "")
            remediation = cat_info.get("remediation", [])

        # Generate ID
        inc_id = self._next_incident_id()

        # Serialise changes
        changes_dicts = []
        for ch in file_changes:
            if hasattr(ch, "to_dict"):
                changes_dicts.append(ch.to_dict())
            elif isinstance(ch, dict):
                changes_dicts.append(ch)

        trigger_dicts = []
        for t in triggers:
            if hasattr(t, "to_dict"):
                trigger_dicts.append(t.to_dict())
            elif isinstance(t, dict):
                trigger_dicts.append(t)

        incident = Incident(
            id=inc_id,
            created=now.isoformat(),
            title=title,
            severity=severity,
            root_cause=root_cause,
            root_cause_description=rc_desc,
            timeline=timeline,
            triggers=trigger_dicts,
            file_changes=changes_dicts,
            decisions=decisions,
            remediation=remediation,
            notes=notes,
        )

        # Save
        self._save_incident(incident)
        return incident

    def _next_incident_id(self) -> str:
        os.makedirs(self.incidents_dir, exist_ok=True)
        existing = [
            f for f in os.listdir(self.incidents_dir)
            if f.startswith("INC-") and f.endswith(".json")
        ]
        nums = []
        for f in existing:
            try:
                nums.append(int(f[4:-5]))
            except ValueError:
                continue
        next_num = max(nums) + 1 if nums else 1
        return f"INC-{next_num:04d}"

    def _save_incident(self, incident: Incident) -> str:
        os.makedirs(self.incidents_dir, exist_ok=True)
        path = os.path.join(self.incidents_dir, f"{incident.id}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(incident.to_dict(), f, indent=2, default=str)
        return path

    def load_incident(self, incident_id: str) -> Optional[Incident]:
        path = os.path.join(self.incidents_dir, f"{incident_id}.json")
        if not os.path.exists(path):
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                return Incident.from_dict(json.load(f))
        except (json.JSONDecodeError, OSError, KeyError) as exc:
            print(f"Error loading incident {incident_id}: {exc}", file=sys.stderr)
            return None

    def list_incidents(self) -> List[dict]:
        results: list[dict] = []
        try:
            files = sorted(f for f in os.listdir(self.incidents_dir) if f.endswith(".json"))
        except OSError:
            return results
        for fname in files:
            path = os.path.join(self.incidents_dir, fname)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                results.append({
                    "id": data.get("id", fname),
                    "created": data.get("created", ""),
                    "title": data.get("title", ""),
                    "severity": data.get("severity", ""),
                    "root_cause": data.get("root_cause", ""),
                    "resolved": data.get("resolved", False),
                })
            except (json.JSONDecodeError, OSError):
                continue
        return results

    def find_patterns(self) -> Dict[str, int]:
        """Find recurring root cause patterns across all incidents."""
        pattern_counts: Dict[str, int] = {}
        incidents = self.list_incidents()
        for inc in incidents:
            rc = inc.get("root_cause", "unknown")
            pattern_counts[rc] = pattern_counts.get(rc, 0) + 1
        return dict(sorted(pattern_counts.items(), key=lambda x: -x[1]))


# ── CLI ───────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Incident Replay — analysis & management")
    parser.add_argument("--config", required=True, help="Path to config .json file")
    parser.add_argument("--analyze", nargs=2, metavar="SNAP", help="Analyze between two snapshots")
    parser.add_argument("--title", default="Unnamed incident", help="Incident title")
    parser.add_argument("--incidents", action="store_true", help="List all incidents")
    parser.add_argument("--incident", default=None, help="Show specific incident by ID")
    parser.add_argument("--patterns", action="store_true", help="Show root cause patterns")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    try:
        cfg = _load_config(args.config)
    except Exception as exc:
        print(f"Error loading config: {exc}", file=sys.stderr)
        sys.exit(1)

    analyzer = Analyzer(cfg)

    if args.analyze:
        try:
            # Import Snapshot from sibling
            from incident_capture import Snapshot, Capturer
            snap_a = Snapshot.load(args.analyze[0])
            snap_b = Snapshot.load(args.analyze[1])
        except Exception as exc:
            print(f"Error loading snapshots: {exc}", file=sys.stderr)
            sys.exit(1)

        cap = Capturer(cfg)
        changes = cap.diff_snapshots(snap_a, snap_b)
        triggers = cap.check_triggers(snap_a, snap_b)
        trigger_dicts = [t.to_dict() for t in triggers]
        decisions = analyzer.extract_decisions(snap_b)
        timeline = analyzer.build_timeline(
            [snap_a, snap_b], triggers=trigger_dicts, changes=changes
        )

        incident = analyzer.create_incident(
            title=args.title,
            timeline=timeline,
            triggers=trigger_dicts,
            file_changes=changes,
            decisions=decisions,
        )

        if args.json:
            print(json.dumps(incident.to_dict(), indent=2, default=str))
        else:
            print(f"Incident {incident.id} created")
            print(f"  Title: {incident.title}")
            print(f"  Severity: {incident.severity}")
            print(f"  Root cause: {incident.root_cause} — {incident.root_cause_description}")
            print(f"  Timeline events: {len(incident.timeline)}")
            print(f"  File changes: {len(incident.file_changes)}")
            print(f"  Decisions: {len(incident.decisions)}")
            print(f"  Remediation:")
            for r in incident.remediation:
                print(f"    → {r}")
        return

    if args.incidents:
        incidents = analyzer.list_incidents()
        if args.json:
            print(json.dumps(incidents, indent=2))
        else:
            if not incidents:
                print("No incidents recorded.")
            for inc in incidents:
                status = "✅" if inc.get("resolved") else "🔴"
                print(
                    f"  {status} {inc['id']}  [{inc['severity'].upper()}]  "
                    f"{inc['title']}  ({inc['root_cause']})"
                )
        return

    if args.incident:
        inc = analyzer.load_incident(args.incident)
        if inc is None:
            print(f"Incident {args.incident} not found.", file=sys.stderr)
            sys.exit(1)
        if args.json:
            print(json.dumps(inc.to_dict(), indent=2, default=str))
        else:
            print(f"Incident: {inc.id}")
            print(f"  Created: {inc.created}")
            print(f"  Title: {inc.title}")
            print(f"  Severity: {inc.severity}")
            print(f"  Root cause: {inc.root_cause} — {inc.root_cause_description}")
            print(f"  Resolved: {inc.resolved}")
            print(f"  Timeline: {len(inc.timeline)} events")
            print(f"  Changes: {len(inc.file_changes)}")
            print(f"  Decisions: {len(inc.decisions)}")
            if inc.remediation:
                print(f"  Remediation:")
                for r in inc.remediation:
                    print(f"    → {r}")
            if inc.notes:
                print(f"  Notes: {inc.notes}")
        return

    if args.patterns:
        patterns = analyzer.find_patterns()
        if args.json:
            print(json.dumps(patterns, indent=2))
        else:
            if not patterns:
                print("No incidents to analyse.")
            for cause, count in patterns.items():
                print(f"  {cause}: {count} incidents")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
