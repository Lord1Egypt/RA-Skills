#!/usr/bin/env python3
"""
Memory Tree Seal Worker

Scans memory/source/ for new/unsealed files, generates topic summaries,
manages global knowledge, and maintains the index.

Usage:
    python3 seal-worker.py [--dry-run] [--force]

--dry-run: Show what would be sealed without writing
--force:  Re-seal all source files (not just new ones)
"""

import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────────────

WORKSPACE = Path(os.environ.get("MEMORY_WORKSPACE", os.path.expanduser("~/.openclaw/workspace")))
MEMORY_ROOT = Path(os.environ.get("MEMORY_ROOT", str(WORKSPACE / "memory")))
SOURCE_DIR = MEMORY_ROOT / "source"
TOPIC_DIR = MEMORY_ROOT / "topic"
GLOBAL_DIR = MEMORY_ROOT / "global"
META_DIR = MEMORY_ROOT / "_meta"

INDEX_FILE = META_DIR / "index.json"
SEALING_LOG = META_DIR / "sealing-log.json"

MAX_TOPIC_TOKENS = 2000   # ~8000 chars
MAX_GLOBAL_TOKENS = 5000  # ~20000 chars
TOKEN_RATIO = 4          # chars per token estimate

# Topic detection keywords → topic name mapping
TOPIC_KEYWORDS = {
    "security": ["security", "audit", "hack", "vulnerability", "penetration", 
                  "breach", "compromise", "wallet", "steal", "theft"],
    "infrastructure": ["service", "docker", "systemd", "gateway", "api", "port", "server",
                       "deploy", "restart", "health", "uptime", "infrastructure"],
    "devices": ["adb", "phone", "tablet", "edge", "s21", "quest", "surface", "razer",
                "device", "tailscale", "battery", "screen"],
    "models": ["model", "ollama", "qwen", "deepseek", "glm", "gemma", "routing", "think",
               "llm", "inference", "token", "context"],
    "conversation": ["voice", "tts", "stt", "wake", "vad", "conversation", "avatar",
                     "speak", "listen", "whisper", "chatterbox", "kokoro"],
    "architecture": ["architecture", "phase", "doctrine", "system", "design", "pattern",
                     "module", "component", "integration", "registry", "compatibility"],
    "team": ["department", "mario", "peter", "woody", "wazowski", "felix", 
             "frida", "kubrick", "atlas", "nova", "rex", "spark", "justicia",
             "dispatch", "evolution", "gupp", "team", "delegate"],
    "product": ["superclaw", "nanoclaw", "command center", "app", "beta", "pwa",
                "apk", "release", "build", "android", "platform"],
    "trading": ["trading", "crypto", "solana", "bot", "stackflow", "ruda", "finance",
                "wallet", "capital"],
    "nanoclaw-os": ["nanoclaw", "lineage", "rom", "bootloader", "razer edge",
                    "nicole", "custom rom", "edge shell"],
    "strategy": ["goal", "initiative", "strategic", "priority", "forecast", "simulation",
                "optimization", "briefing", "planning"],
    "daily-ops": ["heartbeat", "cron", "monitoring", "check", "status", "boot",
                  "routine", "operational"],
}

# Global knowledge categories — maps topic prefixes to global files
GLOBAL_CATEGORIES = {
    "IDENTITY": ["security", "team", "architecture"],
    "DOCTRINE": ["infrastructure", "daily-ops", "strategy", "models"],
    "PREFERENCES": ["models", "conversation", "product"],
    "SECURITY": ["security"],
    "ARCHITECTURE": ["infrastructure", "architecture", "devices", "conversation"],
    "PRODUCTS": ["product", "nanoclaw-os", "conversation", "trading"],
}


# ── Helpers ─────────────────────────────────────────────────────────────────────

def estimate_tokens(text: str) -> int:
    """Rough token estimate: ~4 chars per token."""
    return max(1, len(text) // TOKEN_RATIO)


def file_hash(path: Path) -> str:
    """SHA-256 hash of file contents."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path, default=None):
    """Load JSON file, return default if missing/corrupt."""
    if not path.exists():
        return default if default is not None else {}
    try:
        with open(path) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default if default is not None else {}


def save_json(path: Path, data):
    """Save JSON file with pretty formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def append_sealing_log(entry: dict):
    """Append an entry to the sealing log."""
    log = load_json(SEALING_LOG, [])
    entry["timestamp"] = datetime.now(timezone.utc).isoformat()
    log.append(entry)
    # Keep log to last 500 entries
    if len(log) > 500:
        log = log[-500:]
    save_json(SEALING_LOG, log)


# ── Topic Detection ────────────────────────────────────────────────────────────

def detect_topics(content: str, filename: str) -> list[str]:
    """Detect which topics a source file relates to based on keywords."""
    content_lower = content.lower()
    filename_lower = filename.lower()
    combined = content_lower + " " + filename_lower

    topics = []
    for topic, keywords in TOPIC_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in combined)
        if score >= 2:  # Need at least 2 keyword hits
            topics.append(topic)

    # Always assign at least "misc" if no topics detected
    if not topics:
        topics.append("misc")

    return topics


def extract_date_from_filename(filename: str) -> str:
    """Extract date prefix from filename like 2026-05-22-conversation.md."""
    match = re.match(r"(\d{4}-\d{2}-\d{2})", filename)
    return match.group(1) if match else datetime.now().strftime("%Y-%m-%d")


def extract_headings(content: str) -> list[str]:
    """Extract markdown headings from content."""
    headings = []
    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("#"):
            heading = line.lstrip("#").strip()
            if heading:
                headings.append(heading)
    return headings


def summarize_content(content: str, max_tokens: int = MAX_TOPIC_TOKENS) -> str:
    """
    Create a summary of content within token budget.
    Uses extractive approach: keep headings and first sentences of sections.
    """
    max_chars = max_tokens * TOKEN_RATIO
    if len(content) <= max_chars:
        return content

    lines = content.split("\n")
    result_lines = []
    current_size = 0

    for line in lines:
        # Always keep headings and blank lines
        if line.strip().startswith("#") or line.strip() == "":
            result_lines.append(line)
            current_size += len(line) + 1
        else:
            # Keep first sentence of each paragraph
            sentence = line.split(". ")[0] + ("." if ". " in line else "")
            if len(sentence) > 10:  # Skip very short fragments
                result_lines.append(sentence)
                current_size += len(sentence) + 1

        if current_size >= max_chars:
            result_lines.append("\n... (truncated to fit topic budget)")
            break

    return "\n".join(result_lines)


# ── Sealing Logic ──────────────────────────────────────────────────────────────

def get_unsealed_sources(index: dict) -> list[Path]:
    """Find source files that haven't been sealed yet."""
    sealed_files = set()
    for source_path, info in index.get("sources", {}).items():
        if info.get("sealed"):
            sealed_files.add(source_path)

    all_sources = sorted(SOURCE_DIR.glob("*.md"))
    unsealed = []
    for path in all_sources:
        rel = str(path.relative_to(MEMORY_ROOT))
        if rel not in sealed_files:
            unsealed.append(path)
    return unsealed


def get_changed_sources(index: dict) -> list[Path]:
    """Find source files whose hash has changed since last sealing."""
    changed = []
    for path in sorted(SOURCE_DIR.glob("*.md")):
        rel = str(path.relative_to(MEMORY_ROOT))
        info = index.get("sources", {}).get(rel, {})
        if not info.get("sealed") or info.get("hash") != file_hash(path):
            changed.append(path)
    return changed


def seal_source(source_path: Path, index: dict, dry_run: bool = False) -> dict:
    """
    Seal a single source file into its topic(s).
    Returns sealing info dict.
    """
    rel = str(source_path.relative_to(MEMORY_ROOT))
    content = source_path.read_text(encoding="utf-8", errors="replace")
    h = file_hash(source_path)
    date = extract_date_from_filename(source_path.name)
    topics = detect_topics(content, source_path.name)
    headings = extract_headings(content)

    seal_info = {
        "source": rel,
        "hash": h,
        "tokens": estimate_tokens(content),
        "topics": topics,
        "headings": headings[:20],  # Keep first 20
        "date": date,
        "sealed_at": datetime.now(timezone.utc).isoformat(),
    }

    if dry_run:
        return seal_info

    # Update/create topic summaries
    for topic in topics:
        topic_file = TOPIC_DIR / f"{topic}.md"

        existing_content = ""
        if topic_file.exists():
            existing_content = topic_file.read_text(encoding="utf-8", errors="replace")

        # Build topic entry from this source
        entry = f"\n## Source: {source_path.name} ({date})\n\n"
        # Add summary of the content
        summary = summarize_content(content, max_tokens=500)
        entry += summary + "\n"

        new_content = existing_content + entry

        # Truncate if over budget
        if estimate_tokens(new_content) > MAX_TOPIC_TOKENS:
            # Keep the newest content, truncate from the top
            new_content = _truncate_topic(new_content, MAX_TOPIC_TOKENS)

        topic_file.parent.mkdir(parents=True, exist_ok=True)
        topic_file.write_text(new_content, encoding="utf-8")

        # Update index: source → topic mapping
        if topic not in index.get("source_to_topic", {}):
            index.setdefault("source_to_topic", {})[topic] = []
        if rel not in index["source_to_topic"][topic]:
            index["source_to_topic"][topic].append(rel)

        # Update index: topic info
        index.setdefault("topics", {})[topic] = {
            "file": str(topic_file.relative_to(MEMORY_ROOT)),
            "tokens": estimate_tokens(new_content),
            "sources": index["source_to_topic"].get(topic, []),
            "last_updated": datetime.now(timezone.utc).isoformat(),
        }

    # Mark source as sealed in index
    index.setdefault("sources", {})[rel] = {
        "sealed": True,
        "hash": h,
        "tokens": estimate_tokens(content),
        "topics": topics,
        "sealed_at": datetime.now(timezone.utc).isoformat(),
    }

    append_sealing_log({
        "action": "seal_source",
        "source": rel,
        "topics": topics,
        "tokens": estimate_tokens(content),
    })

    return seal_info


def _truncate_topic(content: str, max_tokens: int) -> str:
    """Truncate topic content from the top, keeping most recent entries."""
    max_chars = max_tokens * TOKEN_RATIO
    if len(content) <= max_chars:
        return content

    # Split by "## Source:" headers
    sections = re.split(r"(?=## Source:)", content)

    # Keep header (first section) and most recent sections
    if sections and not sections[0].startswith("## Source:"):
        header = sections[0]
        entries = sections[1:]
    else:
        header = ""
        entries = sections

    # Keep as many recent entries as fit
    kept = []
    current_size = len(header)
    for entry in reversed(entries):
        if current_size + len(entry) <= max_chars:
            kept.insert(0, entry)
            current_size += len(entry)
        else:
            break

    result = header
    if kept:
        result += "\n".join(kept)
    result += f"\n\n> ⚠️ Topic truncated. {len(entries) - len(kept)} older entries removed.\n"
    return result


def update_global_knowledge(index: dict, dry_run: bool = False) -> list[str]:
    """
    Regenerate global knowledge files from topic summaries.
    Returns list of updated global files.
    """
    updated = []

    for global_name, topic_prefixes in GLOBAL_CATEGORIES.items():
        global_file = GLOBAL_DIR / f"{global_name}.md"

        # Collect content from matching topics
        combined = f"# {global_name.title()} — Global Knowledge\n\n"
        combined += f"_Auto-generated from topic summaries. Last updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}_\n\n"

        for topic_prefix in topic_prefixes:
            topic_file = TOPIC_DIR / f"{topic_prefix}.md"
            if topic_file.exists():
                topic_content = topic_file.read_text(encoding="utf-8", errors="replace")
                # Extract just the key facts (headings + first lines)
                facts = _extract_key_facts(topic_content)
                if facts.strip():
                    combined += f"## {topic_prefix.title()}\n\n"
                    combined += facts + "\n\n"

        if estimate_tokens(combined) > MAX_GLOBAL_TOKENS:
            combined = _truncate_global(combined, MAX_GLOBAL_TOKENS)

        if not dry_run:
            global_file.parent.mkdir(parents=True, exist_ok=True)
            global_file.write_text(combined, encoding="utf-8")

            # Update index
            index.setdefault("global", {})[global_name] = {
                "file": str(global_file.relative_to(MEMORY_ROOT)),
                "tokens": estimate_tokens(combined),
                "topics": topic_prefixes,
                "last_updated": datetime.now(timezone.utc).isoformat(),
            }

        updated.append(global_name)

    return updated


def _extract_key_facts(topic_content: str) -> str:
    """Extract key facts from a topic summary for global knowledge."""
    lines = topic_content.split("\n")
    facts = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Keep headings and bullet points
        if line.startswith("#") or line.startswith("-") or line.startswith("*") or line.startswith("•"):
            facts.append(line)
        # Keep key-value pairs
        elif ":" in line and not line.startswith("```"):
            facts.append(line)

    result = "\n".join(facts)
    # Trim if too long
    max_chars = 1500 * TOKEN_RATIO  # Allocate ~1500 tokens per topic in global
    if len(result) > max_chars:
        result = result[:max_chars] + "\n... (truncated)"
    return result


def _truncate_global(content: str, max_tokens: int) -> str:
    """Truncate global knowledge file to fit within token budget."""
    max_chars = max_tokens * TOKEN_RATIO
    if len(content) <= max_chars:
        return content

    # Keep header and truncate content
    lines = content.split("\n")
    header_lines = []
    content_lines = []
    in_header = True

    for line in lines:
        if in_header and (line.startswith("#") or line.startswith("_") or line.strip() == ""):
            header_lines.append(line)
        else:
            in_header = False
            content_lines.append(line)

    # Keep header + as much content as fits
    result = "\n".join(header_lines) + "\n\n"
    remaining = max_chars - len(result)

    for line in content_lines:
        if remaining - len(line) - 1 > 0:
            result += line + "\n"
            remaining -= len(line) + 1
        else:
            break

    result += f"\n> ⚠️ Global knowledge truncated to {max_tokens} tokens.\n"
    return result


# ── Main ────────────────────────────────────────────────────────────────────────

def main():
    dry_run = "--dry-run" in sys.argv
    force = "--force" in sys.argv

    # Ensure directories exist
    for d in [SOURCE_DIR, TOPIC_DIR, GLOBAL_DIR, META_DIR]:
        d.mkdir(parents=True, exist_ok=True)

    # Load or initialize index
    index = load_json(INDEX_FILE, {
        "version": 1,
        "sources": {},
        "source_to_topic": {},
        "topics": {},
        "global": {},
        "last_seal": None,
    })

    # Find sources to seal
    if force:
        sources_to_seal = sorted(SOURCE_DIR.glob("*.md"))
        print(f"[FORCE] Re-sealing all {len(sources_to_seal)} source files")
    else:
        sources_to_seal = get_changed_sources(index)
        unsealed = get_unsealed_sources(index)
        # Combine: unsealed + changed
        seen = set(str(p) for p in sources_to_seal)
        for s in unsealed:
            if str(s) not in seen:
                sources_to_seal.append(s)
                seen.add(str(s))
        print(f"Found {len(sources_to_seal)} source files to seal")

    if not sources_to_seal:
        print("No new/changed sources to seal.")
        if not dry_run:
            # Still update global knowledge from existing topics
            updated_globals = update_global_knowledge(index, dry_run=False)
            if updated_globals:
                print(f"Updated global knowledge: {', '.join(updated_globals)}")
                index["last_seal"] = datetime.now(timezone.utc).isoformat()
                save_json(INDEX_FILE, index)
        return

    # Seal each source
    seal_results = []
    for source_path in sources_to_seal:
        try:
            result = seal_source(source_path, index, dry_run=dry_run)
            seal_results.append(result)
            print(f"  Sealed: {source_path.name} → {result['topics']}")
        except Exception as e:
            print(f"  ERROR sealing {source_path.name}: {e}")
            append_sealing_log({
                "action": "seal_error",
                "source": str(source_path),
                "error": str(e),
            })

    # Update global knowledge
    updated_globals = update_global_knowledge(index, dry_run=dry_run)
    if updated_globals:
        print(f"Updated global knowledge: {', '.join(updated_globals)}")

    if not dry_run:
        index["last_seal"] = datetime.now(timezone.utc).isoformat()
        save_json(INDEX_FILE, index)
        print(f"\nSealing complete. {len(seal_results)} sources sealed.")
    else:
        print(f"\n[DRY RUN] Would seal {len(seal_results)} sources.")


if __name__ == "__main__":
    main()
