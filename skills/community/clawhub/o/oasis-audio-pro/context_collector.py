#!/usr/bin/env python3

import argparse
import datetime
import json
import os
import re
import sys
from pathlib import Path

import debug_utils

# Regex to strip "Sender (untrusted metadata):\n```json\n{...}\n```\n" prefix
SENDER_PREFIX_RE = re.compile(
    r"^Sender\s*\(untrusted metadata\)\s*:\s*```(?:json)?\s*\{.*?\}\s*```\s*",
    re.DOTALL,
)

# Regex to strip "[Mon 2026-03-30 15:35 GMT+8]" timestamp prefix
TIMESTAMP_PREFIX_RE = re.compile(r"^\[.*?\]\s*")

# Max file size to read fully (2MB). For larger files, read only the tail.
MAX_FILE_SIZE = 2 * 1024 * 1024

TOOL_PATHS = {
    "qclaw": {
        "sessions_dir": "~/.qclaw/agents/main/sessions",
        "memory_dir": "~/.qclaw/workspace/memory",
        "user_md": "~/.qclaw/workspace/USER.md",
    },
    "openclaw": {
        "sessions_dir": "~/.openclaw/agents/main/sessions",
        "memory_dir": "~/.openclaw/workspace/memory",
        "user_md": "~/.openclaw/workspace/USER.md",
    },
}


def get_paths(source_tool):
    """Return resolved paths dict for the given tool."""
    raw = TOOL_PATHS[source_tool]
    return {k: Path(v).expanduser() for k, v in raw.items()}


def find_recent_sessions(sessions_dir, days):
    """Find .jsonl files modified within the time window, newest first.
    Excludes deleted/reset session files."""
    if not sessions_dir.exists():
        debug_utils.debug_print(f"Sessions dir not found: {sessions_dir}")
        return []

    cutoff = datetime.datetime.now().timestamp() - days * 86400
    sessions = []

    for f in sessions_dir.iterdir():
        if not f.name.endswith(".jsonl"):
            continue
        # Skip deleted/reset files like *.jsonl.deleted.* or *.jsonl.reset.*
        if ".deleted." in f.name or ".reset." in f.name:
            continue
        # Skip lock files
        if f.name.endswith(".lock"):
            continue
        try:
            mtime = f.stat().st_mtime
            if mtime >= cutoff:
                sessions.append((mtime, f))
        except OSError:
            continue

    sessions.sort(key=lambda x: x[0], reverse=True)
    debug_utils.debug_print(f"Found {len(sessions)} recent sessions in {sessions_dir}")
    return [f for _, f in sessions]


def clean_user_text(text):
    """Strip sender metadata prefix and timestamp prefix from user message text."""
    text = SENDER_PREFIX_RE.sub("", text)
    text = TIMESTAMP_PREFIX_RE.sub("", text)
    return text.strip()


def parse_session_messages(session_path):
    """Parse a JSONL session file, return (session_id, list of message dicts).
    Each message dict: {timestamp, role, text, id}"""
    session_id = ""
    messages = []
    file_size = session_path.stat().st_size

    try:
        with open(session_path, "r", encoding="utf-8") as f:
            # For large files, seek to tail
            if file_size > MAX_FILE_SIZE:
                debug_utils.debug_print(
                    f"Large file ({file_size} bytes), reading tail: {session_path.name}"
                )
                f.seek(file_size - MAX_FILE_SIZE)
                f.readline()  # Skip partial first line

            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue

                obj_type = obj.get("type")

                if obj_type == "session":
                    session_id = obj.get("id", "")
                    continue

                if obj_type != "message":
                    continue

                msg = obj.get("message", {})
                role = msg.get("role", "")
                if role not in ("user", "assistant"):
                    continue

                # Extract text from content array
                content = msg.get("content", [])
                if isinstance(content, str):
                    text = content
                elif isinstance(content, list):
                    text_parts = []
                    for item in content:
                        if isinstance(item, dict) and item.get("type") == "text":
                            text_parts.append(item.get("text", ""))
                    text = "\n".join(text_parts)
                else:
                    continue

                if not text.strip():
                    continue

                # Clean user messages
                if role == "user":
                    text = clean_user_text(text)

                if not text.strip():
                    continue

                messages.append(
                    {
                        "timestamp": obj.get("timestamp", ""),
                        "role": role,
                        "text": text.strip(),
                        "id": obj.get("id", ""),
                    }
                )
    except (OSError, UnicodeDecodeError) as e:
        debug_utils.debug_print(f"Error reading {session_path}: {e}")

    return session_id, messages


def compile_keyword_patterns(keywords):
    """Compile keyword patterns. Chinese uses substring match, ASCII uses word boundary."""
    patterns = []
    for kw in keywords:
        if kw.isascii():
            patterns.append(re.compile(r"\b" + re.escape(kw) + r"\b", re.IGNORECASE))
        else:
            patterns.append(re.compile(re.escape(kw), re.IGNORECASE))
    return patterns


def match_keywords(messages, patterns):
    """Return indices of user messages matching any keyword pattern."""
    indices = []
    for i, msg in enumerate(messages):
        if msg["role"] != "user":
            continue
        for pat in patterns:
            if pat.search(msg["text"]):
                indices.append(i)
                break
    return indices


def extract_fragments(messages, match_indices, session_id):
    """Extract matched messages with 1 message before/after as context.
    Deduplicates overlapping context windows."""
    if not match_indices:
        return []

    # Merge overlapping ranges
    ranges = []
    for idx in match_indices:
        start = max(0, idx - 1)
        end = min(len(messages) - 1, idx + 1)
        if ranges and start <= ranges[-1][1] + 1:
            ranges[-1] = (ranges[-1][0], end)
        else:
            ranges.append((start, end))

    fragments = []
    for start, end in ranges:
        for i in range(start, end + 1):
            msg = messages[i]
            # Find context
            ctx_before = messages[i - 1]["text"] if i > 0 else ""
            ctx_after = messages[i + 1]["text"] if i < len(messages) - 1 else ""

            # Only include the actual matched user messages as fragments
            if msg["role"] == "user" and i in match_indices:
                fragments.append(
                    {
                        "timestamp": msg["timestamp"],
                        "role": msg["role"],
                        "text": msg["text"],
                        "session_id": session_id,
                        "context_before": ctx_before[:500],  # Truncate long context
                        "context_after": ctx_after[:500],
                    }
                )

    return fragments


def load_daily_memories(memory_dir, days):
    """Read YYYY-MM-DD.md files within the time window."""
    if not memory_dir.exists():
        debug_utils.debug_print(f"Memory dir not found: {memory_dir}")
        return []

    cutoff_date = datetime.date.today() - datetime.timedelta(days=days)
    memories = []

    for f in sorted(memory_dir.iterdir(), reverse=True):
        if not f.name.endswith(".md"):
            continue
        # Parse date from filename
        date_str = f.stem
        try:
            file_date = datetime.date.fromisoformat(date_str)
        except ValueError:
            continue

        if file_date < cutoff_date:
            continue

        try:
            content = f.read_text(encoding="utf-8").strip()
            if content:
                memories.append({"date": date_str, "content": content})
        except (OSError, UnicodeDecodeError):
            continue

    return memories


def load_user_profile(user_md_path):
    """Read USER.md and extract only structured fields (name, MBTI, interests).

    Returns a dict with extracted fields instead of raw file content,
    to minimize the risk of sensitive personal data leaking into prompts.
    """
    result = {"name": "", "mbti": "", "interests": [], "notes": ""}

    if not user_md_path.exists():
        return result
    try:
        text = user_md_path.read_text(encoding="utf-8").strip()
    except (OSError, UnicodeDecodeError):
        return result

    if not text:
        return result

    # Extract structured fields via common patterns
    for line in text.splitlines():
        line_stripped = line.strip()
        lower = line_stripped.lower()

        # Name: value / 名字: value
        if re.match(r"^(?:name|名字|昵称|称呼)\s*[:：]\s*", lower):
            result["name"] = re.split(r"[:：]\s*", line_stripped, maxsplit=1)[-1].strip()
        # MBTI / personality
        elif re.match(r"^(?:mbti|personality|人格|性格)\s*[:：]\s*", lower):
            result["mbti"] = re.split(r"[:：]\s*", line_stripped, maxsplit=1)[-1].strip()
        # Interests / hobbies
        elif re.match(r"^(?:interests?|hobbies?|兴趣|爱好)\s*[:：]\s*", lower):
            raw = re.split(r"[:：]\s*", line_stripped, maxsplit=1)[-1].strip()
            result["interests"] = [i.strip() for i in re.split(r"[,，、;；]", raw) if i.strip()]
        # Notes / preferences
        elif re.match(r"^(?:notes?|preferences?|备注|偏好)\s*[:：]\s*", lower):
            result["notes"] = re.split(r"[:：]\s*", line_stripped, maxsplit=1)[-1].strip()

    debug_utils.debug_print(f"Extracted user profile fields: {list(k for k, v in result.items() if v)}")
    return result


def collect_context(source_tool, keywords_str, days, max_results):
    """Main orchestration: search sessions, memories, and user profile."""
    keywords = [k.strip() for k in keywords_str.split(",") if k.strip()]
    if not keywords:
        debug_utils.debug_print("No keywords provided")
        return {
            "source_tool": source_tool,
            "fragments": [],
            "daily_memories": [],
            "user_profile": {"name": "", "mbti": "", "interests": [], "notes": ""},
        }

    paths = get_paths(source_tool)
    patterns = compile_keyword_patterns(keywords)

    # Search session files
    all_fragments = []
    sessions = find_recent_sessions(paths["sessions_dir"], days)

    for session_path in sessions:
        debug_utils.debug_print(f"Scanning session: {session_path.name}")
        session_id, messages = parse_session_messages(session_path)
        indices = match_keywords(messages, patterns)

        if indices:
            debug_utils.debug_print(
                f"  Found {len(indices)} matches in {session_path.name}"
            )
            frags = extract_fragments(messages, indices, session_id)
            all_fragments.extend(frags)

        # Early stop if we have enough
        if len(all_fragments) >= max_results:
            debug_utils.debug_print(f"Reached max_results ({max_results}), stopping")
            break

    # Sort by timestamp descending, limit
    all_fragments.sort(key=lambda f: f["timestamp"], reverse=True)
    all_fragments = all_fragments[:max_results]

    # Load supplementary data
    daily_memories = load_daily_memories(paths["memory_dir"], days)
    user_profile = load_user_profile(paths["user_md"])

    return {
        "source_tool": source_tool,
        "fragments": all_fragments,
        "daily_memories": daily_memories,
        "user_profile": user_profile,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Collect personalized context from OpenClaw conversation history"
    )
    parser.add_argument(
        "--source-tool",
        required=True,
        choices=["qclaw", "openclaw"],
        help="Which tool's history to search",
    )
    parser.add_argument(
        "--keywords",
        required=True,
        help="Comma-separated search keywords (all layers)",
    )
    parser.add_argument(
        "--days", type=int, required=True, help="Time window in days (3-30)"
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=20,
        help="Maximum fragments to return (default 20)",
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Enable debug output"
    )

    args = parser.parse_args()
    debug_utils.set_debug(args.debug)

    result = collect_context(args.source_tool, args.keywords, args.days, args.max_results)
    output = json.dumps(result, ensure_ascii=False, indent=2)
    # Replace unpaired surrogates (from emoji in session files) with U+FFFD
    output = output.encode("utf-8", errors="replace").decode("utf-8")
    print(output)


if __name__ == "__main__":
    main()
