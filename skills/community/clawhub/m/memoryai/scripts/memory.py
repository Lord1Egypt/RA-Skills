#!/usr/bin/env python3
"""MemoryAI — Thin client. All logic on server.

Commands: store, recall, bootstrap, track, save, profile, health
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
    """Track a message. Call on every user/assistant message.

    The brain keeps the context window healthy on its own and signals
    when it's time to save and continue on a clean slate.
    """
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
        print("SAVE_NOW")
        if result.get("should_compress"):
            print("Action: call 'memory.py save' with a short summary of the conversation so far")
    else:
        print("OK")


def main():
    if len(sys.argv) < 2:
        print("MemoryAI — Long-term memory for AI agents")
        print()
        print("Commands:")
        print("  store \"content\" [--type TYPE]  Store a memory")
        print("  recall \"query\" [--depth deep]  Recall memories")
        print("  bootstrap \"task\"               Wake up with context")
        print("  track \"message\" [--role R]     Keep context healthy (per message)")
        print("  save \"summary\"                 Save session context")
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
    }

    if cmd in commands:
        commands[cmd](args)
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        print(f"Available: {', '.join(commands.keys())}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
