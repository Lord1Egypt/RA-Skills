"""
collector.py — Captures mind-wander sessions to disk for training data.

Output: workspace/completions/wander/YYYY-MM-DD/<session_id>.json

Format extends the main completions-collector schema:
{
  "schema": "mind-wander.v1",
  "session_id": "...",
  "captured_at": "...",
  "model": "qwen3.5-wander-q4",
  "model_variant": "Q4_K_M",
  "anchor": "...",           # which ON_YOUR_MIND item was explored
  "elevated": bool,          # did the novelty gate pass?
  "elevated_title": "...",   # if elevated, what was found
  "tool_calls_count": N,
  "duration_seconds": N,
  "system_prompt": "...",
  "messages": [              # full conversation in OpenAI format
    {"role": "system", "content": "..."},
    {"role": "user",   "content": "..."},
    {"role": "assistant", "content": "...", "tool_calls": [...]},
    {"role": "tool",  "tool_call_id": "...", "content": "..."},
    ...
  ],
  "on_your_mind_snapshot": "...",   # contents of ON_YOUR_MIND.md at run time
  "graph_context": "...",           # graph facts injected as context
  "novelty_outcome": "elevated|discarded|error"
}
"""

import json
from pathlib import Path
from datetime import datetime, timezone

import sys
sys.path.insert(0, str(Path(__file__).parent))
from mind_wander_config import WORKSPACE

WANDER_COMPLETIONS_DIR = WORKSPACE / "completions" / "wander"


def save_session(
    session_id: str,
    model: str,
    anchor: str,
    system_prompt: str,
    messages: list,
    result: dict,
    on_your_mind_snapshot: str = "",
    graph_context: str = "",
):
    """
    Save a complete wander session to the wander completions directory.
    Called at the end of each agent.run() session.
    """
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")

    # Determine model variant from name
    variant = "Q4_K_M" if "q4" in model.lower() else "Q8_0" if "q8" in model.lower() else "unknown"

    # Determine novelty outcome
    if result.get("elevated"):
        outcome = "elevated"
    elif result.get("error"):
        outcome = "error"
    else:
        outcome = "discarded"

    record = {
        "schema":               "mind-wander.v1",
        "session_id":           session_id,
        "captured_at":          now.isoformat(),
        "model":                model,
        "model_variant":        variant,
        "anchor":               anchor or "auto-select",
        "elevated":             result.get("elevated", False),
        "elevated_title":       result.get("title"),
        "tool_calls_count":     result.get("tool_calls", 0),
        "duration_seconds":     round(result.get("duration", 0), 2),
        "novelty_outcome":      outcome,
        "system_prompt":        system_prompt,
        "messages":             messages,
        "on_your_mind_snapshot": on_your_mind_snapshot,
        "graph_context":        graph_context,
    }

    out_dir = WANDER_COMPLETIONS_DIR / date_str
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{session_id}.json"
    out_file.write_text(json.dumps(record, indent=2))

    return out_file
