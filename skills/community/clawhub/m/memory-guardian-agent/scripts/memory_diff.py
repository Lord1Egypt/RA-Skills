#!/usr/bin/env python3
"""memory-guardian: Rule-based diff engine for MEMORY.md changes.

Compares current MEMORY.md against a snapshot, producing a structured diff.
Designed to pair with the semantic diff route (xiaobai_butler) at merge layer.

Usage:
  python3 memory_diff.py [--workspace <path>] [--output <path>]
"""
import json, os, hashlib, argparse, re
from datetime import datetime
from mg_utils import CST, save_meta as _atomic_save

SNAPSHOT_DIR = ".memory-guardian/diff-snapshots"

def hash_file(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def load_snapshot(snapshot_path):
    if not os.path.exists(snapshot_path):
        return None
    with open(snapshot_path, "r", encoding="utf-8") as f:
        return f.read()

def rule_diff(old_text, new_text):
    """Produce a structured diff using line-level + regex rules."""
    changes = []
    old_lines = (old_text or "").splitlines()
    new_lines = (new_text or "").splitlines()

    # Simple line-level diff
    import difflib
    sm = difflib.SequenceMatcher(None, old_lines, new_lines)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        change = {"op": tag}
        if tag == "replace":
            change["removed"] = old_lines[i1:i2]
            change["added"] = new_lines[j1:j2]
        elif tag == "delete":
            change["removed"] = old_lines[i1:i2]
        elif tag == "insert":
            change["added"] = new_lines[j1:j2]
        changes.append(change)

    # Rule-based annotations
    annotations = []
    for change in changes:
        added = change.get("added", [])
        for line in added:
            # Detect metadata updates
            if re.match(r"^[-*]\s*\d{4}-\d{2}-\d{2}", line):
                annotations.append({"type": "date_entry", "line": line[:80], "confidence": "high"})
            if re.match(r"^##?\s+", line):
                annotations.append({"type": "section_change", "line": line[:80], "confidence": "high"})
            # Detect entity mentions
            entities = re.findall(r"@\w+|\b[A-Z][a-z]+(?:_[A-Z][a-z]+)+\b", line)
            if entities:
                annotations.append({"type": "entity_mention", "entities": entities[:5], "line": line[:80]})

    return {"changes": changes, "annotations": annotations}

def _cleanup_snapshots(snap_dir, keep=50):
    """Remove oldest snapshots beyond keep limit."""
    if not os.path.isdir(snap_dir):
        return
    snapshots = sorted([f for f in os.listdir(snap_dir) if f.endswith(".md")])
    if len(snapshots) <= keep:
        return
    to_remove = snapshots[:-keep]
    for fname in to_remove:
        fpath = os.path.join(snap_dir, fname)
        try:
            os.unlink(fpath)
        except OSError:
            pass

def run(workspace, output_path):
    memory_path = os.path.join(workspace, "MEMORY.md")
    snap_dir = os.path.join(workspace, SNAPSHOT_DIR)
    os.makedirs(snap_dir, exist_ok=True)

    # Find latest snapshot
    snapshots = sorted([f for f in os.listdir(snap_dir) if f.endswith(".md")]) if os.path.exists(snap_dir) else []
    latest_snap = os.path.join(snap_dir, snapshots[-1]) if snapshots else None

    old_text = load_snapshot(latest_snap) if latest_snap else ""
    new_text = ""
    if os.path.exists(memory_path):
        with open(memory_path, "r", encoding="utf-8") as f:
            new_text = f.read()

    old_hash = hash_file(latest_snap) if latest_snap else None
    new_hash = hash_file(memory_path)

    if old_hash == new_hash:
        result = {"has_changes": False, "message": "No changes detected"}
    else:
        diff_result = rule_diff(old_text, new_text)
        result = {
            "has_changes": True,
            "old_snapshot": os.path.basename(latest_snap) if latest_snap else None,
            "old_hash": old_hash,
            "new_hash": new_hash,
            "diff": diff_result,
            "change_count": len(diff_result["changes"]),
            "annotation_count": len(diff_result["annotations"]),
        }

    # Save current as new snapshot only when changes detected
    if result.get("has_changes", False):
        ts = datetime.now(CST).strftime("%Y%m%d-%H%M%S")
        new_snap_path = os.path.join(snap_dir, f"{ts}.md")
        import tempfile
        fd, tmp = tempfile.mkstemp(dir=snap_dir, suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(new_text)
            os.replace(tmp, new_snap_path)
        except Exception:
            try: os.unlink(tmp)
            except OSError: pass
            raise
        result["snapshot_saved"] = os.path.basename(new_snap_path)
    else:
        result["snapshot_saved"] = None

    if output_path:
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        _atomic_save(output_path, result)
        print(f"Diff result saved to {output_path}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

    # Cleanup: keep only the latest 50 snapshots
    _cleanup_snapshots(snap_dir)

    return result

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="memory-guardian rule diff engine")
    p.add_argument("--workspace", default=None, help="Workspace path")
    p.add_argument("--output", default=None, help="Output JSON path")
    args = p.parse_args()
    workspace = args.workspace or os.environ.get("OPENCLAW_WORKSPACE", os.path.expanduser("~/workspace/agent/workspace"))
    run(workspace, args.output)
