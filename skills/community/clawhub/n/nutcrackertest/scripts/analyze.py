#!/usr/bin/env python3
"""
analyze.py — Ethnographic analysis engine for UXR Observer.

Reads redacted session data (JSON from collect.sh | redact.py) and produces
a structured analysis object covering:
  - Task taxonomy
  - Interaction patterns
  - Friction signals
  - Delight signals
  - Behavioral archetypes
  - Verbatim quotes
  - Tool/skill usage stats

Usage:
  python3 analyze.py --input <collected_data.json> [--trends <trends.json>]

Outputs analysis JSON to stdout.
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime


# =============================================================================
# Task Taxonomy — keyword-based classification
# =============================================================================

TASK_CATEGORIES = {
    "coding": {
        "keywords": [
            "code", "function", "class", "variable", "bug", "error", "debug",
            "refactor", "implement", "compile", "build", "test", "commit", "git",
            "pull request", "merge", "branch", "deploy", "api", "endpoint",
            "database", "query", "sql", "schema", "migration", "frontend",
            "backend", "component", "module", "package", "dependency",
            "typescript", "python", "javascript", "rust", "go ", "java",
            "react", "vue", "angular", "node", "docker", "kubernetes",
            "lint", "format", "prettier", "eslint", "pytest", "jest",
        ],
        "weight": 1.0,
    },
    "research": {
        "keywords": [
            "research", "find", "search", "look up", "what is", "how does",
            "explain", "learn", "understand", "documentation", "docs", "wiki",
            "article", "paper", "compare", "difference between", "pros and cons",
            "best practice", "recommend", "suggest", "alternative",
        ],
        "weight": 0.9,
    },
    "writing": {
        "keywords": [
            "write", "draft", "edit", "proofread", "rewrite", "summarize",
            "blog", "article", "email", "message", "letter", "report",
            "documentation", "readme", "changelog", "copy", "content",
            "paragraph", "sentence", "tone", "grammar",
        ],
        "weight": 0.9,
    },
    "communication": {
        "keywords": [
            "email", "slack", "message", "reply", "respond", "notify",
            "meeting", "agenda", "notes", "follow up", "introduce",
            "thank", "apolog", "announce", "present",
        ],
        "weight": 0.8,
    },
    "automation": {
        "keywords": [
            "automate", "script", "cron", "schedule", "batch", "pipeline",
            "workflow", "hook", "trigger", "webhook", "ci/cd", "github action",
            "makefile", "task runner",
        ],
        "weight": 0.85,
    },
    "creative": {
        "keywords": [
            "design", "create", "generate", "brainstorm", "idea", "concept",
            "prototype", "mockup", "wireframe", "logo", "image", "illustration",
            "story", "poem", "name", "brand", "tagline", "slogan",
        ],
        "weight": 0.85,
    },
    "sysadmin": {
        "keywords": [
            "server", "ssh", "chmod", "chown", "sudo", "systemctl", "service",
            "nginx", "apache", "dns", "ssl", "certificate", "firewall",
            "backup", "restore", "monitor", "disk", "memory", "cpu",
            "install", "update", "upgrade", "config", "env", "environment",
        ],
        "weight": 0.8,
    },
    "data_analysis": {
        "keywords": [
            "data", "csv", "json", "parse", "transform", "aggregate",
            "chart", "graph", "plot", "visualization", "statistics",
            "average", "median", "count", "filter", "sort", "group by",
            "pandas", "numpy", "excel", "spreadsheet",
        ],
        "weight": 0.85,
    },
}


def classify_task(text: str) -> dict:
    """Classify a user message into task categories with confidence scores."""
    text_lower = text.lower()
    scores = {}

    for category, config in TASK_CATEGORIES.items():
        hit_count = sum(1 for kw in config["keywords"] if kw in text_lower)
        if hit_count > 0:
            # Normalize: more keyword hits = higher confidence, capped at 1.0
            raw_score = min(hit_count / 3.0, 1.0) * config["weight"]
            scores[category] = round(raw_score, 3)

    if not scores:
        scores["uncategorized"] = 0.5

    return scores


# =============================================================================
# Friction Signal Detection
# =============================================================================

FRICTION_PATTERNS = {
    "rephrasing": {
        "description": "User rephrased or repeated a similar request",
        "severity": 3,
    },
    "error_recovery": {
        "description": "Error followed by retry or manual fallback",
        "severity": 4,
    },
    "abandonment": {
        "description": "Task appears to have been abandoned mid-conversation",
        "severity": 4,
    },
    "confusion": {
        "description": "User expressed confusion or misunderstanding",
        "severity": 3,
    },
    "long_session_simple_task": {
        "description": "Unusually long session for a seemingly simple task",
        "severity": 2,
    },
    "tool_failure": {
        "description": "Tool call failed, requiring workaround",
        "severity": 4,
    },
    "correction": {
        "description": "User corrected the agent's output",
        "severity": 3,
    },
}

CONFUSION_PHRASES = [
    "i don't understand", "that's not what i", "no, i meant", "i said",
    "wrong", "incorrect", "that's not right", "not what i asked",
    "confused", "what do you mean", "try again", "let me rephrase",
    "that doesn't work", "still not", "you misunderstood",
    "can you re-read", "re-read", "look again",
]

CORRECTION_PHRASES = [
    "no,", "actually,", "i meant", "that's wrong", "not quite",
    "close, but", "almost, but", "instead,", "what i wanted was",
    "let me clarify", "to clarify", "correction:",
]

POSITIVE_PHRASES = [
    "thank", "thanks", "perfect", "great", "awesome", "excellent",
    "exactly", "that's it", "love it", "well done", "nice",
    "beautiful", "impressive", "amazing", "wonderful", "fantastic",
    "this is great", "you nailed", "spot on", "just what i needed",
    "this works", "it works", "looks good",
]

FRUSTRATION_PHRASES = [
    "ugh", "frustrat", "annoying", "why can't", "why won't",
    "this is broken", "doesn't work", "stop", "forget it",
    "never mind", "nevermind", "give up", "too complicated",
    "waste of time", "useless",
]


def detect_friction(sessions: list) -> list:
    """Analyze sessions for friction signals."""
    friction_log = []

    for session in sessions:
        messages = session.get("messages", [])
        user_messages = [m for m in messages if m.get("role") == "user"]
        tool_calls = session.get("tool_calls", [])

        # Check for rephrasing: similar consecutive user messages
        for i in range(1, len(user_messages)):
            curr = user_messages[i].get("text", "").lower().strip()
            prev = user_messages[i - 1].get("text", "").lower().strip()
            if not curr or not prev:
                continue

            # Simple similarity: shared word ratio
            curr_words = set(curr.split())
            prev_words = set(prev.split())
            if len(curr_words) > 2 and len(prev_words) > 2:
                overlap = len(curr_words & prev_words)
                max_len = max(len(curr_words), len(prev_words))
                similarity = overlap / max_len if max_len > 0 else 0
                if similarity > 0.5 and similarity < 0.95:  # Similar but not identical
                    friction_log.append({
                        "type": "rephrasing",
                        "severity": FRICTION_PATTERNS["rephrasing"]["severity"],
                        "description": FRICTION_PATTERNS["rephrasing"]["description"],
                        "context": f"User rephrased: '{curr[:100]}...'",
                        "timestamp": user_messages[i].get("timestamp", ""),
                        "session_file": session.get("file", ""),
                    })

        # Check for confusion/correction phrases in user messages
        for msg in user_messages:
            text_lower = msg.get("text", "").lower()

            for phrase in CONFUSION_PHRASES:
                if phrase in text_lower:
                    friction_log.append({
                        "type": "confusion",
                        "severity": FRICTION_PATTERNS["confusion"]["severity"],
                        "description": FRICTION_PATTERNS["confusion"]["description"],
                        "context": f"User said: '{msg.get('text', '')[:150]}'",
                        "timestamp": msg.get("timestamp", ""),
                        "session_file": session.get("file", ""),
                    })
                    break

            for phrase in CORRECTION_PHRASES:
                if text_lower.startswith(phrase) or f". {phrase}" in text_lower:
                    friction_log.append({
                        "type": "correction",
                        "severity": FRICTION_PATTERNS["correction"]["severity"],
                        "description": FRICTION_PATTERNS["correction"]["description"],
                        "context": f"User corrected: '{msg.get('text', '')[:150]}'",
                        "timestamp": msg.get("timestamp", ""),
                        "session_file": session.get("file", ""),
                    })
                    break

        # Check for tool failures
        failed_tools = [t for t in tool_calls if not t.get("success", True)]
        if failed_tools:
            friction_log.append({
                "type": "tool_failure",
                "severity": FRICTION_PATTERNS["tool_failure"]["severity"],
                "description": FRICTION_PATTERNS["tool_failure"]["description"],
                "context": f"{len(failed_tools)} tool call(s) failed in session",
                "timestamp": failed_tools[0].get("timestamp", ""),
                "session_file": session.get("file", ""),
            })

        # Check for abandonment: session ends with user message (no assistant response after)
        if messages and messages[-1].get("role") == "user":
            last_text = messages[-1].get("text", "").lower()
            # Only flag if it doesn't look like a closing remark or positive signal
            if not any(p in last_text for p in ["thank", "bye", "done", "ok", "got it", "perfect", "great", "exactly", "awesome", "nice", "love it", "works"]):
                friction_log.append({
                    "type": "abandonment",
                    "severity": FRICTION_PATTERNS["abandonment"]["severity"],
                    "description": FRICTION_PATTERNS["abandonment"]["description"],
                    "context": f"Session ended on user message: '{messages[-1].get('text', '')[:100]}'",
                    "timestamp": messages[-1].get("timestamp", ""),
                    "session_file": session.get("file", ""),
                })

        # Check for long sessions with simple tasks
        duration = session.get("duration_seconds", 0)
        if duration > 1800 and session.get("user_message_count", 0) <= 3:
            friction_log.append({
                "type": "long_session_simple_task",
                "severity": FRICTION_PATTERNS["long_session_simple_task"]["severity"],
                "description": FRICTION_PATTERNS["long_session_simple_task"]["description"],
                "context": f"Session lasted {duration // 60} minutes with only {session.get('user_message_count', 0)} user messages",
                "timestamp": session.get("session_start", ""),
                "session_file": session.get("file", ""),
            })

    # Sort by severity descending
    friction_log.sort(key=lambda x: x.get("severity", 0), reverse=True)
    return friction_log


# =============================================================================
# Delight Signal Detection
# =============================================================================

def detect_delight(sessions: list) -> list:
    """Analyze sessions for delight signals."""
    delight_log = []

    for session in sessions:
        messages = session.get("messages", [])
        user_messages = [m for m in messages if m.get("role") == "user"]

        for msg in user_messages:
            text_lower = msg.get("text", "").lower()

            for phrase in POSITIVE_PHRASES:
                if phrase in text_lower:
                    delight_log.append({
                        "type": "positive_acknowledgment",
                        "context": f"User said: '{msg.get('text', '')[:150]}'",
                        "timestamp": msg.get("timestamp", ""),
                        "session_file": session.get("file", ""),
                    })
                    break

        # Rapid task completion: few turns, short duration, no friction
        duration = session.get("duration_seconds", 0)
        msg_count = session.get("message_count", 0)
        if 0 < duration < 120 and 2 <= msg_count <= 6:
            delight_log.append({
                "type": "rapid_completion",
                "context": f"Task completed in {duration:.0f}s with {msg_count} messages",
                "timestamp": session.get("session_start", ""),
                "session_file": session.get("file", ""),
            })

        # User building on previous output: "now" / "also" / "and then" / "next"
        building_phrases = ["now ", "also ", "and then ", "next,", "next ", "building on", "extending"]
        building_count = sum(
            1 for m in user_messages
            if any(m.get("text", "").lower().startswith(p) for p in building_phrases)
        )
        if building_count >= 2:
            delight_log.append({
                "type": "building_on_output",
                "context": f"User built on agent output {building_count} times in session",
                "timestamp": session.get("session_start", ""),
                "session_file": session.get("file", ""),
            })

    return delight_log


# =============================================================================
# Verbatim Quote Extraction
# =============================================================================

def extract_quotes(sessions: list, max_quotes: int = 10) -> list:
    """Extract notable user quotes that reveal intent, frustration, or satisfaction."""
    quotes = []

    # Phrases that signal quote-worthy content
    signal_phrases = (
        POSITIVE_PHRASES + FRUSTRATION_PHRASES + CONFUSION_PHRASES +
        ["i wish", "i want", "i need", "it would be nice", "can you",
         "i always", "i never", "every time", "i usually", "my workflow"]
    )

    for session in sessions:
        messages = session.get("messages", [])
        user_messages = [m for m in messages if m.get("role") == "user"]

        for msg in user_messages:
            text = msg.get("text", "")
            text_lower = text.lower()

            if len(text) < 10 or len(text) > 500:
                continue

            # Score the quote by how many signal phrases it contains
            signal_score = sum(1 for p in signal_phrases if p in text_lower)

            if signal_score > 0:
                # Determine sentiment
                sentiment = "neutral"
                if any(p in text_lower for p in POSITIVE_PHRASES):
                    sentiment = "positive"
                elif any(p in text_lower for p in FRUSTRATION_PHRASES):
                    sentiment = "frustration"
                elif any(p in text_lower for p in CONFUSION_PHRASES):
                    sentiment = "confusion"

                quotes.append({
                    "text": text[:300],
                    "sentiment": sentiment,
                    "signal_score": signal_score,
                    "timestamp": msg.get("timestamp", ""),
                    "session_file": session.get("file", ""),
                })

    # Sort by signal score descending, take top N
    quotes.sort(key=lambda q: q["signal_score"], reverse=True)
    return quotes[:max_quotes]


# =============================================================================
# Interaction Pattern Detection
# =============================================================================

def detect_patterns(sessions: list) -> dict:
    """Detect recurring interaction patterns across sessions."""
    patterns = {
        "desire_paths": [],
        "workarounds": [],
        "conversation_depth": {
            "single_turn": 0,
            "short": 0,       # 2-5 turns
            "medium": 0,      # 6-15 turns
            "deep": 0,        # 16+ turns
        },
        "session_timing": {
            "hours": Counter(),
        },
        "average_messages_per_session": 0,
    }

    total_messages = 0

    for session in sessions:
        msg_count = session.get("user_message_count", 0)
        total_messages += session.get("message_count", 0)

        if msg_count <= 1:
            patterns["conversation_depth"]["single_turn"] += 1
        elif msg_count <= 5:
            patterns["conversation_depth"]["short"] += 1
        elif msg_count <= 15:
            patterns["conversation_depth"]["medium"] += 1
        else:
            patterns["conversation_depth"]["deep"] += 1

        # Track session start hours
        start = session.get("session_start", "")
        if start:
            try:
                hour = datetime.fromisoformat(start.replace("Z", "+00:00")).hour
                patterns["session_timing"]["hours"][str(hour)] += 1
            except (ValueError, TypeError):
                pass

    if sessions:
        patterns["average_messages_per_session"] = round(total_messages / len(sessions), 1)

    # Convert Counter to dict for JSON serialization
    patterns["session_timing"]["hours"] = dict(patterns["session_timing"]["hours"])

    return patterns


# =============================================================================
# Behavioral Archetype Characterization
# =============================================================================

def characterize_archetype(sessions: list, task_distribution: dict,
                           friction_count: int, delight_count: int) -> dict:
    """Characterize the user's behavioral archetype based on usage patterns."""
    total_sessions = len(sessions)
    if total_sessions == 0:
        return {"archetype": "new_user", "description": "Not enough data yet to characterize usage patterns."}

    total_messages = sum(s.get("message_count", 0) for s in sessions)
    avg_messages = total_messages / total_sessions
    total_user_messages = sum(s.get("user_message_count", 0) for s in sessions)
    tool_heavy = sum(1 for s in sessions if s.get("tool_result_count", 0) > 5)
    avg_duration = sum(s.get("duration_seconds", 0) for s in sessions) / total_sessions

    traits = []
    archetype = "explorer"

    # Delegation level
    if avg_messages > 15 and tool_heavy > total_sessions * 0.5:
        traits.append("delegates complex multi-step tasks")
        archetype = "power_delegator"
    elif avg_messages < 4:
        traits.append("uses quick, targeted queries")
        archetype = "efficient_querier"

    # Task diversity
    if len(task_distribution) >= 4:
        traits.append("works across diverse task categories")
        archetype = "generalist" if archetype == "explorer" else archetype
    elif len(task_distribution) <= 2 and task_distribution:
        top_task = max(task_distribution, key=task_distribution.get)
        traits.append(f"focused primarily on {top_task}")
        archetype = "specialist"

    # Trust level
    if friction_count > delight_count * 2 and friction_count > 3:
        traits.append("frequently corrects or re-prompts the agent")
        archetype = "cautious_verifier"
    elif delight_count > friction_count * 2 and delight_count > 2:
        traits.append("high trust — builds on agent output iteratively")
        if archetype == "explorer":
            archetype = "trusting_collaborator"

    # Session length patterns
    if avg_duration > 1200:
        traits.append("engages in long, deep work sessions")
    elif avg_duration < 180:
        traits.append("prefers short, focused interactions")

    descriptions = {
        "power_delegator": "Power user who delegates complex multi-step tasks and relies heavily on tool integrations.",
        "efficient_querier": "Efficient user who asks targeted questions and gets quick answers.",
        "generalist": "Generalist who uses the agent across many different task categories.",
        "specialist": "Specialist who deeply uses the agent for a focused set of tasks.",
        "cautious_verifier": "Cautious user who double-checks outputs and frequently corrects the agent.",
        "trusting_collaborator": "Trusting collaborator who iteratively builds on agent outputs with confidence.",
        "explorer": "Explorer still developing their usage patterns and discovering capabilities.",
        "new_user": "New user with limited interaction history.",
    }

    return {
        "archetype": archetype,
        "description": descriptions.get(archetype, ""),
        "traits": traits,
    }


# =============================================================================
# Tool / Skill Usage Analysis
# =============================================================================

def analyze_tool_usage(sessions: list) -> dict:
    """Analyze tool and skill usage patterns."""
    tool_stats = {
        "total_tool_calls": 0,
        "successful": 0,
        "failed": 0,
        "success_rate": 0.0,
    }

    for session in sessions:
        calls = session.get("tool_calls", [])
        tool_stats["total_tool_calls"] += len(calls)
        for call in calls:
            if call.get("success", True):
                tool_stats["successful"] += 1
            else:
                tool_stats["failed"] += 1

    if tool_stats["total_tool_calls"] > 0:
        tool_stats["success_rate"] = round(
            tool_stats["successful"] / tool_stats["total_tool_calls"] * 100, 1
        )

    return tool_stats


# =============================================================================
# Trend Comparison
# =============================================================================

def compare_trends(current_metrics: dict, trends_file: str) -> dict:
    """Compare current day's metrics against historical trends."""
    comparison = {"has_history": False, "notes": []}

    try:
        with open(trends_file, "r") as f:
            trends = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return comparison

    daily_entries = trends.get("daily", [])
    if not daily_entries:
        return comparison

    comparison["has_history"] = True

    # Compare against last 7 days average
    recent = daily_entries[-7:]
    if not recent:
        return comparison

    avg_sessions = sum(d.get("session_count", 0) for d in recent) / len(recent)
    avg_cost = sum(d.get("total_cost", 0) for d in recent) / len(recent)
    avg_friction = sum(d.get("friction_count", 0) for d in recent) / len(recent)

    curr_sessions = current_metrics.get("session_count", 0)
    curr_cost = current_metrics.get("total_cost", 0)
    curr_friction = current_metrics.get("friction_count", 0)

    if curr_sessions > avg_sessions * 1.5:
        comparison["notes"].append(f"Session count ({curr_sessions}) is notably higher than 7-day average ({avg_sessions:.1f})")
    elif curr_sessions < avg_sessions * 0.5 and avg_sessions > 1:
        comparison["notes"].append(f"Session count ({curr_sessions}) is notably lower than 7-day average ({avg_sessions:.1f})")

    if curr_cost > avg_cost * 2 and avg_cost > 0:
        comparison["notes"].append(f"Cost (${curr_cost:.4f}) is significantly higher than 7-day average (${avg_cost:.4f})")

    if curr_friction > avg_friction * 1.5 and avg_friction > 0:
        comparison["notes"].append("More friction signals than usual — may indicate a difficult task day")
    elif curr_friction < avg_friction * 0.5 and avg_friction > 1:
        comparison["notes"].append("Fewer friction signals than usual — smooth sailing today")

    return comparison


# =============================================================================
# Recommendations Engine
# =============================================================================

def generate_recommendations(analysis: dict) -> list:
    """Generate actionable UXR-informed recommendations."""
    recs = []
    friction = analysis.get("friction_log", [])
    tasks = analysis.get("task_distribution", {})
    tool_stats = analysis.get("tool_usage", {})
    archetype = analysis.get("behavioral_archetype", {}).get("archetype", "")

    # Friction-based recommendations
    confusion_count = sum(1 for f in friction if f["type"] == "confusion")
    if confusion_count >= 2:
        recs.append({
            "priority": "high",
            "recommendation": "Consider creating a custom skill or CLAUDE.md instructions for frequently confused-about topics to reduce rephrasing overhead.",
        })

    tool_failures = sum(1 for f in friction if f["type"] == "tool_failure")
    if tool_failures >= 2:
        recs.append({
            "priority": "high",
            "recommendation": "Multiple tool failures detected. Review tool configurations and ensure required dependencies are installed.",
        })

    # Task-based recommendations
    if "coding" in tasks and tasks["coding"] > 0.4:
        recs.append({
            "priority": "medium",
            "recommendation": "Heavy coding usage detected. Consider setting up project-specific CLAUDE.md files for your most active repositories to give the agent better context.",
        })

    if "automation" in tasks and tasks["automation"] > 0.2:
        recs.append({
            "priority": "medium",
            "recommendation": "Automation tasks are frequent. Explore OpenClaw's cron job feature to schedule recurring tasks automatically.",
        })

    # Archetype-based recommendations
    if archetype == "cautious_verifier":
        recs.append({
            "priority": "medium",
            "recommendation": "You frequently correct agent outputs. Consider providing more context upfront in your prompts, or creating skills that encode your preferences.",
        })

    if archetype == "efficient_querier":
        recs.append({
            "priority": "low",
            "recommendation": "You use quick, targeted queries effectively. You might benefit from custom slash commands for your most frequent query types.",
        })

    # Tool usage recommendations
    if tool_stats.get("success_rate", 100) < 80:
        recs.append({
            "priority": "high",
            "recommendation": f"Tool success rate is {tool_stats['success_rate']}%. Investigate failing tools and consider updating or replacing unreliable integrations.",
        })

    if not recs:
        recs.append({
            "priority": "info",
            "recommendation": "Usage patterns look healthy. No specific improvements recommended at this time.",
        })

    return recs


# =============================================================================
# Main Analysis Pipeline
# =============================================================================

def run_analysis(sessions: list, trends_file: str = None) -> dict:
    """Run the full ethnographic analysis pipeline."""
    # Task classification across all user messages
    task_scores = Counter()
    task_counts = Counter()

    for session in sessions:
        for msg in session.get("messages", []):
            if msg.get("role") == "user":
                scores = classify_task(msg.get("text", ""))
                for category, score in scores.items():
                    task_scores[category] += score
                    task_counts[category] += 1

    # Normalize task distribution to percentages
    total_score = sum(task_scores.values()) or 1
    task_distribution = {
        cat: round(score / total_score * 100, 1)
        for cat, score in task_scores.most_common()
    }

    # Session statistics
    total_cost = sum(s.get("total_cost", 0) for s in sessions)
    total_duration = sum(s.get("duration_seconds", 0) for s in sessions)
    avg_duration = total_duration / len(sessions) if sessions else 0

    session_stats = {
        "session_count": len(sessions),
        "total_duration_seconds": total_duration,
        "average_duration_seconds": round(avg_duration, 1),
        "total_cost": round(total_cost, 6),
        "total_messages": sum(s.get("message_count", 0) for s in sessions),
        "total_user_messages": sum(s.get("user_message_count", 0) for s in sessions),
        "total_assistant_messages": sum(s.get("assistant_message_count", 0) for s in sessions),
    }

    # Friction and delight
    friction_log = detect_friction(sessions)
    delight_log = detect_delight(sessions)

    # Patterns
    interaction_patterns = detect_patterns(sessions)

    # Quotes
    verbatim_quotes = extract_quotes(sessions)

    # Tool usage
    tool_usage = analyze_tool_usage(sessions)

    # Archetype
    behavioral_archetype = characterize_archetype(
        sessions, task_distribution,
        len(friction_log), len(delight_log)
    )

    # Build analysis object
    analysis = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "session_stats": session_stats,
        "task_distribution": task_distribution,
        "friction_log": friction_log,
        "delight_log": delight_log,
        "interaction_patterns": interaction_patterns,
        "verbatim_quotes": verbatim_quotes,
        "tool_usage": tool_usage,
        "behavioral_archetype": behavioral_archetype,
    }

    # Trend comparison
    if trends_file:
        current_metrics = {
            "session_count": session_stats["session_count"],
            "total_cost": session_stats["total_cost"],
            "friction_count": len(friction_log),
        }
        analysis["trend_comparison"] = compare_trends(current_metrics, trends_file)

    # Recommendations
    analysis["recommendations"] = generate_recommendations(analysis)

    return analysis


def main():
    parser = argparse.ArgumentParser(description="UXR Ethnographic Analysis Engine")
    parser.add_argument("--input", required=True, help="Path to redacted session data JSON")
    parser.add_argument("--trends", default=None, help="Path to trends.json for longitudinal comparison")
    args = parser.parse_args()

    try:
        with open(args.input, "r") as f:
            sessions = json.load(f)
    except FileNotFoundError:
        print(json.dumps({"error": f"Input file not found: {args.input}"}), file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON in input file: {e}"}), file=sys.stderr)
        sys.exit(1)

    if not isinstance(sessions, list):
        print(json.dumps({"error": "Input must be a JSON array of session objects"}), file=sys.stderr)
        sys.exit(1)

    analysis = run_analysis(sessions, args.trends)
    print(json.dumps(analysis, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
