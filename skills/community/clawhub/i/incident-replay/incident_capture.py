#!/usr/bin/env python3
"""
Incident Replay — State Snapshot & Change Detection
=====================================================
Capture workspace state at a point in time, detect changes between snapshots,
and identify incident triggers.

Usage:
    from incident_capture import Capturer
    cap = Capturer(config)
    snapshot = cap.take_snapshot(label="before-deploy")
    changes = cap.diff_snapshots(snap_a, snap_b)
    triggers = cap.check_triggers(snap_a, snap_b)

CLI:
    python3 incident_capture.py --config incident_config.json --snapshot
    python3 incident_capture.py --config incident_config.json --diff snap1.json snap2.json
    python3 incident_capture.py --config incident_config.json --triggers snap1.json snap2.json
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple


def _load_config(path: str) -> Any:
    """Load configuration from a JSON file."""
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Config not found: {path}")
    if not path.endswith(".json"):
        raise ValueError(f"Config must be a .json file: {path}")
    if os.path.getsize(path) > 1_000_000:
        raise ValueError(f"Config file too large (>1MB): {path}")
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def _get(cfg: Any, name: str, default: Any = None) -> Any:
    if isinstance(cfg, dict):
        return cfg.get(name, default)
    return getattr(cfg, name, default)


def _matches_any(path: str, patterns: list) -> bool:
    name = os.path.basename(path)
    for pat in patterns:
        if fnmatch.fnmatch(path, pat) or fnmatch.fnmatch(name, pat):
            return True
    return False


def _file_hash(path: str) -> str:
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
    except (OSError, IOError):
        return ""
    return h.hexdigest()


# ── Data Structures ───────────────────────────────────────────────────────

@dataclass
class FileEntry:
    path: str
    size: int
    modified: float
    sha256: str
    content: Optional[str] = None  # None if too large or binary

    def to_dict(self) -> dict:
        d: dict = {
            "path": self.path,
            "size": self.size,
            "modified": self.modified,
            "sha256": self.sha256,
        }
        if self.content is not None:
            d["content"] = self.content
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "FileEntry":
        return cls(
            path=d["path"],
            size=d.get("size", 0),
            modified=d.get("modified", 0),
            sha256=d.get("sha256", ""),
            content=d.get("content"),
        )


@dataclass
class Snapshot:
    id: str
    label: str
    timestamp: str
    workspace_root: str
    files: Dict[str, FileEntry]
    total_size: int
    file_count: int

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "label": self.label,
            "timestamp": self.timestamp,
            "workspace_root": self.workspace_root,
            "total_size": self.total_size,
            "file_count": self.file_count,
            "files": {k: v.to_dict() for k, v in self.files.items()},
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Snapshot":
        files = {
            k: FileEntry.from_dict(v)
            for k, v in d.get("files", {}).items()
        }
        return cls(
            id=d["id"],
            label=d.get("label", ""),
            timestamp=d.get("timestamp", ""),
            workspace_root=d.get("workspace_root", ""),
            files=files,
            total_size=d.get("total_size", 0),
            file_count=d.get("file_count", 0),
        )

    def save(self, path: str) -> None:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, path: str) -> "Snapshot":
        with open(path, "r", encoding="utf-8") as f:
            return cls.from_dict(json.load(f))


@dataclass
class FileChange:
    path: str
    change_type: str  # "added", "modified", "deleted"
    old_hash: str = ""
    new_hash: str = ""
    old_size: int = 0
    new_size: int = 0
    size_delta: int = 0
    content_diff: Optional[str] = None

    def to_dict(self) -> dict:
        d: dict = {
            "path": self.path,
            "change_type": self.change_type,
            "size_delta": self.size_delta,
        }
        if self.old_hash:
            d["old_hash"] = self.old_hash[:12]
        if self.new_hash:
            d["new_hash"] = self.new_hash[:12]
        if self.content_diff:
            d["content_diff"] = self.content_diff
        return d


@dataclass
class TriggerHit:
    trigger_name: str
    severity: str
    description: str
    evidence: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "trigger": self.trigger_name,
            "severity": self.severity,
            "description": self.description,
            "evidence": self.evidence,
        }


# ── Capturer ──────────────────────────────────────────────────────────────

class Capturer:
    """Capture workspace state and detect changes."""

    def __init__(self, config: Any):
        self.root = os.path.abspath(_get(config, "WORKSPACE_ROOT", "."))
        self.data_dir = _get(config, "DATA_DIR", "incident_data")
        self.include = _get(config, "INCLUDE_PATTERNS", ["*"])
        self.exclude = _get(config, "EXCLUDE_PATTERNS", [])
        self.max_file_size = _get(config, "MAX_FILE_SIZE", 1_000_000)
        self.max_snapshot_size = _get(config, "MAX_SNAPSHOT_SIZE", 50_000_000)
        self.max_snapshots = _get(config, "MAX_SNAPSHOTS", 100)
        self.triggers_cfg = _get(config, "TRIGGERS", [])
        self.max_diff_lines = _get(config, "MAX_DIFF_LINES", 100)
        self.snapshots_dir = os.path.join(self.data_dir, _get(config, "SNAPSHOTS_DIR", "snapshots"))

    def take_snapshot(self, label: str = "") -> Snapshot:
        """Walk workspace and capture file state."""
        now = datetime.now(timezone.utc)
        snap_id = now.strftime("%Y%m%d_%H%M%S")
        files: Dict[str, FileEntry] = {}
        total_size = 0

        for dirpath, dirnames, filenames in os.walk(self.root):
            # Skip excluded directories
            dirnames[:] = [
                d for d in dirnames
                if not _matches_any(os.path.join(dirpath, d) + "/", self.exclude)
            ]
            for fname in filenames:
                full_path = os.path.join(dirpath, fname)
                rel_path = os.path.relpath(full_path, self.root)

                if not _matches_any(rel_path, self.include):
                    continue
                if _matches_any(rel_path, self.exclude):
                    continue

                try:
                    stat = os.stat(full_path)
                except OSError:
                    continue

                size = stat.st_size
                total_size += size
                if total_size > self.max_snapshot_size:
                    raise RuntimeError(
                        f"Snapshot exceeds MAX_SNAPSHOT_SIZE ({self.max_snapshot_size} bytes). "
                        f"Adjust INCLUDE_PATTERNS or MAX_SNAPSHOT_SIZE."
                    )

                fhash = _file_hash(full_path)
                content = None
                if size <= self.max_file_size:
                    try:
                        with open(full_path, "r", encoding="utf-8", errors="replace") as fh:
                            content = fh.read()
                    except (OSError, IOError):
                        pass

                files[rel_path] = FileEntry(
                    path=rel_path,
                    size=size,
                    modified=stat.st_mtime,
                    sha256=fhash,
                    content=content,
                )

        snapshot = Snapshot(
            id=snap_id,
            label=label,
            timestamp=now.isoformat(),
            workspace_root=self.root,
            files=files,
            total_size=total_size,
            file_count=len(files),
        )

        # Save snapshot
        snap_path = os.path.join(self.snapshots_dir, f"{snap_id}.json")
        snapshot.save(snap_path)

        # Enforce max snapshots
        self._prune_snapshots()

        return snapshot

    def _prune_snapshots(self) -> None:
        if self.max_snapshots <= 0:
            return
        try:
            snaps = sorted(
                f for f in os.listdir(self.snapshots_dir)
                if f.endswith(".json")
            )
        except OSError:
            return
        while len(snaps) > self.max_snapshots:
            oldest = snaps.pop(0)
            try:
                os.remove(os.path.join(self.snapshots_dir, oldest))
            except OSError:
                pass

    def diff_snapshots(self, before: Snapshot, after: Snapshot) -> List[FileChange]:
        """Compute file-level diff between two snapshots."""
        changes: list[FileChange] = []
        all_paths = set(before.files.keys()) | set(after.files.keys())

        for path in sorted(all_paths):
            old = before.files.get(path)
            new = after.files.get(path)

            if old is None and new is not None:
                changes.append(FileChange(
                    path=path,
                    change_type="added",
                    new_hash=new.sha256,
                    new_size=new.size,
                    size_delta=new.size,
                ))
            elif old is not None and new is None:
                changes.append(FileChange(
                    path=path,
                    change_type="deleted",
                    old_hash=old.sha256,
                    old_size=old.size,
                    size_delta=-old.size,
                ))
            elif old is not None and new is not None and old.sha256 != new.sha256:
                diff_text = None
                if old.content and new.content:
                    diff_text = self._simple_diff(old.content, new.content, path)
                changes.append(FileChange(
                    path=path,
                    change_type="modified",
                    old_hash=old.sha256,
                    new_hash=new.sha256,
                    old_size=old.size,
                    new_size=new.size,
                    size_delta=new.size - old.size,
                    content_diff=diff_text,
                ))

        return changes

    def _simple_diff(self, old_text: str, new_text: str, path: str) -> str:
        """Generate a simple line-by-line diff (no external deps)."""
        old_lines = old_text.splitlines()
        new_lines = new_text.splitlines()
        output: list[str] = [f"--- {path} (before)", f"+++ {path} (after)"]
        max_lines = self.max_diff_lines
        count = 0

        # Simple approach: show lines unique to each version
        old_set = set(old_lines)
        new_set = set(new_lines)
        removed = [l for l in old_lines if l not in new_set]
        added = [l for l in new_lines if l not in old_set]

        for line in removed:
            if count >= max_lines:
                output.append(f"... ({len(removed) - count} more removed)")
                break
            output.append(f"- {line}")
            count += 1

        count = 0
        for line in added:
            if count >= max_lines:
                output.append(f"... ({len(added) - count} more added)")
                break
            output.append(f"+ {line}")
            count += 1

        return "\n".join(output)

    def check_triggers(
        self, before: Snapshot, after: Snapshot
    ) -> List[TriggerHit]:
        """Check all configured triggers against the change between snapshots."""
        changes = self.diff_snapshots(before, after)
        hits: list[TriggerHit] = []

        for trigger in self.triggers_cfg:
            name = trigger.get("name", "unnamed")
            ttype = trigger.get("type", "")
            cfg = trigger.get("config", {})
            severity = trigger.get("severity", "medium")

            try:
                if ttype == "file_change":
                    hit = self._check_file_change_trigger(name, cfg, severity, changes)
                elif ttype == "log_match":
                    hit = self._check_log_match_trigger(name, cfg, severity, after)
                elif ttype == "pattern":
                    hit = self._check_pattern_trigger(name, cfg, severity, after)
                else:
                    continue
                if hit:
                    hits.append(hit)
            except Exception:
                continue

        return hits

    def _check_file_change_trigger(
        self, name: str, cfg: dict, severity: str, changes: list[FileChange]
    ) -> Optional[TriggerHit]:
        change_type = cfg.get("change_type", "")
        patterns = cfg.get("protected_patterns", cfg.get("watch_patterns", ["*"]))
        evidence: list[str] = []
        for ch in changes:
            if ch.change_type == change_type and _matches_any(ch.path, patterns):
                evidence.append(f"{ch.change_type}: {ch.path}")
        if evidence:
            return TriggerHit(
                trigger_name=name,
                severity=severity,
                description=f"Detected {change_type} on watched files",
                evidence=evidence,
            )
        return None

    def _check_log_match_trigger(
        self, name: str, cfg: dict, severity: str, snapshot: Snapshot
    ) -> Optional[TriggerHit]:
        patterns = cfg.get("patterns", [])
        log_globs = cfg.get("log_files", ["*.log"])
        evidence: list[str] = []
        for path, entry in snapshot.files.items():
            if not _matches_any(path, log_globs):
                continue
            if entry.content is None:
                continue
            for pat in patterns:
                try:
                    matches = re.findall(pat, entry.content, re.M)
                    for m in matches[:5]:
                        evidence.append(f"{path}: {m[:200]}")
                except re.error:
                    continue
        if evidence:
            return TriggerHit(
                trigger_name=name,
                severity=severity,
                description="Log pattern matched",
                evidence=evidence,
            )
        return None

    def _check_pattern_trigger(
        self, name: str, cfg: dict, severity: str, snapshot: Snapshot
    ) -> Optional[TriggerHit]:
        # Check for empty files
        if cfg.get("check") == "empty_file":
            watch = cfg.get("watch_patterns", [])
            evidence: list[str] = []
            for path, entry in snapshot.files.items():
                if _matches_any(path, watch) and entry.size == 0:
                    evidence.append(f"Empty file: {path}")
            if evidence:
                return TriggerHit(
                    trigger_name=name,
                    severity=severity,
                    description="Empty output files detected",
                    evidence=evidence,
                )
            return None

        # Pattern scan on file content
        patterns = cfg.get("patterns", [])
        scan_globs = cfg.get("scan_files", ["*"])
        desc = cfg.get("description", "Pattern matched")
        evidence_list: list[str] = []
        for path, entry in snapshot.files.items():
            if not _matches_any(path, scan_globs):
                continue
            if entry.content is None:
                continue
            for pat in patterns:
                try:
                    if re.search(pat, entry.content, re.I | re.M):
                        evidence_list.append(f"{path}: matches '{pat}'")
                except re.error:
                    continue
        if evidence_list:
            return TriggerHit(
                trigger_name=name,
                severity=severity,
                description=desc,
                evidence=evidence_list,
            )
        return None

    def list_snapshots(self) -> List[dict]:
        """List available snapshots (id, timestamp, label)."""
        results: list[dict] = []
        try:
            files = sorted(f for f in os.listdir(self.snapshots_dir) if f.endswith(".json"))
        except OSError:
            return results
        for fname in files:
            path = os.path.join(self.snapshots_dir, fname)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                results.append({
                    "id": data.get("id", fname),
                    "timestamp": data.get("timestamp", ""),
                    "label": data.get("label", ""),
                    "file_count": data.get("file_count", 0),
                    "total_size": data.get("total_size", 0),
                    "path": path,
                })
            except (json.JSONDecodeError, OSError):
                continue
        return results


# ── CLI ───────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Incident Replay — state capture")
    parser.add_argument("--config", required=True, help="Path to config .json file")
    parser.add_argument("--snapshot", action="store_true", help="Take a new snapshot")
    parser.add_argument("--label", default="", help="Snapshot label")
    parser.add_argument("--list", action="store_true", help="List available snapshots")
    parser.add_argument("--diff", nargs=2, metavar="SNAP", help="Diff two snapshot files")
    parser.add_argument("--triggers", nargs=2, metavar="SNAP", help="Check triggers between snapshots")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    try:
        cfg = _load_config(args.config)
    except Exception as exc:
        print(f"Error loading config: {exc}", file=sys.stderr)
        sys.exit(1)

    cap = Capturer(cfg)

    if args.snapshot:
        snap = cap.take_snapshot(label=args.label)
        print(f"Snapshot {snap.id} captured: {snap.file_count} files, {snap.total_size} bytes")
        if args.json:
            print(json.dumps(snap.to_dict(), indent=2))
        return

    if args.list:
        snaps = cap.list_snapshots()
        if args.json:
            print(json.dumps(snaps, indent=2))
        else:
            for s in snaps:
                print(f"  {s['id']}  {s['timestamp'][:19]}  {s['file_count']} files  {s.get('label', '')}")
        return

    if args.diff:
        try:
            a = Snapshot.load(args.diff[0])
            b = Snapshot.load(args.diff[1])
        except Exception as exc:
            print(f"Error loading snapshots: {exc}", file=sys.stderr)
            sys.exit(1)
        changes = cap.diff_snapshots(a, b)
        if args.json:
            print(json.dumps([c.to_dict() for c in changes], indent=2))
        else:
            if not changes:
                print("No changes detected.")
            for c in changes:
                symbol = {"added": "+", "deleted": "-", "modified": "~"}[c.change_type]
                print(f"  {symbol} {c.path} ({c.size_delta:+d} bytes)")
        return

    if args.triggers:
        try:
            a = Snapshot.load(args.triggers[0])
            b = Snapshot.load(args.triggers[1])
        except Exception as exc:
            print(f"Error loading snapshots: {exc}", file=sys.stderr)
            sys.exit(1)
        hits = cap.check_triggers(a, b)
        if args.json:
            print(json.dumps([h.to_dict() for h in hits], indent=2))
        else:
            if not hits:
                print("No triggers fired.")
            for h in hits:
                print(f"  [{h.severity.upper()}] {h.trigger_name}: {h.description}")
                for e in h.evidence[:5]:
                    print(f"    → {e}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
