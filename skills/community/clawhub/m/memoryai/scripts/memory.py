#!/usr/bin/env python3
"""MemoryAI v2 — Thin client. All logic on server.

Commands: store, recall, bootstrap, save, profile, health
Zero dependencies. Pure stdlib.
"""
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.parent
CONFIG_PATH = SCRIPT_DIR / "config.json"


def _config():
    endpoint = os.environ.get("HM_ENDPOINT", "")
    api_key = os.environ.get("HM_API_KEY", "")
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            cfg = json.load(f)
        endpoint = endpoint or cfg.get("endpoint", "")
        api_key = api_key or cfg.get("api_key", "")
    if not endpoint or not api_key:
        print("Error: Configure endpoint + api_key in config.json or env vars", file=sys.stderr)
        sys.exit(1)
    return endpoint.rstrip("/"), api_key


def _api(method, path, body=None):
    endpoint, key = _config()
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(
        f"{endpoint}{path}",
        data=data,
        method=method,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        err = e.read().decode() if e.fp else str(e.code)
        print(f"Error {e.code}: {err}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Connection failed: {e.reason}", file=sys.stderr)
        sys.exit(1)


def cmd_store(args):
    """Store a memory."""
    content = args[0] if args else ""
    if not content:
        print("Usage: memory.py store \"content\" [--type TYPE] [--tags t1,t2]", file=sys.stderr)
        sys.exit(1)

    body = {"content": content}

    # Parse optional flags
    i = 1
    while i < len(args):
        if args[i] == "--type" and i + 1 < len(args):
            body["memory_type"] = args[i + 1]
            i += 2
        elif args[i] == "--tags" and i + 1 < len(args):
            body["tags"] = [t.strip() for t in args[i + 1].split(",")]
            i += 2
        elif args[i] == "--source" and i + 1 < len(args):
            body["source"] = args[i + 1]
            i += 2
        else:
            i += 1

    result = _api("POST", "/v1/store", body)
    print(f"Stored (id: {result.get('id', '?')})")


def cmd_recall(args):
    """Recall memories."""
    query = args[0] if args else ""
    if not query:
        print("Usage: memory.py recall \"query\" [--limit N] [--depth fast|deep]", file=sys.stderr)
        sys.exit(1)

    body = {"query": query, "depth": "deep", "limit": 5}

    i = 1
    while i < len(args):
        if args[i] == "--limit" and i + 1 < len(args):
            body["limit"] = int(args[i + 1])
            i += 2
        elif args[i] == "--depth" and i + 1 < len(args):
            body["depth"] = args[i + 1]
            i += 2
        elif args[i] == "--since" and i + 1 < len(args):
            body["since"] = args[i + 1]
            i += 2
        else:
            i += 1

    result = _api("POST", "/v1/recall", body)
    memories = result.get("results", [])
    if not memories:
        print("No memories found.")
        return

    for m in memories:
        score = int(m.get("score", 0) * 100)
        mtype = m.get("memory_type", "")
        content = m.get("content", "")
        print(f"[{score}%] [{mtype}] {content}")
        print()


def cmd_bootstrap(args):
    """Bootstrap session — wake up with full context."""
    task = args[0] if args else ""
    body = {"task": task, "mode": "default"}

    i = 1
    while i < len(args):
        if args[i] == "--mode" and i + 1 < len(args):
            body["mode"] = args[i + 1]
            i += 2
        elif args[i] == "--budget" and i + 1 < len(args):
            body["token_budget"] = int(args[i + 1])
            i += 2
        else:
            i += 1

    result = _api("POST", "/v1/bot/guard/bootstrap", body)
    print(result.get("context_block", ""))


def cmd_save(args):
    """Save session context (compact)."""
    content = args[0] if args else ""
    if not content:
        print("Usage: memory.py save \"session summary\"", file=sys.stderr)
        sys.exit(1)

    body = {"content": content}
    if len(args) > 1 and args[1] == "--task":
        body["task_context"] = args[2] if len(args) > 2 else ""

    result = _api("POST", "/v1/context/guard/compact", body)
    status = result.get("status", "done")
    chunks = result.get("chunks_created", 0)
    print(f"Saved ({status}, {chunks} chunks)")


def cmd_profile(args):
    """Get cognitive profile — who is this user?"""
    result = _api("GET", "/v1/personality/cognitive-profile")
    persona = result.get("persona", "Unknown")
    mood = result.get("mood")
    goals = result.get("active_goals", [])
    entities = result.get("top_entities", [])
    procedures = result.get("procedures", [])

    print(f"Persona: {persona}")
    if mood:
        print(f"Mood: {mood.get('current', '?')} (trend: {mood.get('trend', '?')})")
    if goals:
        print(f"Goals: {', '.join(goals[:3])}")
    if entities:
        names = [e["name"] if isinstance(e, dict) else str(e) for e in entities[:5]]
        print(f"Key people/things: {', '.join(names)}")
    if procedures:
        print(f"Procedures: {len(procedures)} known workflows")


def cmd_health(args):
    """Check memory health."""
    result = _api("GET", "/v1/stats")
    total = result.get("total_chunks", 0)
    dna = result.get("dna_chunks", result.get("dna_count", 0))
    print(f"Memories: {total} (DNA: {dna})")
    print(f"Status: healthy")


def cmd_track(args):
    """Track a message in rolling session. Call on every user/assistant message."""
    content = args[0] if args else ""
    if not content:
        print("Usage: memory.py track \"message content\" [--role user|assistant]", file=sys.stderr)
        sys.exit(1)

    role = "user"
    i = 1
    while i < len(args):
        if args[i] == "--role" and i + 1 < len(args):
            role = args[i + 1]
            i += 2
        else:
            i += 1

    result = _api("POST", "/v1/bot/session/message", {
        "message": {"role": role, "content": content},
    })

    if result.get("rotate"):
        print(f"🔄 SESSION ROTATED → {result.get('session_id', '?')}")
        if result.get("should_compress"):
            print(f"   COMPRESS: {result.get('compress_session_id')} ({result.get('compress_message_count', 0)} msgs)")
            print(f"   Action: call 'memory.py save' with old session content")
        print(f"   Context: {result.get('context_message_count', 0)} messages in window")
    else:
        print(f"Session {result.get('session_id', '?')}: {result.get('message_count', 0)}/20")


def cmd_guard(args):
    """Legacy guard check. Use 'sync' instead."""
    cmd_sync(args)


def cmd_sync(args):
    """Unified sync: guard + rolling in 1 call. Called by cron every 5 min."""
    import os
    from pathlib import Path

    # 1. Read token count from sessions.json
    openclaw_dir = Path(os.environ.get("OPENCLAW_DIR", str(Path.home() / ".openclaw")))
    sessions_file = openclaw_dir / "agents" / "main" / "sessions" / "sessions.json"
    estimated_tokens = 0
    max_tokens = 200000
    transcript_path = None

    try:
        with open(sessions_file, encoding="utf-8") as f:
            import json as _json
            sessions = _json.load(f)
            for key, s in sessions.items():
                if "main" in key:
                    estimated_tokens = s.get("totalTokens", 0)
                    max_tokens = s.get("contextTokens", 200000)
                    transcript_path = s.get("sessionFile", "")
                    break
    except Exception:
        pass

    # 2. Read new messages from transcript (if available)
    messages = []
    state_path = Path(os.environ.get("WORKSPACE", str(openclaw_dir / "workspace"))) / "memory" / "sync_state.json"
    state = {"byte_offset": 0, "transcript_path": ""}

    try:
        if state_path.exists():
            with open(state_path, encoding="utf-8") as f:
                state = _json.load(f)
    except Exception:
        pass

    if transcript_path:
        # Resolve full path
        transcript_full = openclaw_dir / "agents" / "main" / "sessions" / transcript_path
        if not transcript_full.exists():
            transcript_full = Path(transcript_path)

        # Detect transcript change (new session)
        if state.get("transcript_path") != str(transcript_full):
            state["byte_offset"] = 0
            state["transcript_path"] = str(transcript_full)

        # Read new lines from offset
        try:
            with open(transcript_full, "rb") as f:
                f.seek(state["byte_offset"])
                new_data = f.read()
                new_offset = state["byte_offset"] + len(new_data)

            if new_data:
                lines = new_data.decode("utf-8", errors="ignore").split("\n")
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        msg = _json.loads(line)
                        if msg.get("role") in ("user", "assistant"):
                            messages.append({
                                "role": msg["role"],
                                "content": msg.get("content", "")[:500],
                            })
                    except Exception:
                        continue
        except Exception:
            new_offset = state["byte_offset"]

    # 3. Call server (1 unified call)
    body = {
        "estimated_tokens": estimated_tokens,
        "max_tokens": max_tokens,
        "messages": messages,
    }

    result = _api("POST", "/v1/bot/session/sync", body)

    # 4. Update state (only after successful call)
    if transcript_path:
        try:
            state_path.parent.mkdir(parents=True, exist_ok=True)
            state["byte_offset"] = new_offset
            with open(state_path, "w", encoding="utf-8") as f:
                _json.dump(state, f)
        except Exception:
            pass

    # 5. Report
    action = result.get("action", "none")
    phase = result.get("phase", "?")
    usage = result.get("usage_percent", 0)

    if action == "rotate":
        print(f"ACTION: rotate")
        print(f"PHASE: {phase}")
        print(f"NEW_SESSION: {result.get('new_session_id', '?')}")
        print(f"ARCHIVED: {result.get('archived_session_id', 'none')}")
        if result.get("message"):
            print(f"MSG: {result['message']}")
    elif action == "compact":
        print(f"ACTION: compact")
        print(f"USAGE: {usage:.1f}%")
        if result.get("message"):
            print(f"MSG: {result['message']}")
    elif action == "warning":
        print(f"ACTION: none")
        print(f"WARNING: {usage:.1f}% — approaching threshold")
    else:
        print(f"ACTION: none")
        health = result.get("context_health", "safe")
        next_rot = result.get("next_rotation_in", "")
        status = f"healthy ({usage:.1f}%)" if usage > 0 else f"phase={phase}"
        if next_rot:
            status += f" | next rotation: {next_rot}"
        print(f"STATUS: {status}")


def main():
    if len(sys.argv) < 2:
        print("MemoryAI v2.0 — Long-term memory for AI agents")
        print()
        print("Commands:")
        print("  store \"content\" [--type TYPE]  Store a memory")
        print("  recall \"query\" [--depth deep]  Recall memories")
        print("  bootstrap \"task\"               Wake up with context")
        print("  save \"summary\"                 Save session context")
        print("  sync                           Sync context (cron, every 5 min)")
        print("  profile                        Get user cognitive profile")
        print("  health                         Check memory health")
        sys.exit(0)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    commands = {
        "store": cmd_store,
        "recall": cmd_recall,
        "bootstrap": cmd_bootstrap,
        "save": cmd_save,
        "profile": cmd_profile,
        "health": cmd_health,
        "track": cmd_track,
        "guard": cmd_guard,
        "sync": cmd_sync,
    }

    if cmd in commands:
        commands[cmd](args)
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        print(f"Available: {', '.join(commands.keys())}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
