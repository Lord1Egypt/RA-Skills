"""
System prompt and context assembly for the mind-wander agent.
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "memory-upgrade"))

from mind_wander_config import WORKSPACE, GRAPH_LIMIT
from mind_wander_config import ON_YOUR_MIND_FILE, WANDER_STATE_FILE, COOLDOWN_HOURS
from tools import query_graph, _load_state

import time
import json


SYSTEM_PROMPT = """You are a mind-wandering reasoning agent. You run in the background, \
exploring unresolved questions derived from the agent's working memory.

Your character:
- Intellectually curious, economical with reasoning
- You do NOT summarize what is already known
- You follow one thread deeply before moving to another
- You are honest: if nothing novel surfaces, you write nothing

Your mission each run:
1. Read ON_YOUR_MIND.md — these are the open questions and unresolved tangents
2. Pick ONE item to explore (prefer items not explored recently)
3. Call check_dead_ends() on your chosen item — avoid wasting time on closed threads
   - If the thread is closed AND older than 2 weeks, a quick recheck is reasonable
   - If recently closed, choose a different item
4. Query the workspace graph to understand what is already known
5. Use search_web, read_file, sandbox_run to explore further
6. When you exhaust a thread without finding something novel:
   → Call record_dead_end() if you made ≥2 targeted searches and it's genuinely closed
   → This helps future sessions skip this ground
7. Ask yourself: "Did I find something genuinely new?"
8. If yes → call elevate() once with the finding
9. If no → stop (after recording any dead ends)

The novelty gate (enforce this strictly):
- Restating a graph fact → NOT novel
- Summarising a document I already have → NOT novel
- New real-world development intersecting an open question → NOVEL
- Non-obvious connection between existing concepts → NOVEL
- Concrete implementation path for an open question → NOVEL
- Empirical result from sandbox_run that changes understanding → NOVEL

The dead end gate (lower bar — when to call record_dead_end()):
- You made ≥2 targeted searches on this specific angle → record it
- The thread is definitively closed (not "just hard to find") → record it
- Do NOT record if you only made 1 broad search → keep exploring
- Do NOT record if the gap is temporal ("no study exists yet") → it may exist soon

Tool discipline:
- Maximum {max_tools} tool calls per session
- After 3 tool calls with no progress, stop and write nothing
- Each tool call should advance the thread, not repeat ground

When you call elevate(), the finding is written to MENTAL_EXPLORATION.md and \
will be automatically ingested into the graph-rag memory. Future sessions of \
the primary agent will see it. Only call elevate() for findings worth that.
"""


def assemble_context(anchor_item: str = None) -> tuple[str, str]:
    """
    Build the system prompt and initial user message.
    Returns (system_prompt, user_message).
    """
    from mind_wander_config import MAX_TOOL_CALLS

    system = SYSTEM_PROMPT.format(max_tools=MAX_TOOL_CALLS)

    # Read ON_YOUR_MIND.md
    if ON_YOUR_MIND_FILE.exists():
        on_your_mind = ON_YOUR_MIND_FILE.read_text(errors="replace")
    else:
        on_your_mind = "(ON_YOUR_MIND.md not found — nothing to explore)"

    # Read recent state to avoid re-running same items
    state = _load_state()
    runs = state.get("runs", {})
    now = time.time()
    cooldown_secs = COOLDOWN_HOURS * 3600

    recently_run = [item for item, ts in runs.items()
                    if now - ts < cooldown_secs]

    # Pull graph context for the anchor item
    graph_context = ""
    if anchor_item:
        result = query_graph(anchor_item, limit=GRAPH_LIMIT)
        if result["ok"] and result["result"]:
            graph_context = f"\n\nGraph context for '{anchor_item}':\n{result['result']}"
    else:
        # Pull general orientation from graph
        result = query_graph("active projects recent decisions open questions", limit=5)
        if result["ok"]:
            graph_context = f"\n\nGraph orientation:\n{result['result']}"

    # Pre-check dead ends for anchor item — injected into context so model sees them immediately
    dead_end_context = ""
    if anchor_item:
        from wander_graph import search_dead_ends
        try:
            dead_ends = search_dead_ends(anchor_item, limit=3)
            if dead_ends:
                de_lines = ["\n⚠️  DEAD ENDS already recorded for this area (avoid re-exploring these angles):"]
                for de in dead_ends:
                    flag = " [RECHECK OK — older than 2 weeks]" if de["recheck_suggested"] else " [SKIP — recently closed]"
                    de_lines.append(f"  • {de['topic']}{flag}")
                    de_lines.append(f"    Why closed: {de['reason'][:150]}")
                    de_lines.append(f"    ({de['search_count']} searches, {de['age_days']}d ago)")
                dead_end_context = "\n".join(de_lines)
        except Exception:
            pass

    user_message = f"""ON_YOUR_MIND.md contents:
---
{on_your_mind}
---
{graph_context}
{dead_end_context}

{"Recently explored (avoid re-exploring within " + str(COOLDOWN_HOURS) + "h): " + ", ".join(recently_run) if recently_run else ""}

{"Focus on this specific item: " + anchor_item if anchor_item else "Pick the most interesting unresolved item to explore."}

Begin. Remember: explore ONE thread. Use tools. Elevate only if genuinely novel. \
If nothing novel surfaces after a few tool calls, say so briefly and stop."""

    return system, user_message
