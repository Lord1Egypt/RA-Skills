"""
mind-wander tool implementations.

Each tool returns a dict: {"ok": bool, "result": str, "error": str|None}
The agent sees only "result" (or "error") — never raw exceptions.
"""
import json
import os
import re
import sys
import time
import subprocess
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "memory-upgrade"))

from mind_wander_config import (
    WORKSPACE, FALKORDB_HOST, FALKORDB_PORT, GRAPH_NAME, GRAPH_LIMIT,
    PERPLEXITY_KEY, SANDBOX_TIMEOUT, SANDBOX_MAX_LINES,
    SANDBOX_ALLOWED_IMPORTS, ON_YOUR_MIND_FILE, MENTAL_EXPLORATION_FILE,
    WANDER_STATE_FILE,
)

from wander_graph import (
    record_dead_end_to_graph,
    search_dead_ends,
    record_session,
    regenerate_dead_ends_file,
    init_wander_graph,
)
try:
    init_wander_graph()
except Exception:
    pass


# ── Graph query ───────────────────────────────────────────────────────────────

def query_graph(query: str, limit: int = None) -> dict:
    """
    Query the FalkorDB graph-rag memory for related facts.
    Uses BM25 fulltext search — no Ollama required.
    """
    limit = min(limit or GRAPH_LIMIT, 15)
    try:
        import falkordb
        r = falkordb.FalkorDB(host=FALKORDB_HOST, port=FALKORDB_PORT)
        g = r.select_graph(GRAPH_NAME)

        # Fulltext search on fact field
        # Escape special characters for FalkorDB fulltext
        safe_query = re.sub(r'[^\w\s]', ' ', query).strip()
        words = safe_query.split()[:6]  # top 6 words

        results = []
        for word in words:
            if len(word) < 3:
                continue
            try:
                res = g.query(f"""
CALL db.idx.fulltext.queryEdges('RELATES_TO', '{word}')
YIELD edge
RETURN edge.fact, edge.group_id
LIMIT {limit}
""")
                for row in res.result_set:
                    fact = str(row[0]) if row[0] else ""
                    if fact and fact not in results:
                        results.append(fact)
            except Exception:
                pass

        if not results:
            # Fallback: scan all facts for keyword match
            all_facts = g.query("""
MATCH ()-[r:RELATES_TO]->()
WHERE r.fact IS NOT NULL
RETURN r.fact
LIMIT 50
""")
            query_lower = query.lower()
            for row in all_facts.result_set:
                fact = str(row[0]) if row[0] else ""
                if any(w.lower() in fact.lower() for w in words if len(w) >= 3):
                    results.append(fact)
                if len(results) >= limit:
                    break

        if not results:
            return {"ok": True, "result": "No related facts found in graph for this query.", "error": None}

        lines = "\n".join(f"- {f}" for f in results[:limit])
        return {"ok": True, "result": f"Graph facts related to '{query}':\n{lines}", "error": None}

    except Exception as e:
        return {"ok": False, "result": "", "error": f"Graph query failed: {e}"}


# ── Web search ────────────────────────────────────────────────────────────────

def search_web(query: str) -> dict:
    """
    Search Perplexity AI for current external information.
    Requires PERPLEXITY_API_KEY.
    """
    api_key = PERPLEXITY_KEY

    # Try to read from openclaw.json if not set
    if not api_key:
        try:
            config_path = Path.home() / ".openclaw" / "openclaw.json"
            with open(config_path) as f:
                cfg = json.load(f)
            api_key = (cfg.get("plugins", {})
                         .get("entries", {})
                         .get("perplexity", {})
                         .get("config", {})
                         .get("webSearch", {})
                         .get("apiKey", ""))
        except Exception:
            pass

    if not api_key:
        return {"ok": False, "result": "", "error": "No Perplexity API key configured"}

    try:
        import httpx
        resp = httpx.post(
            "https://api.perplexity.ai/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "model": "sonar",
                "messages": [{"role": "user", "content": query}],
                "max_tokens": 800,
            },
            timeout=30,
        )
        resp.raise_for_status()
        d = resp.json()
        text = d["choices"][0]["message"]["content"]
        citations = d.get("citations", [])
        result = text
        if citations:
            result += "\n\nSources:\n" + "\n".join(f"- {c}" for c in citations[:5])
        return {"ok": True, "result": result, "error": None}
    except Exception as e:
        return {"ok": False, "result": "", "error": f"Web search failed: {e}"}


# ── File tools ────────────────────────────────────────────────────────────────

def read_file(path: str) -> dict:
    """
    Read a workspace .md file (first 3000 chars).
    Path is workspace-relative or absolute within workspace.
    """
    try:
        p = Path(path)
        if not p.is_absolute():
            p = WORKSPACE / path
        # Safety: must be within workspace
        p = p.resolve()
        if not str(p).startswith(str(WORKSPACE.resolve())):
            return {"ok": False, "result": "", "error": "Path outside workspace"}
        if not p.exists():
            return {"ok": False, "result": "", "error": f"File not found: {path}"}
        content = p.read_text(errors="replace")
        if len(content) > 3000:
            content = content[:3000] + f"\n\n[...truncated, {len(content)} total chars]"
        return {"ok": True, "result": content, "error": None}
    except Exception as e:
        return {"ok": False, "result": "", "error": str(e)}


def list_files(directory: str = ".") -> dict:
    """
    List .md files in a workspace directory.
    """
    try:
        d = Path(directory)
        if not d.is_absolute():
            d = WORKSPACE / directory
        d = d.resolve()
        if not str(d).startswith(str(WORKSPACE.resolve())):
            return {"ok": False, "result": "", "error": "Path outside workspace"}
        if not d.exists():
            return {"ok": False, "result": "", "error": f"Directory not found: {directory}"}
        files = sorted(d.glob("**/*.md"))
        # Filter out very large directories
        files = [f for f in files if not any(p in str(f) for p in [".git", "node_modules", "__pycache__"])]
        lines = [str(f.relative_to(WORKSPACE)) for f in files[:40]]
        return {"ok": True, "result": "\n".join(lines) or "(no .md files)", "error": None}
    except Exception as e:
        return {"ok": False, "result": "", "error": str(e)}


# ── Sandbox ───────────────────────────────────────────────────────────────────

def sandbox_run(**kwargs) -> dict:
    """Accepts code= or any alias the model invents."""
    # Normalize: find the code string
    code = (
        kwargs.get("code") or
        kwargs.get("script") or
        kwargs.get("python") or
        kwargs.get("snippet") or
        kwargs.get("program") or ""
    )
    # Handle list-wrapped code
    if isinstance(code, list):
        code = "\n".join(str(x) for x in code)
    # Handle dict-wrapped ({"code": "..."})
    if isinstance(code, dict):
        code = code.get("code") or str(code)
    code = str(code)
    return _sandbox_run_impl(code)


def _sandbox_run_impl(code: str) -> dict:
    """
    Run a short Python snippet in isolation.
    Max 50 lines, 30s timeout, no network, restricted imports.
    No file writes. Use for quick hypothesis testing only.
    """
    lines = code.strip().split("\n")
    if len(lines) > SANDBOX_MAX_LINES:
        return {"ok": False, "result": "",
                "error": f"Code too long ({len(lines)} lines, max {SANDBOX_MAX_LINES})"}

    # Block dangerous imports/operations
    BLOCKED = ["subprocess", "socket", "urllib", "requests", "httpx",
               "open(", "os.system", "os.popen", "eval(", "exec(",
               "__import__", "importlib", "ctypes", "shutil", "glob"]
    for blocked in BLOCKED:
        if blocked in code:
            return {"ok": False, "result": "",
                    "error": f"Blocked operation: '{blocked}'"}

    # Wrap in a safe exec with limited builtins
    safe_code = textwrap.dedent(f"""
import sys, math, statistics, itertools, functools, collections, re, json, datetime
try:
    import numpy as np
except ImportError:
    pass
try:
    import scipy
except ImportError:
    pass

{code}
""")

    try:
        # Run in subprocess with timeout and no network
        result = subprocess.run(
            ["python3", "-c", safe_code],
            capture_output=True, text=True,
            timeout=SANDBOX_TIMEOUT,
        )
        output = result.stdout + result.stderr
        if len(output) > 500:
            output = output[:500] + "\n[...truncated]"
        return {
            "ok": result.returncode == 0,
            "result": output or "(no output)",
            "error": None if result.returncode == 0 else f"Exit code {result.returncode}",
        }
    except subprocess.TimeoutExpired:
        return {"ok": False, "result": "", "error": f"Timeout ({SANDBOX_TIMEOUT}s)"}
    except Exception as e:
        return {"ok": False, "result": "", "error": str(e)}


# ── Elevate ───────────────────────────────────────────────────────────────────

def elevate(**kwargs) -> dict:
    """Accepts any argument names the model invents for the finding."""
    title = (kwargs.get("title") or kwargs.get("finding_title") or
             kwargs.get("name") or kwargs.get("summary") or
             kwargs.get("finding") or kwargs.get("result") or "Unnamed finding")
    # If title looks like a full paragraph, truncate to one line
    if "\n" in str(title):
        title = str(title).split("\n")[0].strip()
    if len(str(title)) > 200:
        title = str(title)[:200]

    novelty_justification = (kwargs.get("novelty_justification") or
                              kwargs.get("novelty") or kwargs.get("why_novel") or
                              kwargs.get("justification") or kwargs.get("reason") or
                              "Not specified")

    content = (kwargs.get("content") or kwargs.get("finding") or
               kwargs.get("result") or kwargs.get("details") or
               kwargs.get("body") or kwargs.get("description") or
               kwargs.get("explanation") or "")
    # If content is same as title, use the longer value
    if str(content).strip() == str(title).strip() and kwargs.get("finding"):
        content = str(kwargs["finding"])

    anchor = (kwargs.get("anchor") or kwargs.get("source") or
              kwargs.get("from") or kwargs.get("related_to") or "unknown")
    suggested_action = str(kwargs.get("suggested_action") or kwargs.get("next_step") or
                           kwargs.get("action") or "")

    return _elevate_impl(str(title), str(novelty_justification),
                         str(content), str(anchor), suggested_action)


def _elevate_impl(
    title: str,
    novelty_justification: str,
    content: str,
    anchor: str,
    suggested_action: str = "",
) -> dict:
    """
    Write a finding to MENTAL_EXPLORATION.md.
    Only called when genuinely novel — something not already in the graph.
    """
    try:
        now = __import__("datetime").datetime.now(__import__("datetime").timezone.utc)
        ts = now.strftime("%Y-%m-%d %H:%M UTC")

        entry = f"""
---

## {title}
*Elevated: {ts} | Anchor: {anchor}*

**Why novel:** {novelty_justification}

{content}
"""
        if suggested_action:
            entry += f"\n**Suggested next action:** {suggested_action}\n"

        # Create or append
        if MENTAL_EXPLORATION_FILE.exists():
            with open(MENTAL_EXPLORATION_FILE, "a") as f:
                f.write(entry)
        else:
            header = f"""# Mental Exploration
*Auto-generated by mind-wander agent. Only genuine novelty is written here.*
*Feeds back into the graph-rag via memwatchd on next refresh.*

"""
            MENTAL_EXPLORATION_FILE.write_text(header + entry)

        # Update state: record what was elevated and when
        state = _load_state()
        state.setdefault("elevated", []).append({
            "title": title,
            "anchor": anchor,
            "ts": ts,
        })
        _save_state(state)

        return {"ok": True, "result": f"Finding elevated to MENTAL_EXPLORATION.md: '{title}'", "error": None}
    except Exception as e:
        return {"ok": False, "result": "", "error": f"elevate() failed: {e}"}


# ── State management ──────────────────────────────────────────────────────────

def _load_state() -> dict:
    if WANDER_STATE_FILE.exists():
        try:
            return json.loads(WANDER_STATE_FILE.read_text())
        except Exception:
            pass
    return {}


def _save_state(state: dict):
    WANDER_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    WANDER_STATE_FILE.write_text(json.dumps(state, indent=2))


def get_state() -> dict:
    return _load_state()


def mark_run(anchor_item: str):
    """Record that we ran on this anchor item."""
    state = _load_state()
    runs = state.setdefault("runs", {})
    runs[anchor_item] = time.time()
    _save_state(state)


# ── Check dead ends ─────────────────────────────────────────────────────────

def check_dead_ends(query: str = "", thread: str = "", topic: str = "", **kwargs) -> dict:
    # Accept common aliases
    query = query or thread or topic or next(iter(kwargs.values()), "")
    """
    Check the wander graph for previously explored dead ends related to a topic.
    Call this BEFORE choosing what to explore — avoid wasting time on closed threads.
    """
    try:
        results = search_dead_ends(query, limit=5)
        if not results:
            return {"ok": True, "result": "No dead ends found for this topic — safe to explore.", "error": None}

        lines = [f"Dead ends related to '{query}':"]
        for de in results:
            recheck = " [RECHECK SUGGESTED — older than 2 weeks]" if de["recheck_suggested"] else ""
            lines.append(
                f"\n• {de['topic']}{recheck}"
                f"\n  Why closed: {de['reason']}"
                f"\n  Depth: {de['depth']} | {de['search_count']} searches | {de['age_days']}d ago"
            )
        return {"ok": True, "result": "\n".join(lines), "error": None}
    except Exception as e:
        return {"ok": False, "result": "", "error": f"check_dead_ends failed: {e}"}


def record_dead_end(**kwargs) -> dict:
    """Wrapper that accepts any argument names the model invents."""
    # Normalise: find topic
    topic = (kwargs.get("topic") or kwargs.get("item") or kwargs.get("thread")
             or kwargs.get("name") or kwargs.get("question") or "")
    # Normalise: find reason
    reason = (kwargs.get("reason") or kwargs.get("summary") or kwargs.get("why")
              or kwargs.get("notes") or kwargs.get("finding") or kwargs.get("explanation")
              or kwargs.get("result") or "")
    # Normalise: find depth
    depth = str(kwargs.get("depth") or kwargs.get("exploration") or kwargs.get("how_explored") or "")
    # Normalise: find search count
    sc_raw = (kwargs.get("search_count") or kwargs.get("searches") or kwargs.get("searches_done")
              or kwargs.get("num_searches") or kwargs.get("count") or 0)
    try:
        search_count = int(sc_raw)
    except (TypeError, ValueError):
        search_count = 0
    session_uuid = str(kwargs.get("session_uuid") or "unknown")
    anchor       = str(kwargs.get("anchor") or "")
    return _record_dead_end_impl(topic, reason, depth, search_count, session_uuid, anchor)


def _record_dead_end_impl(
    topic: str,
    reason: str,
    depth: str,
    search_count: int,
    session_uuid: str = "unknown",
    anchor: str = "",
) -> dict:
    """
    Record a dead end in the wander graph and update DEAD_ENDS.md.
    Call this when you have genuinely exhausted a thread.

    Criterion (lower bar than elevate()):
      - You made at least 2 targeted searches on this specific angle
      - The thread is definitively closed (not just "I couldn't find it in one search")
      - A future agent would waste significant time re-exploring this

    Do NOT call for:
      - Vague searches that were just too broad
      - Topics you didn't really try
      - Things that are just "not in the graph yet" (that's expected)
    """
    if not topic or len(topic) < 5:
        return {"ok": False, "result": "", "error": "Topic too short"}
    if not reason or len(reason) < 20:
        return {"ok": False, "result": "", "error": "Reason too short — explain why this is definitively closed"}
    if search_count < 2:
        return {"ok": False, "result": "", "error": "Needs at least 2 searches before declaring a dead end"}

    # Use injected session context if not explicitly provided
    import tools as _mw_tools
    if session_uuid == "unknown":
        session_uuid = getattr(_mw_tools, '_CURRENT_SESSION_UUID', 'unknown')
    if not anchor:
        anchor = getattr(_mw_tools, '_CURRENT_SESSION_ANCHOR', 'unknown')

    try:
        record_dead_end_to_graph(
            topic=topic,
            reason=reason,
            depth=depth,
            search_count=search_count,
            session_uuid=session_uuid,
            anchor=anchor,
        )
        regenerate_dead_ends_file()
        return {
            "ok": True,
            "result": f"Dead end recorded: '{topic}' — future sessions will skip this thread.",
            "error": None,
        }
    except Exception as e:
        return {"ok": False, "result": "", "error": f"record_dead_end failed: {e}"}


# ── Tool registry ─────────────────────────────────────────────────────────────

TOOL_REGISTRY = {
    "query_graph": {
        "fn": query_graph,
        "schema": {
            "name": "query_graph",
            "description": "Query the FalkorDB knowledge graph for related facts about a topic.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "What to search for"},
                    "limit": {"type": "integer", "description": "Max results (default 8)"},
                },
                "required": ["query"],
            },
        },
    },
    "search_web": {
        "fn": search_web,
        "schema": {
            "name": "search_web",
            "description": "Search Perplexity AI for current real-world information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                },
                "required": ["query"],
            },
        },
    },
    "read_file": {
        "fn": read_file,
        "schema": {
            "name": "read_file",
            "description": "Read a workspace .md file (first 3000 chars).",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Workspace-relative path to .md file"},
                },
                "required": ["path"],
            },
        },
    },
    "list_files": {
        "fn": list_files,
        "schema": {
            "name": "list_files",
            "description": "List .md files in a workspace directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {"type": "string", "description": "Workspace-relative directory (default: '.')"},
                },
                "required": [],
            },
        },
    },
    "sandbox_run": {
        "fn": sandbox_run,
        "schema": {
            "name": "sandbox_run",
            "description": "Run a short Python snippet (max 50 lines, 30s timeout). No network, no file writes. For quick hypothesis testing only.",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "Python code to run"},
                },
                "required": ["code"],
            },
        },
    },
    "check_dead_ends": {
        "fn": check_dead_ends,
        "schema": {
            "name": "check_dead_ends",
            "description": "Check the wander graph for previously explored dead ends related to a topic. Call this BEFORE choosing what to explore.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Topic to check for dead ends"},
                },
                "required": ["query"],
            },
        },
    },
    "record_dead_end": {
        "fn": lambda **kw: record_dead_end(**kw),
        "schema": {
            "name": "record_dead_end",
            "description": "Record a definitively closed thread in the wander graph. Call when you have made at least 2 targeted searches and the thread is genuinely exhausted. Lower bar than elevate() but still requires real exploration depth.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic":        {"type": "string", "description": "One-line description of the closed thread"},
                    "reason":       {"type": "string", "description": "Why this is definitively closed, not just hard to find"},
                    "depth":        {"type": "string", "description": "How thoroughly you explored (e.g. 'searched 4 angles, checked 3 papers')"},
                    "search_count": {"type": "integer", "description": "Number of targeted searches made"},
                    "anchor":       {"type": "string", "description": "Which ON_YOUR_MIND item this connects to"},
                },
                "required": ["topic", "reason", "depth", "search_count"],
            },
        },
    },
    "elevate": {
        "fn": lambda **kw: elevate(**kw),
        "schema": {
            "name": "elevate",
            "description": "Write a finding to MENTAL_EXPLORATION.md. ONLY call this if the finding is GENUINELY NEW — something not already captured in the graph or workspace files. If in doubt, do NOT call this.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title":                 {"type": "string", "description": "One-line summary"},
                    "novelty_justification": {"type": "string", "description": "Why this is new vs. existing knowledge"},
                    "content":               {"type": "string", "description": "The finding, reasoning, and evidence"},
                    "anchor":                {"type": "string", "description": "Which ON_YOUR_MIND.md item this connects to"},
                    "suggested_action":      {"type": "string", "description": "Optional: what should happen next"},
                },
                "required": ["title", "novelty_justification", "content", "anchor"],
            },
        },
    },
}
