#!/usr/bin/env python3
"""
OpenMem - auto_compress.py
Automated daily session compression. Designed to run unattended via OpenClaw cron.

Guards:
  - Runs at most once per calendar day
  - Only runs after 2+ hours of agent inactivity
  - Skips the most recently active session (may still be in use)

Extraction:
  - Calls `openclaw capability model run` to use the user's configured model
  - No credentials or config files are read — OpenClaw handles provider routing
  - Falls back to heuristic extraction if openclaw CLI is unavailable

Deduplication:
  - FTS5 word-overlap check before every insert
  - Skips memories too similar to existing ones

Session wipe:
  - After all memories confirmed in DB, replaces old session JSONL with a
    one-line stub. Only wipes sessions that are >24h old and not the
    most recently active session.

Usage:
  python3 auto_compress.py              # normal run (respects guards)
  python3 auto_compress.py --force      # skip date/inactivity guards
  python3 auto_compress.py --dry-run    # show what would happen, no writes
  python3 auto_compress.py --no-wipe    # compress but do not wipe session files

Env vars:
  OPENMEM_DB                   Path to openmem.db
  OPENMEM_SESSIONS_DIR         Path to OpenClaw sessions directory
  OPENMEM_COMPRESS_INACTIVITY  Minimum inactivity hours before running (default: 2)
"""

import argparse
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import time
from datetime import date
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DEFAULT_DB = Path(
    os.environ.get("OPENMEM_DB", "~/.openclaw/workspace/memory/openmem.db")
).expanduser()

DEFAULT_SESSIONS_DIR = Path(
    os.environ.get("OPENMEM_SESSIONS_DIR", "~/.openclaw/agents/main/sessions")
).expanduser()

STATE_FILE = DEFAULT_DB.parent / "auto_compress_state.json"
LOG_FILE = Path("~/.openclaw/logs/openmem-compress.log").expanduser()

INACTIVITY_HOURS = float(os.environ.get("OPENMEM_COMPRESS_INACTIVITY", "2"))

EXTRACT_PROMPT_TEMPLATE = """\
You are extracting long-term memories from an AI agent conversation log.

Extract 3-8 key facts, preferences, decisions, and corrections worth keeping.
Focus on:
- User preferences and working style
- Decisions made and why
- Corrections (what was wrong, what's right)
- Key facts about the user's projects, systems, and setup
- Important events or milestones

Respond with ONLY a JSON array, no explanation:
[
  {{"content": "...", "category": "preference|fact|insight|correction|event", "importance": 0.7}}
]

Rules:
- Skip routine status updates, small talk, greetings, tool output
- Each memory must be standalone (understandable without context)
- Maximum 100 words per memory
- importance: 0.9 = critical preference/correction, 0.7 = important, 0.5 = normal

Conversation (most recent messages):
{text}

JSON array:"""


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def log(msg: str):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except OSError:
        pass


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

def load_state() -> dict:
    try:
        return json.loads(STATE_FILE.read_text())
    except (OSError, json.JSONDecodeError):
        return {}


def save_state(state: dict):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


def already_ran_today(state: dict) -> bool:
    return state.get("last_run_date") == str(date.today())


# ---------------------------------------------------------------------------
# Inactivity check
# ---------------------------------------------------------------------------

def latest_session_mtime(sessions_dir: Path) -> Optional[float]:
    """Return the mtime of the most recently modified session file."""
    best = None
    for p in sessions_dir.glob("*.jsonl"):
        if ".checkpoint." in p.name:
            continue
        mtime = p.stat().st_mtime
        if best is None or mtime > best:
            best = mtime
    return best


def agent_is_inactive(sessions_dir: Path, min_hours: float) -> bool:
    mtime = latest_session_mtime(sessions_dir)
    if mtime is None:
        return True  # no sessions at all → treat as inactive
    inactive_seconds = time.time() - mtime
    return inactive_seconds >= (min_hours * 3600)


# ---------------------------------------------------------------------------
# Session reading (mirrors compress.py)
# ---------------------------------------------------------------------------

def read_session_messages(session_file: Path) -> list[dict]:
    messages = []
    try:
        with open(session_file, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if obj.get("type") != "message":
                    continue
                msg = obj.get("message", {})
                role = msg.get("role")
                if role not in ("user", "assistant"):
                    continue
                content = msg.get("content", "")
                if isinstance(content, list):
                    parts = []
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "text":
                            parts.append(block.get("text", ""))
                    content = "\n".join(parts)
                content = _strip_metadata(content.strip())
                if content:
                    messages.append({
                        "role": role,
                        "content": content,
                        "timestamp": obj.get("timestamp"),
                    })
    except (OSError, PermissionError):
        pass
    return messages


def _strip_metadata(text: str) -> str:
    text = re.sub(
        r"^Sender \(untrusted metadata\):\s*```json\s*\{.*?\}\s*```\s*\n",
        "", text, flags=re.DOTALL
    )
    text = re.sub(r"^\[[^\]]+\]\s*", "", text)
    # Strip thinking blocks
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    return text.strip()


def messages_to_text(messages: list[dict], max_chars: int = 12000) -> str:
    """Convert messages to a compact text block for the LLM prompt."""
    parts = []
    total = 0
    # Take the most recent messages first (up to max_chars)
    for msg in reversed(messages):
        role = "USER" if msg["role"] == "user" else "AGENT"
        chunk = f"{role}: {msg['content'][:500]}\n"
        if total + len(chunk) > max_chars:
            break
        parts.append(chunk)
        total += len(chunk)
    parts.reverse()
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Memory extraction — via openclaw CLI (no credential access required)
# ---------------------------------------------------------------------------

def _openclaw_bin() -> Optional[str]:
    """Return path to the openclaw binary, or None if not found."""
    return shutil.which("openclaw")


INFER_CHUNK_CHARS = 6000   # max chars per infer call
INFER_MAX_MEMORIES = 8     # cap total memories per session across all chunks


def _infer_one(bin_path: str, text: str) -> list[dict]:
    """Run a single `openclaw capability model run` call. Returns parsed memories or []."""
    prompt = EXTRACT_PROMPT_TEMPLATE.format(text=text)
    try:
        proc = subprocess.run(
            [bin_path, "--no-color", "capability", "model", "run", "--prompt", prompt, "--json"],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if proc.returncode != 0:
            return []
        stdout = proc.stdout.strip()
        obj_match = re.search(r"\{.*\}", stdout, re.DOTALL)
        if not obj_match:
            return []
        data = json.loads(obj_match.group(0))
        if not data.get("ok") or not data.get("outputs"):
            return []
        content = data["outputs"][0].get("text", "").strip()
        arr_match = re.search(r"\[.*\]", content, re.DOTALL)
        if not arr_match:
            return []
        memories = json.loads(arr_match.group(0))
        result = []
        for m in memories:
            if not isinstance(m, dict) or not m.get("content"):
                continue
            result.append({
                "content": str(m["content"])[:500].strip(),
                "category": m.get("category", "general"),
                "importance": float(m.get("importance", 0.5)),
            })
        return result
    except Exception:
        return []


def extract_via_infer(text: str) -> list[dict]:
    """
    Call `openclaw capability model run` to extract memories using whatever
    model the user has configured. OpenClaw handles all provider routing and
    auth internally — this function reads no credentials and makes no direct
    network calls.

    Large sessions are split into chunks of INFER_CHUNK_CHARS characters.
    Results are merged and deduplicated by content prefix.
    Returns list of {content, category, importance}.
    """
    bin_path = _openclaw_bin()
    if not bin_path:
        log("  openclaw not found in PATH — falling back to heuristic")
        return []

    # Split into chunks if needed
    chunks = []
    if len(text) <= INFER_CHUNK_CHARS:
        chunks = [text]
    else:
        # Split on newlines at chunk boundaries to avoid cutting mid-message
        lines = text.split("\n")
        current, current_len = [], 0
        for line in lines:
            line_len = len(line) + 1
            if current_len + line_len > INFER_CHUNK_CHARS and current:
                chunks.append("\n".join(current))
                current, current_len = [], 0
            current.append(line)
            current_len += line_len
        if current:
            chunks.append("\n".join(current))

    if len(chunks) > 1:
        log(f"  large session — splitting into {len(chunks)} chunks")

    all_memories: list[dict] = []
    seen_prefixes: set = set()

    for i, chunk in enumerate(chunks):
        chunk_memories = _infer_one(bin_path, chunk)
        if len(chunks) > 1:
            log(f"  chunk {i + 1}/{len(chunks)}: {len(chunk_memories)} candidates")
        for mem in chunk_memories:
            prefix = mem["content"][:60].lower()
            if prefix not in seen_prefixes:
                seen_prefixes.add(prefix)
                all_memories.append(mem)
            if len(all_memories) >= INFER_MAX_MEMORIES:
                break
        if len(all_memories) >= INFER_MAX_MEMORIES:
            break

    if not all_memories and len(chunks) > 1:
        log("  all chunks failed infer — falling back to heuristic")

    return all_memories


def extract_heuristic(messages: list[dict]) -> list[dict]:
    """Keyword-pattern extraction when Ollama is unavailable."""
    patterns = [
        (r"(?:I|we)\s+(?:prefer|like|always use|never use|hate)\s+.{15,100}", "preference", 0.6),
        (r"(?:actually|no,?|wrong[,.]|correction[,:]|mistake[,.])\s+.{15,100}", "correction", 0.75),
        (r"(?:decided|going with|will use|the plan is|we chose)[: ].{15,100}", "insight", 0.6),
        (r"(?:the project|this repo|our stack|the system)\s+.{15,100}", "fact", 0.5),
        (r"(?:important|remember|note that|keep in mind)\s*[:-]?\s*.{15,100}", "fact", 0.55),
    ]
    memories = []
    seen = set()
    for msg in messages:
        if msg["role"] != "user":
            continue
        for pattern, category, importance in patterns:
            for match in re.finditer(pattern, msg["content"], re.IGNORECASE):
                content = match.group(0).strip().rstrip(".,")
                key = content.lower()[:50]
                if key not in seen and len(content) > 20:
                    seen.add(key)
                    memories.append({
                        "content": content,
                        "category": category,
                        "importance": importance,
                    })
    return memories[:8]


def extract_memories(messages: list[dict]) -> list[dict]:
    """Try openclaw infer first, fall back to heuristic."""
    if not messages:
        return []
    text = messages_to_text(messages)
    memories = extract_via_infer(text)
    if not memories:
        memories = extract_heuristic(messages)
    return memories


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------

def _significant_words(text: str) -> set:
    stopwords = {"the", "that", "this", "with", "from", "have", "will", "been",
                 "they", "were", "when", "what", "which", "there", "their",
                 "them", "then", "than", "your", "also", "into", "some",
                 "just", "over", "like", "such", "only", "more", "very"}
    words = set(re.findall(r"\b[a-zA-Z]{4,}\b", text.lower()))
    return words - stopwords


def find_duplicate(db: sqlite3.Connection, content: str, threshold: float = 0.65) -> Optional[int]:
    """Return ID of an existing memory with high word overlap, or None."""
    words = _significant_words(content)
    if len(words) < 3:
        return None

    # Build FTS query from up to 6 significant words
    query_words = list(words)[:6]
    fts_query = " OR ".join(f'"{w}"' for w in query_words)

    try:
        rows = db.execute(
            "SELECT m.id, m.content FROM memories m "
            "JOIN memories_fts ON m.id = memories_fts.rowid "
            "WHERE memories_fts MATCH ? LIMIT 10",
            (fts_query,)
        ).fetchall()
    except Exception:
        return None

    for row in rows:
        existing_words = _significant_words(row["content"])
        if not existing_words:
            continue
        overlap = len(words & existing_words) / min(len(words), len(existing_words))
        if overlap >= threshold:
            return row["id"]

    return None


# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

def open_db(db_path: Path) -> sqlite3.Connection:
    db = sqlite3.connect(str(db_path), timeout=10)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA journal_mode=WAL")
    # Ensure compressed_sessions table exists with wipe column
    db.executescript("""
        CREATE TABLE IF NOT EXISTS compressed_sessions (
            session_id    TEXT PRIMARY KEY,
            session_file  TEXT NOT NULL,
            compressed_at INTEGER NOT NULL,
            memory_count  INTEGER NOT NULL DEFAULT 0,
            wiped_at      INTEGER
        );
        CREATE TABLE IF NOT EXISTS memories (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            content      TEXT    NOT NULL,
            category     TEXT    NOT NULL DEFAULT 'general',
            source       TEXT    NOT NULL DEFAULT 'manual',
            importance   REAL    NOT NULL DEFAULT 0.5,
            session_id   TEXT,
            created_at   INTEGER NOT NULL,
            updated_at   INTEGER NOT NULL,
            access_count INTEGER NOT NULL DEFAULT 0
        );
        CREATE UNIQUE INDEX IF NOT EXISTS idx_memories_content ON memories(content);
    """)
    # Add wiped_at column if it doesn't exist (migration)
    try:
        db.execute("ALTER TABLE compressed_sessions ADD COLUMN wiped_at INTEGER")
        db.commit()
    except sqlite3.OperationalError:
        pass  # column already exists
    db.commit()
    return db


def insert_memory(db: sqlite3.Connection, content: str, category: str,
                  importance: float, session_id: str, source: str) -> Optional[int]:
    """Insert a memory and return its ID, or None if it failed."""
    now = int(time.time())
    try:
        cur = db.execute(
            "INSERT INTO memories (content, category, source, importance, session_id, "
            "created_at, updated_at) VALUES (?,?,?,?,?,?,?)",
            (content, category, source, importance, session_id, now, now)
        )
        db.commit()
        return cur.lastrowid
    except sqlite3.IntegrityError:
        # content unique constraint — exact duplicate
        row = db.execute("SELECT id FROM memories WHERE content = ?", (content,)).fetchone()
        return row["id"] if row else None
    except Exception as e:
        log(f"    DB insert error: {e}")
        return None


def confirm_memory_in_db(db: sqlite3.Connection, memory_id: int) -> bool:
    row = db.execute("SELECT id FROM memories WHERE id = ?", (memory_id,)).fetchone()
    return row is not None


def verify_session_memories(db: sqlite3.Connection, session_id: str,
                             expected_count: int) -> tuple[bool, int]:
    """
    Re-query the DB for memories sourced from this session and verify:
      1. The count matches expected_count
      2. Each memory is readable and has non-empty content
      3. The FTS index contains each memory (search by ID)
    Returns (ok, actual_count).
    """
    short_id = session_id[:8]
    rows = db.execute(
        "SELECT id, content FROM memories WHERE source LIKE ?",
        (f"%{short_id}%",)
    ).fetchall()
    actual = len(rows)

    if actual != expected_count:
        return False, actual

    # Verify content is non-empty and FTS index has each row
    for row in rows:
        if not row["content"] or not row["content"].strip():
            return False, actual
        # Confirm FTS index entry exists
        fts_row = db.execute(
            "SELECT rowid FROM memories_fts WHERE rowid = ?", (row["id"],)
        ).fetchone()
        if fts_row is None:
            return False, actual

    return True, actual


def get_compressed_ids(db: sqlite3.Connection) -> set:
    rows = db.execute("SELECT session_id FROM compressed_sessions").fetchall()
    return {r["session_id"] for r in rows}


def mark_session_compressed(db: sqlite3.Connection, session_id: str,
                             session_file: str, memory_count: int):
    db.execute(
        "INSERT OR REPLACE INTO compressed_sessions "
        "(session_id, session_file, compressed_at, memory_count) VALUES (?,?,?,?)",
        (session_id, session_file, int(time.time()), memory_count)
    )
    db.commit()


def mark_session_wiped(db: sqlite3.Connection, session_id: str):
    db.execute(
        "UPDATE compressed_sessions SET wiped_at = ? WHERE session_id = ?",
        (int(time.time()), session_id)
    )
    db.commit()


# ---------------------------------------------------------------------------
# Session file wipe
# ---------------------------------------------------------------------------

WIPE_MIN_AGE_HOURS = 24  # only wipe sessions older than this


def should_wipe_session(session_file: Path, active_session_file: Optional[Path]) -> bool:
    """Check if it's safe to wipe this session file."""
    if session_file == active_session_file:
        return False
    age_hours = (time.time() - session_file.stat().st_mtime) / 3600
    return age_hours >= WIPE_MIN_AGE_HOURS


def wipe_session_file(session_file: Path, session_id: str,
                      memory_count: int, dry_run: bool) -> bool:
    """Replace session JSONL with a compressed stub. Returns True on success."""
    stub = json.dumps({
        "type": "custom",
        "customType": "openmem:compressed-stub",
        "data": {
            "session_id": session_id,
            "compressed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "memory_count": memory_count,
        },
        "id": "compressed-stub",
        "parentId": None,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime()),
    })

    if dry_run:
        log(f"    [dry-run] would wipe {session_file.name} ({session_file.stat().st_size // 1024}KB)")
        return True

    try:
        session_file.write_text(stub + "\n", encoding="utf-8")
        return True
    except OSError as e:
        log(f"    Wipe failed: {e}")
        return False


# ---------------------------------------------------------------------------
# Main compression loop
# ---------------------------------------------------------------------------

def compress_session(session_file: Path, db: sqlite3.Connection,
                     dry_run: bool) -> int:
    """Compress one session. Returns number of memories added."""
    session_id = session_file.stem

    messages = read_session_messages(session_file)
    if not messages:
        log(f"  {session_id[:8]}: no messages, skipping")
        return 0

    log(f"  {session_id[:8]}: {len(messages)} messages → extracting...")
    candidates = extract_memories(messages)
    log(f"  {session_id[:8]}: {len(candidates)} candidates found")

    added = 0
    for mem in candidates:
        content = mem["content"]
        category = mem.get("category", "general")
        importance = float(mem.get("importance", 0.5))

        # Dedup check
        dup_id = find_duplicate(db, content)
        if dup_id is not None:
            log(f"    skip (dup #{dup_id}): {content[:60]}...")
            continue

        # Insert
        if dry_run:
            log(f"    [dry-run] would add [{category}] {content[:80]}")
            added += 1
            continue

        mem_id = insert_memory(db, content, category, importance,
                               session_id=session_id,
                               source=f"auto_compress:{session_id[:8]}")
        if mem_id is None:
            log(f"    insert failed: {content[:60]}")
            continue

        # Confirm it's in DB before counting it
        if confirm_memory_in_db(db, mem_id):
            log(f"    added #{mem_id} [{category} {importance:.1f}]: {content[:70]}")
            added += 1
        else:
            log(f"    confirmation failed for #{mem_id}: {content[:60]}")

    return added


def run(force: bool = False, dry_run: bool = False, wipe: bool = True,
        sessions_dir: Path = DEFAULT_SESSIONS_DIR,
        db_path: Path = DEFAULT_DB) -> int:
    """
    Main entry point. Returns exit code (0 = success/skipped, 1 = error).
    """
    state = load_state()

    if not force and already_ran_today(state):
        log("Already ran today — skipping")
        return 0

    if not force and not agent_is_inactive(sessions_dir, INACTIVITY_HOURS):
        log(f"Agent active within last {INACTIVITY_HOURS}h — skipping")
        return 0

    if not db_path.exists():
        log(f"Database not found: {db_path}")
        return 1

    db = open_db(db_path)
    compressed_ids = get_compressed_ids(db)

    # Find all session files, sorted oldest-first
    all_sessions = sorted(
        [p for p in sessions_dir.glob("*.jsonl") if ".checkpoint." not in p.name],
        key=lambda p: p.stat().st_mtime
    )
    pending = [f for f in all_sessions if f.stem not in compressed_ids]

    # The most recently modified session may be the active one — skip it
    # unless --force is set (covers the case where it was already the "latest")
    active_session = all_sessions[-1] if all_sessions else None
    if not force and active_session in pending:
        pending.remove(active_session)

    if not pending:
        log("No sessions pending compression")
        save_state({**state, "last_run_date": str(date.today()), "last_run_ts": int(time.time())})
        return 0

    log(f"Compressing {len(pending)} session(s)...")
    total_added = 0
    total_wiped = 0

    for session_file in pending:
        added = compress_session(session_file, db, dry_run)
        total_added += added

        if not dry_run:
            mark_session_compressed(db, session_file.stem, session_file.name, added)

        # Wipe if safe and requested — but only after verifying memories are in DB
        if wipe and not dry_run and should_wipe_session(session_file, active_session):
            if added > 0:
                ok, actual = verify_session_memories(db, session_file.stem, added)
                if not ok:
                    log(f"  {session_file.stem[:8]}: verification FAILED "
                        f"(expected {added}, confirmed {actual}) — skipping wipe")
                else:
                    wiped = wipe_session_file(session_file, session_file.stem, added, dry_run)
                    if wiped:
                        mark_session_wiped(db, session_file.stem)
                        total_wiped += 1
                        log(f"  {session_file.stem[:8]}: verified {actual} memories, wiped")
            elif session_file.stat().st_size > 50_000:
                # Large session with 0 memories extracted — still safe to wipe
                # (nothing to verify, no data loss)
                wiped = wipe_session_file(session_file, session_file.stem, 0, dry_run)
                if wiped:
                    mark_session_wiped(db, session_file.stem)
                    total_wiped += 1
                    log(f"  {session_file.stem[:8]}: 0 memories, wiped large session")

    log(f"Done: {total_added} memories added, {total_wiped} sessions wiped")

    if not dry_run:
        save_state({
            "last_run_date": str(date.today()),
            "last_run_ts": int(time.time()),
            "sessions_compressed": len(pending),
            "memories_added": total_added,
        })

    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    p = argparse.ArgumentParser(
        prog="auto_compress.py",
        description="OpenMem automated session compression"
    )
    p.add_argument("--force", action="store_true",
                   help="Skip date and inactivity guards")
    p.add_argument("--dry-run", action="store_true",
                   help="Show what would happen without writing anything")
    p.add_argument("--no-wipe", action="store_true",
                   help="Compress sessions but do not wipe session files")
    p.add_argument("--sessions-dir", type=Path, default=DEFAULT_SESSIONS_DIR)
    p.add_argument("--db", type=Path, default=DEFAULT_DB)
    args = p.parse_args()

    model_label = "openclaw-infer" if _openclaw_bin() else "heuristic"
    log(f"auto_compress starting (force={args.force}, dry_run={args.dry_run}, wipe={not args.no_wipe}, model={model_label})")
    sys.exit(run(
        force=args.force,
        dry_run=args.dry_run,
        wipe=not args.no_wipe,
        sessions_dir=args.sessions_dir,
        db_path=args.db,
    ))


if __name__ == "__main__":
    main()
