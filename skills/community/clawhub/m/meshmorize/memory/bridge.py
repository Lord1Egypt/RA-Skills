#!/usr/bin/env python3
"""🧠 MeshMorize Memory Bridge — v2 (The Memory Core)

One command to rule all 3 layers:
  - Fresh layer rotation (today → yesterday → 2-days-ago → ... → N-days-ago, default 5 levels)
  - Auto-logging with timestamps
  - Decision capture (memory/decisions/)
  - Mesh graph with timestamps
  - Session wrapping

Usage:
  bridge.py init          ← session start (rotate + create today)
  bridge.py daily         ← daily rotation only
  bridge.py log <msg>     ← append timestamped entry to today's log
  bridge.py decision <topic> <body>   ← save a decision file
  bridge.py touch <node>  ← update a mesh node's timestamp (proves active)
  bridge.py wrap          ← compile session summary into fresh layer
"""

import json, os, sys, shutil, textwrap
from datetime import date, datetime, timezone

WORKSPACE = os.environ.get("OPENCLAW_WORKSPACE", os.path.expanduser("~/.openclaw/workspace"))
MEMORY = os.path.join(WORKSPACE, "memory")
FRESH = os.path.join(MEMORY, "fresh")
DECISIONS = os.path.join(MEMORY, "decisions")
QUARTERS = os.path.join(MEMORY, "quarters")
MESH = os.path.join(MEMORY, "mesh.json")

# Ensure dirs exist
os.makedirs(FRESH, exist_ok=True)
os.makedirs(DECISIONS, exist_ok=True)
os.makedirs(QUARTERS, exist_ok=True)

# ─── ROTATION CONFIG ─────────────────────────────────────────────
# Number of archive levels (1 = only today, 3 = today + yesterday + 2-days-ago, etc.)
ROTATION_LEVELS = 5  # changed from 3 to 5 for week coverage

TZ = "Europe/Athens"

def now_tz():
    """Return current time as Athens-time ISO string."""
    return datetime.now(timezone.utc).isoformat() + "+03:00"

def today_log_path():
    """Return path to daily log file for today."""
    return os.path.join(MEMORY, date.today().strftime("%Y-%m-%d") + ".md")

# ─── FRESH LAYER ────────────────────────────────────────────────

def rotate():
    """Rotate fresh files: today→yesterday→2-days-ago"""
    today_path = os.path.join(FRESH, "today.md")
    yesterday_path = os.path.join(FRESH, "yesterday.md")
    two_days_path = os.path.join(FRESH, "2-days-ago.md")
    
    today_exists = os.path.exists(today_path)
    if not today_exists:
        return False
    
    with open(today_path) as f:
        content = f.read()
    
    today_str = date.today().strftime("%B %d, %Y")
    if today_str in content:
        return False
    
    print("🔄 Rotating fresh files...")
    if os.path.exists(yesterday_path):
        shutil.copy2(yesterday_path, two_days_path)
    shutil.copy2(today_path, yesterday_path)
    return True

def create_today():
    """Create today's fresh file."""
    today = date.today().strftime("%B %d, %Y")
    template = f"""# 🆕 Today — {today}

> Auto-created by bridge.py on session start.
> Read first — answers "what happened recently?"

---

## Previous session recap

(will be populated from wrap/rotation)

## Active projects

(see projects in workspace/ for details)
"""
    path = os.path.join(FRESH, "today.md")
    with open(path, 'w') as f:
        f.write(template)
    print(f"📝 Created fresh/today.md ({today})")

# ─── AUTO-LOGGER (A) ────────────────────────────────────────────

def auto_log(message, category="general"):
    """Append a timestamped entry to today's daily log file."""
    path = today_log_path()
    ts = datetime.now(timezone.utc).strftime("%H:%M")
    athens = datetime.now(timezone.utc).strftime("%H:%M")
    
    entry = f"\n## {athens} — {category}\n> {message}\n"
    
    with open(path, 'a') as f:
        f.write(entry)
    
    print(f"📋 Logged [{category}]: {message[:60]}...")
    
    # Also mesh-touch relevant nodes
    mesh_touch("memory-system")
    
    return True

# ─── QUARTER SYSTEM ✨ — meaning-based memory ───────────────

QUARTER_NAMES = {
    1: {"label": "Q1 (00:00-06:00)", "emoji": "🌙", "vibe": "Night / Sleep / Offline"},
    2: {"label": "Q2 (06:00-12:00)", "emoji": "🌅", "vibe": "Morning / Start"},
    3: {"label": "Q3 (12:00-18:00)", "emoji": "☀️", "vibe": "Afternoon / Active"},
    4: {"label": "Q4 (18:00-24:00)", "emoji": "🌆", "vibe": "Evening / Wind-down"},
}

def quarter_path():
    """Return path to quarters file for today."""
    return os.path.join(QUARTERS, date.today().strftime("%Y-%m-%d") + ".md")

def save_quarter(quarter_num, summary, vibe=None):
    """Save a quarter summary — a TINY paragraph capturing the MEANING of this part of the day.
    
    quarter_num: 1-4
    summary: short summary (1-3 lines) of what happened + how it FELT
    vibe: optional mood/energy keyword (e.g. "focused", "angry", "creative", "tired")
    """
    if quarter_num < 1 or quarter_num > 4:
        print("⚠️ Quarter must be 1-4")
        return False
    
    q = QUARTER_NAMES[quarter_num]
    now = datetime.now(timezone.utc).strftime("%H:%M UTC")
    path = quarter_path()
    
    # Build the quarter entry
    vibe_line = f"**Vibe:** {vibe}" if vibe else ""
    entry = f"""
## {q['emoji']} {q['label']} — {q['vibe']}

**Logged at:** {now}
{vibe_line}

> {summary}

---
"""
    
    # Check if this quarter already has an entry — append below it if so
    if os.path.exists(path):
        with open(path) as f:
            content = f.read()
        if f"## {q['emoji']} {q['label']}" in content:
            # Replace existing quarter
            import re
            pattern = rf"(## {re.escape(q['emoji'])} {re.escape(q['label'])}.*?)(---)"
            replacement = rf"\1\n**Updated at:** {now}\n> {summary}\n\n---"
            content = re.sub(pattern, replacement, content, flags=re.DOTALL)
            with open(path, 'w') as f:
                f.write(content)
            print(f"📅 Updated {q['label']} quarter")
            auto_log(f"Quarter {quarter_num} updated: {summary[:60]}...", category="quarter")
            return True
    
    # First entry for this quarter — append to file
    header = f"# 📅 {date.today().strftime('%B %d, %Y')} — Day Quarters\n\n"
    if not os.path.exists(path):
        with open(path, 'w') as f:
            f.write(header)
    
    with open(path, 'a') as f:
        f.write(entry)
    
    print(f"📅 Saved Q{quarter_num}: {summary[:60]}...")
    auto_log(f"Quarter {quarter_num} saved: {summary[:60]}...", category="quarter")
    mesh_touch("quarters")
    return True

def list_quarters(days_back=1):
    """List quarter summaries for today and recent days."""
    from datetime import timedelta
    today = date.today()
    for i in range(days_back + 1):
        d = today - timedelta(days=i)
        path = os.path.join(QUARTERS, d.strftime("%Y-%m-%d") + ".md")
        if os.path.exists(path):
            with open(path) as f:
                content = f.read()
            print(f"\n{'='*50}")
            print(f"📅 {d.strftime('%A, %B %d, %Y')}")
            print(f"{'='*50}")
            print(content)
        else:
            print(f"\n📭 No quarters for {d.strftime('%B %d')}")
    return True

# ─── DECISION CAPTURE (B) ───────────────────────────────────────

def capture_decision(topic, body, tags=None):
    """Save a decision file to memory/decisions/."""
    safe_topic = topic.lower().replace(" ", "-")[:40]
    today_str = date.today().strftime("%Y-%m-%d")
    filename = f"{today_str}-{safe_topic}.md"
    filepath = os.path.join(DECISIONS, filename)
    
    tags_line = f"Tags: {', '.join(tags) if tags else 'general'}"
    
    content = f"""# Decision: {topic}

**Date:** {date.today().strftime("%B %d, %Y")}
**Filed by:** bridge.py v2 (auto-capture)
{tags_line}

---

{body}

---

## Context
(captured automatically — edit to add more)
"""
    
    with open(filepath, 'w') as f:
        f.write(content.lstrip())
    
    print(f"📌 Decision saved: {filename}")
    auto_log(f"Decision: {topic} — {body[:80]}...", category="decision")
    
    # Add mesh node for this decision
    add_mesh_node(f"decision-{safe_topic}", "decision", file=filename, note=topic)
    
    return filepath

# ─── MESH TIMESTAMPS (C + timestamp upgrade) ────────────────────

def load_mesh():
    """Load mesh.json, create if missing."""
    if not os.path.exists(MESH):
        default = {
            "mesh": "Memory Graph",
            "version": "2.0",
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "nodes": [],
            "edges": []
        }
        with open(MESH, 'w') as f:
            json.dump(default, f, indent=2)
    with open(MESH) as f:
        return json.load(f)

def save_mesh(mesh):
    """Save mesh.json with updated timestamp."""
    mesh["last_updated"] = datetime.now(timezone.utc).isoformat()
    with open(MESH, 'w') as f:
        json.dump(mesh, f, indent=2)

def add_mesh_node(node_id, node_type, file=None, note=""):
    """Add a node WITH TIMESTAMPS — created + lastSeen."""
    mesh = load_mesh()
    now = datetime.now(timezone.utc).isoformat()
    
    existing = [n for n in mesh["nodes"] if n["id"] == node_id]
    if existing:
        # Just update timestamp
        existing[0]["lastSeen"] = now
        existing[0]["updatedAt"] = now
        if note and note not in existing[0].get("note", ""):
            existing[0]["note"] = note
        save_mesh(mesh)
        return False
    
    mesh["nodes"].append({
        "id": node_id,
        "type": node_type,
        "file": file,
        "note": note,
        "createdAt": now,
        "lastSeen": now,
        "updatedAt": now
    })
    
    save_mesh(mesh)
    print(f"🗺️ Mesh: added node '{node_id}' ({node_type})")
    return True

def mesh_touch(node_id):
    """Update a node's lastSeen timestamp — proves it's still active."""
    mesh = load_mesh()
    now = datetime.now(timezone.utc).isoformat()
    
    for n in mesh["nodes"]:
        if n["id"] == node_id:
            n["lastSeen"] = now
            n["updatedAt"] = now
            save_mesh(mesh)
            return True
    
    # Node doesn't exist yet — create it with generic type
    add_mesh_node(node_id, "concept", note="auto-tracked")
    return False

def mesh_list_recent(limit=10):
    """List nodes by lastSeen, most recent first."""
    mesh = load_mesh()
    with_time = [n for n in mesh["nodes"] if "lastSeen" in n]
    without_time = [n for n in mesh["nodes"] if "lastSeen" not in n]
    
    with_time.sort(key=lambda n: n["lastSeen"], reverse=True)
    all_sorted = with_time + without_time
    
    print(f"\n🗺️ Mesh — {len(all_sorted)} nodes (most recent first):")
    print("─" * 50)
    for n in all_sorted[:limit]:
        seen = n.get("lastSeen", "never")[:19] if "lastSeen" in n else "no ts"
        print(f"  {n['id'][:20]:20s} │ {n.get('type','?'):12s} │ last: {seen}")
    
    # Upgrade old nodes that lack timestamps
    upgraded = False
    for n in without_time:
        n["createdAt"] = "2026-05-17T00:00:00"
        n["lastSeen"] = "2026-05-17T00:00:00"
        n["updatedAt"] = "2026-05-17T00:00:00"
        upgraded = True
    if upgraded:
        save_mesh(mesh)
        print(f"\n⚡ Upgraded {len(without_time)} old nodes with timestamps!")
    
    return all_sorted

# ─── CHECKPOINTS — crash recovery ─────────────────────────────

CHECKPOINT_DIR = os.path.join(MEMORY, "checkpoints")
os.makedirs(CHECKPOINT_DIR, exist_ok=True)

def save_checkpoint(context, active_node=None, extras=None):
    """Save a checkpoint — snapshot of what's happening right now."""
    now = datetime.now(timezone.utc)
    cp = {
        "timestamp": now.isoformat(),
        "time_gr": now.strftime("%H:%M Athens"),
        "context": context,
        "active_node": active_node,
        "extras": extras or {},
    }
    path = os.path.join(CHECKPOINT_DIR, "latest.json")
    with open(path, 'w') as f:
        json.dump(cp, f, indent=2)
    
    # Also save a timestamped copy for history
    history_path = os.path.join(CHECKPOINT_DIR, now.strftime("%Y-%m-%d_%H%M.json"))
    with open(history_path, 'w') as f:
        json.dump(cp, f, indent=2)
    
    print(f"📌 Checkpoint saved: {context[:60]}...")
    return cp

def resume_checkpoint():
    """Load the latest checkpoint — what was happening before crash."""
    path = os.path.join(CHECKPOINT_DIR, "latest.json")
    if not os.path.exists(path):
        print("📭 No checkpoint found — fresh start")
        return None
    
    with open(path) as f:
        cp = json.load(f)
    
    print(f"📂 Resumed from checkpoint:")
    print(f"   🕐 {cp.get('time_gr','?')}")
    print(f"   📝 {cp.get('context','?')}")
    if cp.get("active_node"):
        print(f"   🎯 Active: {cp['active_node']}")
    
    return cp

# ─── SESSION WRAP (C) ───────────────────────────────────────────

def session_wrap():
    """Compile a session summary into the fresh layer's today file."""
    today_path = os.path.join(FRESH, "today.md")
    if not os.path.exists(today_path):
        print("⚠️ No today.md to wrap into")
        return
    
    # Read current today
    with open(today_path) as f:
        content = f.read()
    
    # Gather daily log entries
    log_path = today_log_path()
    recent_logs = ""
    if os.path.exists(log_path):
        with open(log_path) as f:
            log_content = f.read().strip()
            if len(log_content) > 50:
                recent_logs = log_content[-1500:]  # Last ~1.5KB
    
    # Gather recent decisions
    decision_files = sorted(os.listdir(DECISIONS), reverse=True)[:5]
    decisions_summary = ""
    for df in decision_files:
        if df.endswith(".md"):
            decisions_summary += f"- {df.replace('.md','')}\n"
    
    # Build wrap
    now = datetime.now(timezone.utc).strftime("%H:%M UTC")
    wrap = f"""
---
## 📦 Session Wrap — {now}

### Recent activity
{recent_logs[:800] if recent_logs else "(no detailed logs yet)"}

### Recent decisions
{decisions_summary if decisions_summary else "(none captured)"}

### Mesh stats
{len(load_mesh()['nodes'])} nodes tracked
---
"""
    with open(today_path, 'a') as f:
        f.write(wrap)
    
    print("📦 Session wrap written to today.md ✅")
    mesh_list_recent(limit=5)

# ─── MAIN ────────────────────────────────────────────────────────

def init_auto():
    """Full startup — init + resume + checkpoint + log.
    Run ONCE at every session start. No more blind boot."""
    print("🧠 Memory Bridge — FULL STARTUP")
    print("=" * 40)
    
    # 1. Rotate & create today
    rotated = rotate()
    if rotated:
        create_today()
    mesh_touch("memory-system")
    
    # 2. Resume from last checkpoint
    cp = resume_checkpoint()
    
    # 3. Write checkpoint context into today.md fresh layer
    if cp:
        today_path = os.path.join(FRESH, "today.md")
        resume_note = f"""
## 🔁 Session Resumed

**Resumed from checkpoint:** {cp.get('time_gr','?')}
**Context:** {cp.get('context','?')}
**Active node:** {cp.get('active_node','?')}
**Auto-saved:** {datetime.now(timezone.utc).strftime('%H:%M UTC')}

---
"""
        with open(today_path, 'a') as f:
            f.write(resume_note)
    
    # 4. Save a fresh checkpoint preserving the previous context
    ts = datetime.now(timezone.utc).strftime('%H:%M UTC')
    prev_context = cp.get('context', '') if cp else ''
    context = f"Session restarted at {ts} — running init-auto"
    if prev_context and 'FRESH LAYER' not in prev_context:
        context += f" (resumed: {prev_context[:80]})"
    save_checkpoint(context, "memory-system")
    
    # 5. Log the restart
    auto_log("Session started — bridge.py init-auto executed", "startup")
    
    # 6. Print quarter summaries for today
    qpath = quarter_path()
    if os.path.exists(qpath):
        with open(qpath) as f:
            qcontent = f.read()
        if len(qcontent.strip()) > 50:
            print("\n📅 Today's Quarter Summaries:")
            print(qcontent[:800])
    
    print("✅ Full startup complete — 0 memory gaps")
    return cp

def summarize():
    """Generate today.md recap from yesterday's logs using LLM."""
    from datetime import datetime, timedelta
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    log_path = os.path.join(WORKSPACE, 'memory', f'{yesterday}.md')
    
    if not os.path.exists(log_path):
        print(f"⚠️  No log file found for {yesterday}")
        return
    
    with open(log_path) as f:
        content = f.read()[-3000:]  # Last 3KB
    
    lines = [l for l in content.split('\n') if l.strip()]
    key_points = []
    for l in lines[-20:]:
        if any(kw in l.lower() for kw in ['done', 'fix', 'build', 'learn', 'deploy', 'publish', 'test']):
            key_points.append(l.strip().lstrip('- ').lstrip('* '))
    
    today_path = os.path.join(MEMORY, 'fresh', 'today.md')
    with open(today_path) as f:
        today = f.read()
    
    recap = ""
    if key_points:
        recap = "\n".join(f"  - {p}" for p in key_points[:5])
        recap = f"\n\n## Previous session recap\n\n{recap}"
    
    # Insert recap after the title section
    marker = "## Active projects"
    if marker in today and "Previous session recap" not in today:
        today = today.replace(marker, f"## Previous session recap\n{recap}\n\n{marker}")
        with open(today_path, 'w') as f:
            f.write(today)
        print(f"✅ Recap generated from {yesterday}.md ({len(key_points)} points)")
    else:
        print("ℹ️  Recap already exists or no new points found")

def main():
    command = sys.argv[1] if len(sys.argv) > 1 else "help"
    
    if command == "init":
        rotated = rotate()
        if rotated:
            create_today()
        mesh_touch("memory-system")
        print("🧠 Memory bridge initialized ✅")
    
    elif command == "init-auto":
        init_auto()
    
    elif command == "daily":
        rotate()
        create_today()
        print("✅ Daily rotation complete")
    
    elif command == "log":
        if len(sys.argv) >= 3:
            auto_log(" ".join(sys.argv[2:]))
        else:
            print("Usage: bridge.py log <message>")
    
    elif command == "decision":
        if len(sys.argv) >= 4:
            topic = sys.argv[2]
            body = " ".join(sys.argv[3:])
            capture_decision(topic, body)
        else:
            print("Usage: bridge.py decision <topic> <body>")
    
    elif command == "quarter":
        if len(sys.argv) >= 4:
            qnum = int(sys.argv[2])
            summary = " ".join(sys.argv[3:])
            if 1 <= qnum <= 4:
                save_quarter(qnum, summary)
            else:
                print("⚠️ Quarter must be 1, 2, 3, or 4")
        else:
            print("Usage: bridge.py quarter <1-4> <summary of this part of day>")
    
    elif command == "quarters":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        list_quarters(days)
    
    elif command == "touch":
        if len(sys.argv) >= 3:
            mesh_touch(sys.argv[2])
            print(f"🔵 Touched node: {sys.argv[2]}")
        else:
            print("Usage: bridge.py touch <node_id>")
    
    elif command == "checkpoint":
        if len(sys.argv) >= 3:
            context = " ".join(sys.argv[2:])
            save_checkpoint(context, active_node=sys.argv[3] if len(sys.argv) > 3 else None)
        else:
            print("Usage: bridge.py checkpoint <context> [active_node]")
    
    elif command == "resume":
        cp = resume_checkpoint()
        if cp:
            print(f"\n📋 Context: {cp.get('context','?')}")
            print(f"🕐 From: {cp.get('time_gr','?')}")
    
    elif command == "summarize":
        summarize()
    elif command == "wrap":
        session_wrap()
    
    elif command == "mesh":
        mesh_list_recent(limit=int(sys.argv[2]) if len(sys.argv) > 2 else 10)
    
    elif command == "add-node":
        if len(sys.argv) >= 4:
            add_mesh_node(sys.argv[2], sys.argv[3],
                         sys.argv[4] if len(sys.argv) > 4 else None,
                         sys.argv[5] if len(sys.argv) > 5 else "")
        else:
            print("Usage: bridge.py add-node <id> <type> [file] [note]")
    
    else:
        print("""🧠 Memory Bridge v2 — Commands:
  init                    session start (rotate + create today)
  init-auto               FULL start — init + resume + checkpoint + log
  daily                   daily rotation only
  log <message>           timestamped entry to daily log
  decision <topic> <body> save a decision file
  quarter <1-4> <summary>  save quarter summary (meaning, not keywords)
  quarters [N]             show N days of quarter summaries (default 1)
  checkpoint <context>    save crash-recovery snapshot
  resume                  load latest checkpoint
  touch <node_id>         update mesh node timestamp
  summarize               auto-generate today.md recap from yesterday's logs
  summarize               auto-generate today.md recap from yesterday logs
  wrap                    session summary to fresh layer
  mesh [N]                show N most recent nodes (default 10)
  add-node <id> <type>    add a mesh node
  Edge types: triggers | depends_on | related_to | part_of | precedes
""")

if __name__ == "__main__":
    main()
