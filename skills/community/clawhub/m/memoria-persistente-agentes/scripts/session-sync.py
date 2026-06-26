#!/usr/bin/env python3
"""Session sync: index all sessions and promote cross-session context.

Reads OpenClaw session transcripts, extracts key topics, and writes
a shared index that any session can consult.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# Force UTF-8 on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def find_sessions_dir(workspace: Path) -> Path:
    """Find the OpenClaw sessions directory."""
    # Check common locations
    candidates = [
        workspace / ".openclaw" / "agents" / "main" / "sessions",
        Path.home() / ".openclaw" / "agents" / "main" / "sessions",
    ]

    # Check OPENCLAW_STATE_DIR
    state_dir = os.environ.get("OPENCLAW_STATE_DIR")
    if state_dir:
        candidates.insert(0, Path(state_dir) / "agents" / "main" / "sessions")

    for candidate in candidates:
        if candidate.exists():
            return candidate

    return candidates[-1]  # Return last as default


def read_session_index(sessions_dir: Path) -> dict:
    """Read sessions.json to get session metadata."""
    index_path = sessions_dir / "sessions.json"
    if not index_path.exists():
        return {}

    try:
        with open(index_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def extract_session_topics(transcript_path: Path, max_lines: int = 200) -> list[str]:
    """Extract key topics from a session transcript."""
    topics = set()

    try:
        with open(transcript_path, "r", encoding="utf-8", errors="replace") as f:
            for i, line in enumerate(f):
                if i >= max_lines:
                    break
                try:
                    msg = json.loads(line)
                except json.JSONDecodeError:
                    continue

                message = msg.get("message", {})
                content = message.get("content", "")
                if isinstance(content, list):
                    texts = [c.get("text", "") for c in content if c.get("type") == "text"]
                    content = " ".join(texts)
                elif not isinstance(content, str):
                    continue

                # Extract topics from text
                topic_patterns = [
                    r"(?:proyecto|project)\s+[\w\-]+",
                    r"(?:letta|memoria|memory|archival|core)",
                    r"(?:openclaw|gateway|telegram|bot)",
                    r"(?:cobranza|billing|pago|invoice)",
                    r"(?:falclaw|pezuño|maestro)",
                    r"(?:locatering|cholitas)",
                    r"(?:vps|server|deploy|config)",
                    r"(?:oauth|gmail|calendar|drive|gog)",
                ]

                for pattern in topic_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    for m in matches:
                        topics.add(m.strip().lower())

    except OSError:
        pass

    return sorted(topics)


def build_index(sessions_dir: Path, workspace: Path) -> list[dict]:
    """Build a session index with topics."""
    sessions_meta = read_session_index(sessions_dir)
    index = []

    for session_key, meta in sessions_meta.items():
        session_id = meta.get("sessionId", "")
        if not session_id:
            continue

        # Find transcript file
        transcript_pattern = f"{session_id}*.jsonl"
        transcript_files = list(sessions_dir.glob(transcript_pattern))

        if not transcript_files:
            continue

        # Skip the main transcript (use the .jsonl, not trajectory)
        transcript = None
        for tf in transcript_files:
            if tf.suffix == ".jsonl" and "trajectory" not in tf.name:
                transcript = tf
                break

        if not transcript:
            continue

        channel = meta.get("lastChannel", "unknown")
        to = meta.get("deliveryContext", {}).get("to", "unknown")
        updated = meta.get("updatedAt", 0)

        # Extract topics
        topics = extract_session_topics(transcript)

        # Simple channel label
        if "telegram" in str(to):
            if "group" in session_key:
                channel_label = "telegram:group"
            else:
                channel_label = "telegram:dm"
        elif "webchat" in channel or "tui" in session_key:
            channel_label = "tui"
        elif "cron" in session_key:
            channel_label = "cron"
        else:
            channel_label = channel

        entry = {
            "session": session_key,
            "channel": channel_label,
            "updated": datetime.fromtimestamp(updated / 1000).isoformat() if updated else "unknown",
            "topics": topics[:10],  # Limit to 10 topics
        }

        index.append(entry)

    # Sort by most recent
    index.sort(key=lambda x: x.get("updated", ""), reverse=True)

    return index


def write_index(workspace: Path, index: list[dict], dry_run: bool = False) -> str:
    """Write the session index to a file."""
    index_dir = workspace / "memory" / "archival"
    index_dir.mkdir(parents=True, exist_ok=True)
    index_path = index_dir / "session-index.json"

    if dry_run:
        return f"[DRY RUN] Would write {len(index)} sessions to {index_path}"

    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    return f"Wrote {len(index)} sessions to {index_path}"


def main():
    parser = argparse.ArgumentParser(description="Sync session context into shared index")
    parser.add_argument("--workspace", type=str, default=".", help="Workspace root path")
    parser.add_argument("--dry-run", action="store_true", help="Show without writing")

    args = parser.parse_args()
    workspace = Path(args.workspace).resolve()
    sessions_dir = find_sessions_dir(workspace)

    if not sessions_dir.exists():
        print(f"Sessions directory not found: {sessions_dir}")
        sys.exit(1)

    index = build_index(sessions_dir, workspace)
    result = write_index(workspace, index, args.dry_run)
    print(result)

    # Also print a summary
    for entry in index[:10]:
        topics_str = ", ".join(entry["topics"][:5]) if entry["topics"] else "(no topics)"
        print(f"  {entry['channel']:15} | {entry['updated'][:10]} | {topics_str}")


if __name__ == "__main__":
    main()