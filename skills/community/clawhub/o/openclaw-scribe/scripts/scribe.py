#!/usr/bin/env python3
"""
Scribe - Autonomous session memory extractor for OpenClaw.
Reads today's session JSONL files, extracts key signals via LLM,
and writes structured memory to memory/YYYY-MM-DD.md.
"""

import os
import sys
import json
import datetime
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────
SESSION_DIR  = Path(os.environ.get("SCRIBE_SESSION_DIR",
               Path.home() / ".openclaw/agents/main/sessions"))
WORKSPACE    = Path(os.environ.get("SCRIBE_WORKSPACE",
               Path.home() / ".openclaw/workspace"))
DAYS_BACK    = int(os.environ.get("SCRIBE_DAYS", "1"))
APPEND_LT    = os.environ.get("SCRIBE_APPEND_LONGTERM", "false").lower() == "true"
MODEL        = os.environ.get("SCRIBE_MODEL", "")   # empty = use oracle default

# ── Helpers ───────────────────────────────────────────────────────────────────
def date_range(days_back: int) -> list[str]:
    today = datetime.date.today()
    return [(today - datetime.timedelta(days=i)).isoformat() for i in range(days_back)]

def load_sessions(session_dir: Path, dates: list[str]) -> list[dict]:
    """Load JSONL session files modified on the target dates."""
    messages = []
    for jsonl in sorted(session_dir.glob("*.jsonl")):
        mtime = datetime.date.fromtimestamp(jsonl.stat().st_mtime).isoformat()
        if mtime not in dates:
            continue
        with open(jsonl, encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    messages.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return messages

def filter_user_messages(messages: list[dict]) -> list[str]:
    """Extract meaningful user messages, skip system/heartbeat noise.
    
    Supports two JSONL formats:
    1. Flat: {role, content}
    2. Nested: {type, message: {role, content: [{type, text}]}}
    """
    skip_patterns = [
        "HEARTBEAT", "heartbeat", "Pre-compaction memory flush",
        "Read HEARTBEAT.md", "HEARTBEAT_OK",
    ]
    texts = []
    for m in messages:
        # Format 1: nested {message: {role, content}}
        inner = m.get("message")
        if isinstance(inner, dict):
            role = inner.get("role", "")
            content = inner.get("content", "")
        else:
            # Format 2: flat {role, content}
            role = m.get("role", "")
            content = m.get("content", "")

        if role != "user":
            continue

        # Normalize content: list of {type, text} or plain string
        if isinstance(content, list):
            content = " ".join(
                c.get("text", "") for c in content if isinstance(c, dict)
            )
        if not content or not content.strip():
            continue
        if any(p in content for p in skip_patterns):
            continue
        texts.append(content.strip())
    return texts

def get_api_config() -> tuple[str, str]:
    """Read OpenRouter API key and model from OpenClaw config."""
    config_path = Path.home() / ".openclaw/openclaw.json"
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    model = MODEL or "anthropic/claude-haiku-4-5"

    if not api_key and config_path.exists():
        try:
            with open(config_path) as f:
                cfg = json.load(f)
            providers = cfg.get("models", {}).get("providers", {})
            or_cfg = providers.get("openrouter", {})
            api_key = or_cfg.get("apiKey", "")
            if not MODEL:
                models = or_cfg.get("models", [])
                if models:
                    model = models[0].get("id", model)
        except Exception:
            pass

    return api_key, model

def extract_with_llm(conversation_text: str, date: str) -> str:
    """Call OpenRouter API to extract signals from conversation text."""

    api_key, model = get_api_config()
    if not api_key:
        print("[scribe] No API key found. Set OPENROUTER_API_KEY or configure OpenClaw.", file=sys.stderr)
        sys.exit(1)

    prompt = f"""You are a session scribe. Analyze the following AI assistant conversation from {date} and extract key signals.

Output ONLY a structured Markdown document with these sections (skip any section with no content):

## 🔑 Decisions Made
- Concrete decisions or choices the user made

## 💡 Preferences & Rules
- User preferences, constraints, or rules they expressed

## 🗣️ Framework Sentences
- Strong directive phrases the user used that reveal how they think/communicate
- Examples: "不管，你来决定", "做不到就换个方法", "一步一步来"

## 📦 Project Updates
- Progress on specific projects, tools, or features discussed

## ✅ Todos / Follow-ups
- Tasks mentioned but not yet completed

---

CONVERSATION:
{conversation_text}
"""

    payload = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2000,
    })

    import tempfile, os as _os
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write(payload)
        tmp_path = f.name

    try:
        import subprocess
        result = subprocess.run(
            [
                "curl", "-s", "--max-time", "60",
                "-X", "POST",
                "https://openrouter.ai/api/v1/chat/completions",
                "-H", f"Authorization: Bearer {api_key}",
                "-H", "Content-Type: application/json",
                "-H", "HTTP-Referer: https://github.com/openclaw/scribe",
                "-d", f"@{tmp_path}",
            ],
            capture_output=True, text=True, timeout=70,
        )
        _os.unlink(tmp_path)
        if result.returncode != 0:
            print(f"[scribe] curl error: {result.stderr}", file=sys.stderr)
            return ""
        data = json.loads(result.stdout)
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"[scribe] LLM call failed: {e}", file=sys.stderr)
        _os.unlink(tmp_path)
        return ""

def write_memory(date: str, content: str, workspace: Path) -> Path:
    """Write extracted content to memory/YYYY-MM-DD.md."""
    memory_dir = workspace / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    out_path = memory_dir / f"{date}.md"

    header = f"# {date} Memory (Scribe)\n\n"

    # Append if file already exists (manual notes may be there)
    if out_path.exists():
        existing = out_path.read_text(encoding="utf-8")
        if "## 🔑 Decisions Made" in existing:
            # Already has scribe output — append with separator
            out_path.write_text(
                existing + f"\n\n---\n*Scribe update — {datetime.datetime.now().strftime('%H:%M')}*\n\n" + content,
                encoding="utf-8",
            )
        else:
            out_path.write_text(existing + "\n\n" + header + content, encoding="utf-8")
    else:
        out_path.write_text(header + content, encoding="utf-8")

    return out_path

def append_longterm(content: str, workspace: Path, date: str):
    """Optionally append a summary line to MEMORY.md."""
    lt_path = workspace / "MEMORY.md"
    if not lt_path.exists():
        return
    summary_line = f"\n<!-- Scribe {date} -->\n{content}\n"
    with open(lt_path, "a", encoding="utf-8") as f:
        f.write(summary_line)

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    dates = date_range(DAYS_BACK)
    target_date = dates[0]  # primary date label for output file

    print(f"[scribe] Scanning sessions for: {', '.join(dates)}")
    print(f"[scribe] Session dir: {SESSION_DIR}")

    messages = load_sessions(SESSION_DIR, dates)
    print(f"[scribe] Loaded {len(messages)} raw messages")

    user_msgs = filter_user_messages(messages)
    print(f"[scribe] Filtered to {len(user_msgs)} user messages")

    if not user_msgs:
        print("[scribe] Nothing to extract. Exiting.")
        return

    conversation_text = "\n\n".join(f"USER: {m}" for m in user_msgs)

    # Truncate if very long (oracle has context limits)
    max_chars = 40_000
    if len(conversation_text) > max_chars:
        conversation_text = conversation_text[-max_chars:]
        print(f"[scribe] Truncated to last {max_chars} chars")

    print("[scribe] Extracting signals via LLM...")
    extracted = extract_with_llm(conversation_text, target_date)

    if not extracted:
        print("[scribe] No output from oracle. Exiting.")
        return

    out_path = write_memory(target_date, extracted, WORKSPACE)
    print(f"[scribe] Written to: {out_path}")

    if APPEND_LT:
        append_longterm(extracted, WORKSPACE, target_date)
        print(f"[scribe] Appended to MEMORY.md")

if __name__ == "__main__":
    main()
