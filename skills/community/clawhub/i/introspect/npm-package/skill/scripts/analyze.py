#!/usr/bin/env python3
"""
Introspect 🔍 — Phase 1: Data Extraction Engine

Extracts raw data from Claude Code sessions and outputs structured JSON
for Claude (the AI) to interpret and analyze in Phase 2.

This script does the BORING stuff:
- File I/O, counting, timestamps, token math
- Session filtering by date/project
- Raw metric calculation
- Picking interesting session samples for Claude to read

Claude does the SMART stuff (via SKILL.md):
- Pattern recognition, behavioral analysis, archetype assignment
- Personalized insights, shadow archetype detection
- The actual "psychology" of the report
"""

import json
import os
import sys
import argparse
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path
from collections import Counter, defaultdict

# ─── Constants ───────────────────────────────────────────────────────────────

CLAUDE_DIR = Path.home() / ".claude"
PROJECTS_DIR = CLAUDE_DIR / "projects"
HISTORY_FILE = CLAUDE_DIR / "history.jsonl"
SESSIONS_DIR = CLAUDE_DIR / "sessions"

# Signal keyword lists (used for COUNTING only — Claude interprets meaning)
#
# IMPORTANT: These are COMPOUND signals where possible. Single words like "no"
# or "run" have too many false positives. We require either multi-word phrases
# or combine single words with context checks in the analysis functions.

# Frustration: requires COMPOUND signals — "no" alone is NOT frustration
# (could be "no, I meant the other file" = correction, not frustration)
FRUSTRATION_SIGNALS_STRONG = [
    # Clearly frustrated — no ambiguity
    "that's not what", "thats not what", "not what i asked", "not what i want",
    "still not working", "still wrong", "still broken", "still not right",
    "that doesn't work", "doesnt work", "not working", "this is wrong",
    "why did you", "i said", "i already said", "i told you",
    "start over", "from scratch", "completely wrong",
    "you broke", "you deleted", "you removed", "you changed",
    "no no no", "stop stop", "what the",
]
FRUSTRATION_SIGNALS_MILD = [
    # Could be frustration OR just correction — needs context
    "try again", "nahi", "galat", "nope",
    "revert", "undo", "go back", "wrong",
    "not right", "that's not", "thats not",
]

AGREEMENT_SIGNALS = [
    "ok", "okay", "yes", "yeah", "yep", "sure", "proceed", "go ahead",
    "do it", "continue", "fine", "alright", "haan", "theek hai", "kar do",
    "ha", "hmm ok", "cool", "agreed", "right", "yup"
]

# Checkpoint questions Claude typically asks before user says "continue"
CHECKPOINT_SIGNALS = [
    "should i continue", "shall i continue", "want me to continue",
    "should i proceed", "shall i proceed", "want me to proceed",
    "do you want me to", "should i go ahead", "shall i go ahead",
    "want me to go ahead", "ready to", "move on to",
    "commit and push", "commit first", "push now",
    "does this look", "look good", "what do you think",
    "any changes", "anything else", "want to review",
    "here's what i", "here is what i", "so far i",
    "i've completed", "i have completed", "done with",
    "want me to stop", "should i stop", "pause here",
]

# Verification: tightened — "run" alone is execution, not verification
VERIFICATION_SIGNALS = [
    "run tests", "run the tests", "run test", "does it work",
    "did it work", "is it working", "check if", "verify that",
    "try it", "try running", "show me the output", "show me the result",
    "let me see", "screenshot", "does it pass", "did it pass",
    "test it", "check the output", "check output", "working?",
    "does it compile", "any errors", "is it correct",
    "self review", "self-review", "review it", "re-review",
    "cross check", "double check", "sanity check",
]

ENGAGEMENT_SIGNALS = [
    "but", "however", "what if", "instead", "why not", "i think",
    "my suggestion", "alternatively", "better if", "how about",
    "wouldn't it", "shouldn't", "consider", "actually", "disagree",
    "not sure about", "what about", "lekin", "par", "suggestion"
]

DIRECTIVE_SIGNALS = [
    "do this", "make it", "change this", "fix this", "add", "remove",
    "delete", "create", "build", "implement", "write", "update",
    "replace", "move", "copy", "rename", "install", "run this",
    "execute", "deploy", "push", "commit", "karo", "bana do", "kar do"
]

COLLABORATIVE_SIGNALS = [
    "what do you think", "what if we", "how about", "should we",
    "let's discuss", "your opinion", "suggest", "brainstorm",
    "what's the best", "which approach", "pros and cons",
    "kya lagta hai", "discuss", "explore", "consider"
]

EXPLORATORY_SIGNALS = [
    "can we", "is it possible", "how does", "what is", "explain",
    "why does", "how would", "could we", "tell me about",
    "understand", "learn", "research", "samjhao", "bata"
]


# ─── Data Loading ────────────────────────────────────────────────────────────

def load_history(days: int) -> list[dict]:
    """Load history.jsonl entries within the date range."""
    if not HISTORY_FILE.exists():
        return []

    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    cutoff_ms = cutoff.timestamp() * 1000

    entries = []
    with open(HISTORY_FILE, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                ts = obj.get("timestamp", 0)
                if isinstance(ts, (int, float)) and ts > cutoff_ms:
                    entries.append(obj)
            except json.JSONDecodeError:
                continue
    return entries


def discover_sessions(days: int, project_filter: str = "all") -> list[dict]:
    """Find all session JSONL files within date range."""
    if not PROJECTS_DIR.exists():
        return []

    cutoff = datetime.now() - timedelta(days=days)
    sessions = []

    for proj_dir in PROJECTS_DIR.iterdir():
        if not proj_dir.is_dir():
            continue

        proj_name = proj_dir.name

        if project_filter != "all":
            if project_filter.lower() not in proj_name.lower():
                continue

        for jsonl_file in proj_dir.glob("*.jsonl"):
            if "subagents" in str(jsonl_file):
                continue

            mtime = datetime.fromtimestamp(jsonl_file.stat().st_mtime)
            if mtime < cutoff:
                continue

            sessions.append({
                "path": str(jsonl_file),
                "project": proj_name,
                "session_id": jsonl_file.stem,
                "modified": mtime.isoformat(),
                "size": jsonl_file.stat().st_size
            })

    return sorted(sessions, key=lambda s: s["modified"], reverse=True)


def parse_session(session_info: dict) -> dict | None:
    """Parse a single session JSONL into structured data."""
    path = session_info["path"]

    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except Exception:
        return None

    user_messages = []
    assistant_messages = []
    tool_uses = []
    total_input_tokens = 0
    total_output_tokens = 0
    timestamps = []
    git_branches = []
    files_touched = set()

    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue

        msg_type = obj.get("type", "")
        is_meta = obj.get("isMeta", False)

        # Extract timestamp
        ts_raw = obj.get("timestamp")
        ts_dt = None
        if ts_raw:
            if isinstance(ts_raw, str):
                try:
                    ts_dt = datetime.fromisoformat(ts_raw.replace("Z", "+00:00"))
                except ValueError:
                    pass
            elif isinstance(ts_raw, (int, float)):
                ts_dt = datetime.fromtimestamp(ts_raw / 1000)
            if ts_dt:
                timestamps.append(ts_dt)

        if obj.get("gitBranch"):
            git_branches.append(obj["gitBranch"])

        if msg_type == "user" and not is_meta:
            msg = obj.get("message", {})
            content = msg.get("content", "")

            text = ""
            if isinstance(content, str):
                text = content
            elif isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        text += block.get("text", "") + " "

            text = text.strip()
            if not text:
                continue

            # Skip slash commands and XML-wrapped commands — these are UI actions,
            # not real user prompts. /clear, /status, /mcp, etc.
            # They appear as "<command-name>/clear</command-name>" or just "/clear"
            text_lower = text.lower().strip()
            is_command = (
                text_lower.startswith("<command-") or
                text_lower.startswith("/clear") or
                text_lower.startswith("/status") or
                text_lower.startswith("/mcp") or
                text_lower.startswith("/help") or
                text_lower.startswith("/config") or
                text_lower.startswith("/model") or
                text_lower.startswith("/compact") or
                text_lower.startswith("/review") or
                (text_lower.startswith("/") and len(text_lower) < 30 and " " not in text_lower.strip("/"))
            )
            if is_command:
                continue

            user_messages.append({
                "text": text,
                "timestamp": ts_dt.isoformat() if ts_dt else None,
                "char_count": len(text),
                "word_count": len(text.split()),
            })

        elif msg_type == "assistant":
            msg = obj.get("message", {})
            content = msg.get("content", [])
            usage = msg.get("usage", {})

            total_input_tokens += usage.get("input_tokens", 0)
            total_output_tokens += usage.get("output_tokens", 0)

            text = ""
            tools_in_msg = []

            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict):
                        if block.get("type") == "text":
                            text += block.get("text", "") + " "
                        elif block.get("type") == "tool_use":
                            tool_name = block.get("name", "unknown")
                            tools_in_msg.append(tool_name)
                            tool_uses.append(tool_name)
                            # Track files from tool inputs
                            tool_input = block.get("input", {})
                            if isinstance(tool_input, dict):
                                for key in ["file_path", "path", "command"]:
                                    val = tool_input.get(key, "")
                                    if val and isinstance(val, str):
                                        files_touched.add(val[:100])

            assistant_messages.append({
                "text": text.strip(),
                "tools": tools_in_msg,
                "char_count": len(text.strip()),
            })

    if not user_messages:
        return None

    # Calculate duration (capped at 4h)
    duration_minutes = 0
    if len(timestamps) >= 2:
        duration = timestamps[-1] - timestamps[0]
        duration_minutes = min(duration.total_seconds() / 60, 240)

    # Unique branches
    unique_branches = list(set(git_branches))

    return {
        "session_id": session_info["session_id"],
        "project": session_info["project"],
        "git_branches": unique_branches,
        "user_messages": user_messages,
        "assistant_messages": assistant_messages,
        "tool_uses": tool_uses,
        "files_touched": list(files_touched)[:50],
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "total_tokens": total_input_tokens + total_output_tokens,
        "duration_minutes": round(duration_minutes, 1),
        "first_timestamp": timestamps[0].isoformat() if timestamps else None,
        "last_timestamp": timestamps[-1].isoformat() if timestamps else None,
        "user_msg_count": len(user_messages),
        "assistant_msg_count": len(assistant_messages),
        "tool_call_count": len(tool_uses),
        "turn_count": len(user_messages),
    }


# ─── Metric Computation (Raw Numbers Only) ──────────────────────────────────

def contains_signal(text: str, signals: list[str]) -> bool:
    text_lower = text.lower().strip()
    for signal in signals:
        if signal in text_lower:
            return True
    return False


def compute_raw_metrics(sessions: list[dict]) -> dict:
    """Compute raw metrics — numbers only, no interpretation."""

    total_user_msgs = sum(s["user_msg_count"] for s in sessions)
    total_assistant_msgs = sum(s["assistant_msg_count"] for s in sessions)
    total_tokens = sum(s["total_tokens"] for s in sessions)
    total_tool_calls = sum(s["tool_call_count"] for s in sessions)
    total_duration = sum(s["duration_minutes"] for s in sessions)

    # Per-session stats
    turns_per_session = [s["turn_count"] for s in sessions]
    sorted_turns = sorted(turns_per_session)
    mid = len(sorted_turns) // 2
    median_turns = sorted_turns[mid] if len(sorted_turns) % 2 else (sorted_turns[mid - 1] + sorted_turns[mid]) / 2

    # Prompt length distribution
    prompt_lengths = []
    for s in sessions:
        for msg in s["user_messages"]:
            prompt_lengths.append(msg["char_count"])

    short_prompts = sum(1 for l in prompt_lengths if l < 30)
    medium_prompts = sum(1 for l in prompt_lengths if 30 <= l <= 200)
    long_prompts = sum(1 for l in prompt_lengths if 200 < l <= 500)
    mega_prompts = sum(1 for l in prompt_lengths if l > 500)

    # ─── Signal Counting (with context awareness) ─────────────────────
    frustration_strong_count = 0
    frustration_mild_count = 0
    agreement_count = 0
    blind_agreement_count = 0
    informed_checkpoint_count = 0  # NEW: "continue" in response to Claude's checkpoint
    verification_count = 0
    engagement_count = 0
    directive_count = 0
    collaborative_count = 0
    exploratory_count = 0

    for s in sessions:
        assistant_msgs = s.get("assistant_messages", [])
        for idx, msg in enumerate(s["user_messages"]):
            text = msg["text"]

            # ── Frustration: compound detection ──
            # Strong = definitely frustrated (multi-word phrases, no ambiguity)
            if contains_signal(text, FRUSTRATION_SIGNALS_STRONG):
                frustration_strong_count += 1
            # Mild = maybe frustrated, maybe just correcting
            # Only count mild if REPEATED (2+ mild signals in last 3 messages)
            elif contains_signal(text, FRUSTRATION_SIGNALS_MILD):
                # Check if previous 2 user msgs also had mild frustration
                recent_msgs = s["user_messages"][max(0, idx-2):idx]
                recent_mild = sum(1 for m in recent_msgs if contains_signal(m["text"], FRUSTRATION_SIGNALS_MILD))
                if recent_mild >= 1:
                    # Pattern of corrections = likely actual frustration
                    frustration_mild_count += 1

            # ── Verification: tightened ──
            if contains_signal(text, VERIFICATION_SIGNALS):
                verification_count += 1

            # ── Engagement ──
            if contains_signal(text, ENGAGEMENT_SIGNALS):
                engagement_count += 1

            # ── Communication style ──
            if contains_signal(text, DIRECTIVE_SIGNALS):
                directive_count += 1
            if contains_signal(text, COLLABORATIVE_SIGNALS):
                collaborative_count += 1
            if contains_signal(text, EXPLORATORY_SIGNALS):
                exploratory_count += 1

            # ── Agreement: CONTEXTUAL detection (Point A fix) ──
            text_clean = text.lower().strip().rstrip("!.,?")
            is_short_agree = len(text_clean) <= 40 and contains_signal(text_clean, AGREEMENT_SIGNALS)

            if is_short_agree:
                # Check if Claude ASKED a checkpoint question in the previous message
                prev_assistant_text = ""
                if idx > 0 and idx - 1 < len(assistant_msgs):
                    prev_assistant_text = assistant_msgs[idx - 1].get("text", "").lower()

                if contains_signal(prev_assistant_text, CHECKPOINT_SIGNALS):
                    # User replied to Claude's checkpoint = INFORMED, token-efficient
                    informed_checkpoint_count += 1
                else:
                    # Claude just outputted work, user said "ok" without context = blind
                    blind_agreement_count += 1
            elif contains_signal(text, AGREEMENT_SIGNALS):
                agreement_count += 1

    # Total frustration = strong + counted mild (mild already filtered above)
    frustration_count = frustration_strong_count + frustration_mild_count

    # ── Structured & mega prompt analysis (improved) ──
    structured_prompts = 0
    structured_mega_prompts = 0  # NEW: mega but well-structured = GOOD
    unstructured_mega_prompts = 0  # Mega wall of text = needs work
    for s in sessions:
        for msg in s["user_messages"]:
            text = msg["text"]
            has_structure = any(m in text for m in [
                "\n-", "\n*", "\n1.", "\n2.", "\n3.",
                "step 1", "step 2", "first,", "then,",
                "\n- ", "\n• ", "\n> ",
            ])
            if has_structure:
                structured_prompts += 1
            # Classify mega prompts
            if len(text) > 500:
                if has_structure:
                    structured_mega_prompts += 1
                else:
                    unstructured_mega_prompts += 1

    # Tool usage distribution
    tool_counter = Counter()
    for s in sessions:
        for tool in s["tool_uses"]:
            tool_counter[tool] += 1

    # ─── Smart Completion Detection ────────────────────────────────────
    # Categories:
    #   completed  — clear wrap-up signals (thanks, done, commit, ship)
    #   paused     — natural stop (end of day, long gap before next session, low frustration)
    #   continued  — same project session starts shortly after this one ended
    #   abandoned  — high frustration, mid-task stop, no follow-up
    completion_count = 0
    paused_count = 0
    continued_count = 0
    abandoned_count = 0

    completion_signals = ["done", "thanks", "perfect", "great", "commit", "push",
                          "ship it", "looks good", "working", "passed", "merged",
                          "nice", "awesome", "sahi hai", "badhiya", "thank",
                          "lgtm", "approved", "shipped", "deployed", "fixed"]

    # Sort sessions by timestamp for continuity detection
    sorted_sessions = sorted(sessions, key=lambda x: x.get("first_timestamp") or "")

    for idx, s in enumerate(sorted_sessions):
        if not s["user_messages"]:
            abandoned_count += 1
            continue

        last_msgs = s["user_messages"][-3:]
        has_completion = any(contains_signal(m["text"], completion_signals) for m in last_msgs)

        if has_completion:
            completion_count += 1
            continue

        # Check if next session is same project within 2 hours → "continued"
        is_continued = False
        if idx + 1 < len(sorted_sessions) and s.get("last_timestamp") and sorted_sessions[idx + 1].get("first_timestamp"):
            try:
                end_time = datetime.fromisoformat(s["last_timestamp"])
                next_start = datetime.fromisoformat(sorted_sessions[idx + 1]["first_timestamp"])
                gap_minutes = (next_start - end_time).total_seconds() / 60
                same_project = s["project"] == sorted_sessions[idx + 1]["project"]
                if same_project and 0 < gap_minutes < 120:
                    is_continued = True
            except (ValueError, TypeError):
                pass

        if is_continued:
            continued_count += 1
            continue

        # Check for natural pause signals:
        # - Session ended in evening/night (likely end of day)
        # - Low frustration in last few messages
        # - Reasonable session length (not a 2-message abandon)
        is_natural_pause = False
        if s.get("last_timestamp"):
            try:
                end_dt = datetime.fromisoformat(s["last_timestamp"])
                end_hour = end_dt.hour
                # End of day (after 6pm or before 8am) = natural pause
                if end_hour >= 18 or end_hour < 8:
                    is_natural_pause = True
            except (ValueError, TypeError):
                pass

        # Also natural if session had decent length and low frustration at end
        last_frustrations = sum(1 for m in last_msgs if contains_signal(m["text"], FRUSTRATION_SIGNALS_STRONG) or contains_signal(m["text"], FRUSTRATION_SIGNALS_MILD))
        if s["turn_count"] >= 5 and last_frustrations == 0:
            is_natural_pause = True

        if is_natural_pause:
            paused_count += 1
            continue

        # Everything else = abandoned (mid-task, high frustration, or very short)
        abandoned_count += 1

    # Repeated prompts (similar consecutive messages)
    # Repeated prompts detection (tightened)
    # Filter out common stopwords to reduce false positives
    STOPWORDS = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been",
        "this", "that", "it", "and", "or", "but", "in", "on", "at",
        "to", "for", "of", "with", "from", "by", "as", "do", "does",
        "did", "not", "no", "yes", "can", "will", "should", "would",
        "could", "have", "has", "had", "i", "you", "we", "me", "my",
        "your", "please", "also", "just", "so", "if", "then", "now",
        "like", "want", "need", "make", "let", "ok", "okay",
    }
    repeated_prompts = 0
    for s in sessions:
        prev = ""
        for msg in s["user_messages"]:
            text = msg["text"]
            if prev and len(text) > 30 and len(prev) > 30:
                # Use meaningful words only (filter stopwords)
                words_prev = set(prev.lower().split()) - STOPWORDS
                words_curr = set(text.lower().split()) - STOPWORDS
                if len(words_prev) >= 3 and len(words_curr) >= 3:
                    overlap = len(words_prev & words_curr) / max(len(words_prev), len(words_curr))
                    # Require 70% overlap on MEANINGFUL words (stricter)
                    if overlap > 0.7:
                        repeated_prompts += 1
            prev = text

    # Files touched per session
    avg_files_per_session = sum(len(s["files_touched"]) for s in sessions) / max(len(sessions), 1)
    unique_tools = len(tool_counter)
    sessions_with_tools = sum(1 for s in sessions if s["tool_call_count"] > 0)

    return {
        "totals": {
            "sessions": len(sessions),
            "user_messages": total_user_msgs,
            "assistant_messages": total_assistant_msgs,
            "tokens": total_tokens,
            "input_tokens": sum(s["total_input_tokens"] for s in sessions),
            "output_tokens": sum(s["total_output_tokens"] for s in sessions),
            "tool_calls": total_tool_calls,
            "duration_minutes": round(total_duration, 1),
        },
        "per_session": {
            "avg_turns": round(sum(turns_per_session) / max(len(turns_per_session), 1), 1),
            "median_turns": round(median_turns, 1),
            "min_turns": min(turns_per_session) if turns_per_session else 0,
            "max_turns": max(turns_per_session) if turns_per_session else 0,
            "avg_files_touched": round(avg_files_per_session, 1),
            "tokens_per_turn": round(total_tokens / max(total_user_msgs, 1)),
        },
        "prompt_distribution": {
            "short_under_30": short_prompts,
            "medium_30_200": medium_prompts,
            "long_200_500": long_prompts,
            "mega_over_500": mega_prompts,
            "mega_structured": structured_mega_prompts,
            "mega_unstructured": unstructured_mega_prompts,
            "structured": structured_prompts,
            "total": len(prompt_lengths),
            "avg_length": round(sum(prompt_lengths) / max(len(prompt_lengths), 1)),
        },
        "signals": {
            "frustration_total": frustration_count,
            "frustration_strong": frustration_strong_count,
            "frustration_mild": frustration_mild_count,
            "blind_agreement": blind_agreement_count,
            "informed_checkpoint": informed_checkpoint_count,
            "informed_agreement": agreement_count,
            "verification": verification_count,
            "engagement": engagement_count,
            "repeated_prompts": repeated_prompts,
        },
        "communication_style": {
            "directive": directive_count,
            "collaborative": collaborative_count,
            "exploratory": exploratory_count,
            "passive_blind": blind_agreement_count,
            "informed_checkpoint": informed_checkpoint_count,
            "total_classified": directive_count + collaborative_count + exploratory_count + blind_agreement_count + informed_checkpoint_count,
        },
        "tool_usage": {
            "total_calls": total_tool_calls,
            "unique_tools": unique_tools,
            "sessions_with_tools": sessions_with_tools,
            "top_tools": tool_counter.most_common(10),
        },
        "completion": {
            "completed": completion_count,
            "paused": paused_count,
            "continued": continued_count,
            "abandoned": abandoned_count,
            "completion_rate": round(completion_count / max(len(sessions), 1) * 100, 1),
            "healthy_rate": round((completion_count + paused_count + continued_count) / max(len(sessions), 1) * 100, 1),
            "true_abandon_rate": round(abandoned_count / max(len(sessions), 1) * 100, 1),
        },
    }


def compute_chrono_analysis(sessions: list[dict], history: list[dict]) -> dict:
    """Time-based analysis: when the user is most active and productive."""

    hour_counts = Counter()
    day_counts = Counter()
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # From history (more granular)
    for entry in history:
        ts = entry.get("timestamp", 0)
        if isinstance(ts, (int, float)) and ts > 0:
            dt = datetime.fromtimestamp(ts / 1000)
            hour_counts[dt.hour] += 1
            day_counts[day_names[dt.weekday()]] += 1

    # Session start times
    session_hours = Counter()
    for s in sessions:
        if s.get("first_timestamp"):
            try:
                dt = datetime.fromisoformat(s["first_timestamp"])
                session_hours[dt.hour] += 1
            except (ValueError, TypeError):
                pass

    # Time blocks
    morning = sum(hour_counts.get(h, 0) for h in range(6, 12))
    afternoon = sum(hour_counts.get(h, 0) for h in range(12, 18))
    evening = sum(hour_counts.get(h, 0) for h in range(18, 24))
    night = sum(hour_counts.get(h, 0) for h in range(0, 6))

    # Per-session: map start hour to completion/quality
    hour_to_turns = defaultdict(list)
    for s in sessions:
        if s.get("first_timestamp"):
            try:
                dt = datetime.fromisoformat(s["first_timestamp"])
                hour_to_turns[dt.hour].append(s["turn_count"])
            except (ValueError, TypeError):
                pass

    # Avg turns per time block (more turns might mean less efficient)
    block_efficiency = {}
    for block_name, hours in [("morning", range(6, 12)), ("afternoon", range(12, 18)),
                               ("evening", range(18, 24)), ("night", range(0, 6))]:
        turns = []
        for h in hours:
            turns.extend(hour_to_turns.get(h, []))
        block_efficiency[block_name] = round(sum(turns) / max(len(turns), 1), 1) if turns else None

    return {
        "time_blocks": {
            "morning_6_12": morning,
            "afternoon_12_18": afternoon,
            "evening_18_24": evening,
            "night_0_6": night,
        },
        "peak_hour": hour_counts.most_common(1)[0] if hour_counts else None,
        "day_distribution": dict(day_counts.most_common()),
        "busiest_day": day_counts.most_common(1)[0] if day_counts else None,
        "quietest_day": day_counts.most_common()[-1] if day_counts else None,
        "block_avg_turns": block_efficiency,
        "hourly_distribution": dict(sorted(hour_counts.items())),
    }


def compute_context_switching(sessions: list[dict], history: list[dict]) -> dict:
    """Analyze project/branch switching patterns."""

    # Group sessions by date
    sessions_by_date = defaultdict(list)
    for s in sessions:
        if s.get("first_timestamp"):
            try:
                dt = datetime.fromisoformat(s["first_timestamp"])
                date_key = dt.strftime("%Y-%m-%d")
                sessions_by_date[date_key].append(s)
            except (ValueError, TypeError):
                pass

    # Per-day stats
    daily_stats = []
    for date, day_sessions in sorted(sessions_by_date.items()):
        projects = set(s["project"] for s in day_sessions)
        branches = set()
        for s in day_sessions:
            branches.update(s.get("git_branches", []))

        daily_stats.append({
            "date": date,
            "session_count": len(day_sessions),
            "unique_projects": len(projects),
            "project_names": [format_project_name(p) for p in projects],
            "unique_branches": len(branches),
        })

    # Overall
    avg_projects_per_day = sum(d["unique_projects"] for d in daily_stats) / max(len(daily_stats), 1)
    most_fragmented = max(daily_stats, key=lambda d: d["unique_projects"]) if daily_stats else None
    most_focused = min(daily_stats, key=lambda d: d["unique_projects"]) if daily_stats else None

    # Longest focus streak (consecutive sessions on same project)
    longest_focus = 0
    current_streak = 0
    current_project = None
    for s in sorted(sessions, key=lambda x: x.get("first_timestamp", "")):
        if s["project"] == current_project:
            current_streak += 1
        else:
            longest_focus = max(longest_focus, current_streak)
            current_streak = 1
            current_project = s["project"]
    longest_focus = max(longest_focus, current_streak)

    return {
        "avg_projects_per_day": round(avg_projects_per_day, 1),
        "daily_stats": daily_stats,
        "most_fragmented_day": most_fragmented,
        "most_focused_day": most_focused,
        "longest_focus_streak": longest_focus,
        "total_unique_projects": len(set(s["project"] for s in sessions)),
    }


def compute_session_journey(sessions: list[dict]) -> list[dict]:
    """Compute the 'emotional arc' of each session — message patterns over time."""

    journeys = []
    for s in sessions:
        if s["user_msg_count"] < 4:
            continue

        msgs = s["user_messages"]
        total = len(msgs)

        # Split into thirds
        third = max(total // 3, 1)
        start_msgs = msgs[:third]
        mid_msgs = msgs[third:third * 2]
        end_msgs = msgs[third * 2:]

        def phase_stats(phase_msgs):
            if not phase_msgs:
                return {}
            avg_len = sum(m["char_count"] for m in phase_msgs) / len(phase_msgs)
            frustrations = sum(1 for m in phase_msgs if (
                contains_signal(m["text"], FRUSTRATION_SIGNALS_STRONG) or
                contains_signal(m["text"], FRUSTRATION_SIGNALS_MILD)
            ))
            agreements = sum(1 for m in phase_msgs if len(m["text"].strip()) <= 40 and contains_signal(m["text"], AGREEMENT_SIGNALS))
            verifications = sum(1 for m in phase_msgs if contains_signal(m["text"], VERIFICATION_SIGNALS))
            return {
                "msg_count": len(phase_msgs),
                "avg_char_length": round(avg_len),
                "frustration_signals": frustrations,
                "short_agreements": agreements,
                "verification_signals": verifications,
            }

        journeys.append({
            "session_id": s["session_id"][:8],
            "project": format_project_name(s["project"]),
            "total_turns": total,
            "start_phase": phase_stats(start_msgs),
            "mid_phase": phase_stats(mid_msgs),
            "end_phase": phase_stats(end_msgs),
        })

    return journeys


def extract_session_snippets(sessions: list[dict], max_snippets: int = 8) -> list[dict]:
    """Extract representative conversation snippets for Claude to analyze.

    Picks diverse samples: longest, shortest, most frustrated, most efficient, etc.
    Truncates messages to keep token usage reasonable.
    """

    if not sessions:
        return []

    snippets = []
    selected_ids = set()

    def add_snippet(s, reason, max_msgs=15):
        if s["session_id"] in selected_ids:
            return
        selected_ids.add(s["session_id"])

        # Get user messages (truncated)
        user_msgs = []
        for msg in s["user_messages"][:max_msgs]:
            user_msgs.append({
                "text": msg["text"][:500],  # Truncate long messages
                "timestamp": msg.get("timestamp"),
            })

        # Get first message (full, up to 800 chars) — important for goal clarity
        first_msg = s["user_messages"][0]["text"][:800] if s["user_messages"] else ""

        # Get last 3 messages (for completion detection)
        last_msgs = []
        for msg in s["user_messages"][-3:]:
            last_msgs.append(msg["text"][:300])

        # Frustration moments (full context)
        frustration_moments = []
        for i, msg in enumerate(s["user_messages"]):
            if contains_signal(msg["text"], FRUSTRATION_SIGNALS_STRONG) or contains_signal(msg["text"], FRUSTRATION_SIGNALS_MILD):
                context = {
                    "user_msg": msg["text"][:400],
                    "position": f"turn {i + 1}/{s['user_msg_count']}",
                }
                # Get the assistant response before this (if any)
                if i > 0 and i - 1 < len(s["assistant_messages"]):
                    context["assistant_before"] = s["assistant_messages"][i - 1]["text"][:300]
                # Get next user message (recovery?)
                if i + 1 < len(s["user_messages"]):
                    context["user_next"] = s["user_messages"][i + 1]["text"][:300]
                frustration_moments.append(context)
                if len(frustration_moments) >= 3:
                    break

        snippets.append({
            "session_id": s["session_id"][:8],
            "project": format_project_name(s["project"]),
            "reason": reason,
            "turn_count": s["turn_count"],
            "duration_minutes": s["duration_minutes"],
            "first_message": first_msg,
            "last_messages": last_msgs,
            "sample_messages": [m["text"] for m in user_msgs],
            "frustration_moments": frustration_moments,
            "tools_used": list(set(s["tool_uses"]))[:10],
            "total_tokens": s["total_tokens"],
        })

    # Strategy: pick diverse sessions
    sorted_by_turns = sorted(sessions, key=lambda s: s["turn_count"], reverse=True)
    sorted_by_frustration = sorted(sessions, key=lambda s: sum(
        1 for m in s["user_messages"] if contains_signal(m["text"], FRUSTRATION_SIGNALS_STRONG) or contains_signal(m["text"], FRUSTRATION_SIGNALS_MILD)
    ), reverse=True)

    # Longest session (most data)
    if sorted_by_turns:
        add_snippet(sorted_by_turns[0], "longest_session")

    # Shortest meaningful session (efficiency?)
    short = [s for s in sessions if s["turn_count"] >= 3]
    if short:
        add_snippet(min(short, key=lambda s: s["turn_count"]), "shortest_session")

    # Most frustrated session
    if sorted_by_frustration:
        add_snippet(sorted_by_frustration[0], "most_frustrated")

    # Most efficient (fewest turns, completed)
    completed = [s for s in sessions if any(
        contains_signal(m["text"], ["done", "thanks", "perfect", "great", "working", "passed"])
        for m in (s["user_messages"][-3:] if s["user_messages"] else [])
    )]
    if completed:
        add_snippet(min(completed, key=lambda s: s["turn_count"]), "most_efficient")

    # Random picks to fill remaining slots
    remaining = [s for s in sessions if s["session_id"] not in selected_ids and s["turn_count"] >= 3]
    random.shuffle(remaining)
    for s in remaining[:max_snippets - len(snippets)]:
        add_snippet(s, "random_sample")

    return snippets


def compute_scope_analysis(sessions: list[dict]) -> list[dict]:
    """Detect scope changes within sessions — did the task drift?"""
    scope_data = []

    for s in sessions:
        if s["user_msg_count"] < 5:
            continue

        # Compare first message topic vs later messages
        first_msg = s["user_messages"][0]["text"][:500]
        branches_used = s.get("git_branches", [])

        # Count REAL topic shifts — not just "also" or "next" within same task
        # "also add error handling" = same task extension (NOT a shift)
        # "btw, can you also check the CSS" = different topic (IS a shift)
        task_shifts = 0
        # Strong shift signals — clearly changing topic
        strong_shift_phrases = [
            "different thing", "new task", "switch to", "let's move to",
            "unrelated but", "separate thing", "another topic",
            "btw", "by the way", "while you're at it", "aur ek",
            "one more thing", "oh also",
        ]
        # Weak signals — only count if message is about a DIFFERENT subject
        # (we can't detect subject change perfectly, so we check if the msg
        # introduces NEW action verbs on likely different areas)
        for i, msg in enumerate(s["user_messages"][1:], 1):
            text = msg["text"].lower()
            # Strong signals — always count
            if any(phrase in text for phrase in strong_shift_phrases):
                task_shifts += 1
            # "now do X" / "next do X" only count if msg is long enough
            # to likely be a new task (not just "next" as continuation)
            elif any(phrase in text for phrase in ["now do", "now let's", "now create", "now fix"]):
                if len(text) > 60:  # Substantive enough to be a real new task
                    task_shifts += 1

        scope_data.append({
            "session_id": s["session_id"][:8],
            "project": format_project_name(s["project"]),
            "first_message_preview": first_msg[:200],
            "total_turns": s["turn_count"],
            "task_shifts_detected": task_shifts,
            "branches_used": len(branches_used),
            "files_touched": len(s.get("files_touched", [])),
        })

    return scope_data


def format_project_name(raw: str) -> str:
    """Clean up project directory name for display.

    Dynamically detects home directory components instead of hardcoding usernames.
    Handles paths encoded as dash-separated segments (Claude project dir format).
    """
    home_dir = str(Path.home())
    # Build a set of path components to skip (from actual home dir)
    # e.g., /home/john/Documents/Projects → {"home", "john", "Documents", "Projects"}
    skip_parts = set()
    for component in Path(home_dir).parts:
        skip_parts.add(component.strip("/"))

    # Common directory names that aren't meaningful project identifiers
    skip_parts.update({
        "", "Documents", "Projects", "projects", "repos", "Repos",
        "workspace", "Workspace", "dev", "Dev", "code", "Code",
        "src", "Source", "github", "GitHub", "gitlab", "GitLab",
        "work", "Work", "personal", "Personal", "Desktop", "Downloads",
    })

    # Also try to detect and skip the username-level directory
    # (e.g., "Umang" in /home/tops/Documents/Umang/Projects/)
    # Heuristic: if a part appears right after a common parent dir, skip it
    # We check: is there a path like ~/Documents/<Name>/Projects? If so, <Name> is a user dir.
    common_parents = {"Documents", "Desktop", "repos", "code", "dev", "work"}
    for parent in common_parents:
        candidate_dir = Path(home_dir) / parent
        if candidate_dir.exists():
            for child in candidate_dir.iterdir():
                if child.is_dir() and (child / "Projects").is_dir():
                    skip_parts.add(child.name)
                if child.is_dir() and (child / "projects").is_dir():
                    skip_parts.add(child.name)

    parts = raw.split("-")
    meaningful = []
    # Track if we're still in the "path prefix" zone (skip until we hit meaningful parts)
    found_meaningful = False
    for p in parts:
        if p in skip_parts:
            continue
        # Skip single-char fragments that are likely path artifacts
        if len(p) <= 1 and not found_meaningful:
            continue
        found_meaningful = True
        meaningful.append(p)
    return "/".join(meaningful) if meaningful else raw


# ─── Dreyfus Skill Model & Archetype Tier Data ──────────────────────────────

DREYFUS_LEVELS = [
    {"name": "Novice", "emoji": "🌱", "grade_range": "D (0-39)", "description": "Follows rules rigidly, needs step-by-step guidance"},
    {"name": "Advanced Beginner", "emoji": "🌿", "grade_range": "C (40-59)", "description": "Recognizes patterns, still needs structure"},
    {"name": "Competent", "emoji": "🌳", "grade_range": "B (60-74)", "description": "Plans, prioritizes, handles complexity"},
    {"name": "Proficient", "emoji": "🏔️", "grade_range": "A (75-89)", "description": "Sees the big picture, intuitive decisions"},
    {"name": "Expert", "emoji": "⭐", "grade_range": "S (90-100)", "description": "Fluid, automatic, creates reusable patterns"},
]

ARCHETYPE_TIERS = {
    "S": {
        "archetypes": ["The Sniper", "The Architect"],
        "description": "Elite — precise, structured, minimal waste"
    },
    "A": {
        "archetypes": ["The Scientist", "The Director", "The Phoenix"],
        "description": "Strong — effective collaboration, clear strengths"
    },
    "B": {
        "archetypes": ["The Sprinter", "The Philosopher"],
        "description": "Solid — gets it done, specific growth areas"
    },
    "C": {
        "archetypes": ["The Hacker", "The Bulldozer"],
        "description": "Developing — high output but costly process"
    },
    "D": {
        "archetypes": ["The Explorer"],
        "description": "Starting — still finding their style"
    },
}

ARCHETYPE_EVOLUTION_PATHS = {
    "The Explorer": {
        "current_tier": "D",
        "next_target": "The Sprinter",
        "generic_tips": [
            "Set ONE clear goal per session — write it as your first message",
            "Time-box sessions to 30 minutes max until you find your rhythm",
            "After each session, note what worked and what didn't (even mentally)"
        ]
    },
    "The Bulldozer": {
        "current_tier": "C",
        "next_target": "The Phoenix",
        "generic_tips": [
            "On retry #3 for the same thing — STOP. Ask 'why is this failing?' before trying again",
            "When frustrated, change APPROACH not just WORDING — try a different strategy entirely",
            "Keep a mental count of retries — if you hit 5 on one task, pause and re-scope"
        ]
    },
    "The Hacker": {
        "current_tier": "C",
        "next_target": "The Sprinter",
        "generic_tips": [
            "Before executing, spend 30 seconds planning — even a mental checklist helps",
            "End every session with a clean wrap-up: what was done, what's next",
            "Batch related changes instead of rapid-fire single edits"
        ]
    },
    "The Sprinter": {
        "current_tier": "B",
        "next_target": "The Sniper",
        "generic_tips": [
            "Front-load context in your first message — spend 60 extra seconds writing a richer prompt",
            "For complex tasks, resist the urge to 'just start' — a 3-line plan saves 10 turns",
            "Verify critical changes even when speed feels more important"
        ]
    },
    "The Philosopher": {
        "current_tier": "B",
        "next_target": "The Scientist",
        "generic_tips": [
            "Pair every deep discussion with a concrete action — 'let's discuss X, then implement Y'",
            "Time-box philosophical exploration: 5 turns max, then shift to execution",
            "Add verification checkpoints — after discussing, test the conclusion"
        ]
    },
    "The Scientist": {
        "current_tier": "A",
        "next_target": "The Architect",
        "generic_tips": [
            "You verify well — now plan BEFORE execution. Write a 3-step plan as first message",
            "Scale verification to complexity — quick checks for simple tasks, deep for complex",
            "Start structuring prompts with explicit expected outcomes"
        ]
    },
    "The Director": {
        "current_tier": "A",
        "next_target": "The Architect",
        "generic_tips": [
            "You delegate well — add structure by scoping sessions to 1 deliverable",
            "End sessions with explicit summaries — 'done: X, pending: Y, next: Z'",
            "Before delegating, write a brief spec — even 3 lines reduces iterations"
        ]
    },
    "The Phoenix": {
        "current_tier": "A",
        "next_target": "The Scientist",
        "generic_tips": [
            "Your resilience is rare — add systematic verification to complement your adaptability",
            "After recovering from a failure, pause to understand WHY it failed (not just fix it)",
            "Document your recovery strategies — they're reusable patterns"
        ]
    },
    "The Architect": {
        "current_tier": "S",
        "next_target": "The Sniper",
        "generic_tips": [
            "You plan well — now compress. Turn multi-step plans into precise single prompts",
            "Trust your structure enough to skip scaffolding on familiar tasks",
            "Optimize for fewer turns without losing clarity — aim for first-prompt resolution"
        ]
    },
    "The Sniper": {
        "current_tier": "S",
        "next_target": None,
        "generic_tips": [
            "You're at the top — focus on consistency across ALL task types",
            "Share your prompting patterns with others — teaching deepens mastery",
            "Experiment with Claude's newer capabilities to expand your toolset"
        ]
    },
}


def compute_dreyfus_and_tiers(raw_metrics: dict) -> dict:
    """Compute Dreyfus skill level mapping and archetype tier data.

    This provides the RAW data — Claude (via SKILL.md) does the interpretation,
    personalized tips (75-85%), and evolution path narrative.
    """

    # Map metric areas to approximate scores for Dreyfus placement
    # These are heuristic — Claude will refine with actual session analysis
    param_scores = {}

    totals = raw_metrics["totals"]
    per_session = raw_metrics["per_session"]
    prompts = raw_metrics["prompt_distribution"]
    signals = raw_metrics["signals"]
    tools = raw_metrics["tool_usage"]
    completion = raw_metrics["completion"]
    comms = raw_metrics["communication_style"]

    total_msgs = max(totals["user_messages"], 1)
    total_sessions = max(totals["sessions"], 1)

    # Clarity score
    detail_ratio = (prompts["long_200_500"] + prompts["mega_over_500"]) / max(prompts["total"], 1) * 100
    vague_ratio = prompts["short_under_30"] / max(prompts["total"], 1) * 100
    param_scores["clarity"] = min(100, max(0, int(50 + detail_ratio * 0.4 - vague_ratio * 0.3)))

    # Iteration efficiency
    avg_turns = per_session["avg_turns"]
    if avg_turns <= 5: param_scores["iteration"] = 90
    elif avg_turns <= 10: param_scores["iteration"] = 80
    elif avg_turns <= 20: param_scores["iteration"] = 65
    elif avg_turns <= 40: param_scores["iteration"] = 50
    else: param_scores["iteration"] = 35

    # Tool leverage
    tool_rate = tools["sessions_with_tools"] / total_sessions * 100
    diversity_bonus = min(20, tools["unique_tools"] * 3)
    param_scores["tool_leverage"] = min(100, int(40 + tool_rate * 0.4 + diversity_bonus))

    # Verification
    verify_rate = signals["verification"] / total_msgs * 100
    if verify_rate > 30: param_scores["verification"] = 90
    elif verify_rate > 20: param_scores["verification"] = 85
    elif verify_rate > 10: param_scores["verification"] = 70
    elif verify_rate > 5: param_scores["verification"] = 55
    else: param_scores["verification"] = 35

    # Engagement — informed checkpoints are GOOD, not blind
    engage_rate = signals["engagement"] / total_msgs * 100
    blind_rate = signals["blind_agreement"] / total_msgs * 100
    checkpoint_rate = signals.get("informed_checkpoint", 0) / total_msgs * 100
    # Informed checkpoints BOOST engagement (user is responsive to Claude's questions)
    param_scores["engagement"] = min(100, max(0, int(50 + engage_rate * 1.5 - blind_rate * 0.8 + checkpoint_rate * 0.5)))

    # Frustration recovery — only count STRONG frustration heavily
    strong_frust_rate = signals["frustration_strong"] / total_msgs * 100
    mild_frust_rate = signals["frustration_mild"] / total_msgs * 100
    repeat_rate = signals["repeated_prompts"] / total_msgs * 100
    # Strong frustration penalizes more, mild is lighter
    # Repeats penalty capped — some repetition is natural in long sessions
    capped_repeat_rate = min(repeat_rate, 20)  # Cap at 20% impact
    param_scores["frustration_recovery"] = min(100, max(0, int(85 - strong_frust_rate * 3 - mild_frust_rate * 1 - capped_repeat_rate * 1.5)))

    # NOTE: Momentum REMOVED as graded metric — completion data stays in JSON
    # for context/fun stats but doesn't affect overall score

    # Token efficiency
    tpt = per_session["tokens_per_turn"]
    if tpt < 5000: param_scores["token_efficiency"] = 90
    elif tpt < 15000: param_scores["token_efficiency"] = 80
    elif tpt < 30000: param_scores["token_efficiency"] = 65
    elif tpt < 60000: param_scores["token_efficiency"] = 50
    else: param_scores["token_efficiency"] = 35

    # Decomposition — structured mega prompts are GOOD, unstructured are bad
    unstructured_mega_ratio = prompts.get("mega_unstructured", 0) / max(prompts["total"], 1)
    structured_mega_ratio = prompts.get("mega_structured", 0) / max(prompts["total"], 1)
    struct_ratio = prompts["structured"] / max(prompts["total"], 1)
    # Penalize only UNSTRUCTURED mega prompts; reward structured ones
    param_scores["decomposition"] = min(100, max(0, int(
        70 - unstructured_mega_ratio * 60 + structured_mega_ratio * 20 + struct_ratio * 40
    )))

    # Map scores to Dreyfus levels
    def score_to_dreyfus(score: int) -> dict:
        if score >= 90: level_idx = 4  # Expert
        elif score >= 75: level_idx = 3  # Proficient
        elif score >= 60: level_idx = 2  # Competent
        elif score >= 40: level_idx = 1  # Advanced Beginner
        else: level_idx = 0  # Novice
        return {
            "score": score,
            "level": DREYFUS_LEVELS[level_idx]["name"],
            "emoji": DREYFUS_LEVELS[level_idx]["emoji"],
            "level_index": level_idx,
            "next_level": DREYFUS_LEVELS[level_idx + 1]["name"] if level_idx < 4 else None,
        }

    dreyfus_map = {param: score_to_dreyfus(score) for param, score in param_scores.items()}

    # Overall score (momentum removed — not a fair graded metric)
    weights = {
        "clarity": 1.5, "iteration": 1.2, "decomposition": 1.0,
        "tool_leverage": 0.8, "frustration_recovery": 1.0,
        "verification": 1.2, "engagement": 1.0, "token_efficiency": 0.8,
    }
    total_weight = sum(weights.values())
    overall_score = int(sum(param_scores.get(k, 50) * w for k, w in weights.items()) / total_weight)

    return {
        "param_scores": param_scores,
        "dreyfus_map": dreyfus_map,
        "dreyfus_levels_reference": DREYFUS_LEVELS,
        "overall_score": overall_score,
        "overall_dreyfus": score_to_dreyfus(overall_score),
        "archetype_tiers": ARCHETYPE_TIERS,
        "evolution_paths": ARCHETYPE_EVOLUTION_PATHS,
    }


# ─── Main Output ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Introspect 🔍 — Data Extraction Engine")
    parser.add_argument("--days", type=int, default=7, help="Days to look back")
    parser.add_argument("--sessions", type=int, default=10, help="Sessions to analyze")
    parser.add_argument("--project", type=str, default="all", help="Project filter")
    parser.add_argument("--output", type=str, default=None, help="Output directory")
    args = parser.parse_args()

    print(f"🔍 Introspect — Scanning last {args.days} days...", file=sys.stderr)

    # Discover & select sessions
    available = discover_sessions(args.days, args.project)
    print(f"📂 Found {len(available)} sessions in range", file=sys.stderr)

    if not available:
        print("❌ No sessions found.", file=sys.stderr)
        sys.exit(1)

    if len(available) > args.sessions:
        selected = random.sample(available, args.sessions)
        print(f"🎲 Randomly selected {args.sessions} sessions", file=sys.stderr)
    else:
        selected = available
        print(f"📋 Analyzing all {len(selected)} sessions", file=sys.stderr)

    # Parse sessions
    parsed = []
    for s in selected:
        result = parse_session(s)
        if result and result["user_msg_count"] > 0:
            parsed.append(result)

    print(f"✅ Parsed {len(parsed)} sessions", file=sys.stderr)

    if not parsed:
        print("❌ No valid sessions found.", file=sys.stderr)
        sys.exit(1)

    # Load history
    history = load_history(args.days)

    # Compute everything
    raw_metrics = compute_raw_metrics(parsed)
    chrono = compute_chrono_analysis(parsed, history)
    context_switching = compute_context_switching(parsed, history)
    journeys = compute_session_journey(parsed)
    snippets = extract_session_snippets(parsed, max_snippets=8)
    scope = compute_scope_analysis(parsed)

    # Dreyfus & tier analysis
    dreyfus_data = compute_dreyfus_and_tiers(raw_metrics)

    # Project distribution
    project_counts = Counter(format_project_name(s["project"]) for s in parsed)

    # Build final output
    output = {
        "_meta": {
            "generated_at": datetime.now().isoformat(),
            "days_scanned": args.days,
            "sessions_analyzed": len(parsed),
            "project_filter": args.project,
            "date_range": {
                "from": (datetime.now() - timedelta(days=args.days)).strftime("%Y-%m-%d"),
                "to": datetime.now().strftime("%Y-%m-%d"),
            },
        },
        "raw_metrics": raw_metrics,
        "dreyfus_and_tiers": dreyfus_data,
        "chrono_analysis": chrono,
        "context_switching": context_switching,
        "session_journeys": journeys,
        "scope_analysis": scope,
        "project_distribution": dict(project_counts.most_common()),
        "session_snippets": snippets,
    }

    # Save
    output_dir = args.output or str(Path.home() / ".claude" / "skills" / "introspect" / "reports")
    os.makedirs(output_dir, exist_ok=True)

    filename = f"introspect-data-{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.json"
    output_path = os.path.join(output_dir, filename)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, default=str)

    print(f"📄 Data saved: {output_path}", file=sys.stderr)

    # Also print to stdout for Claude to read directly
    print(json.dumps(output, indent=2, default=str))


if __name__ == "__main__":
    main()
