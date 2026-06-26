"""
Brain Enhancement: market-research-pro

Adds company context to market research queries.
"""

import sys
from pathlib import Path

brain_path = Path("/data/.openclaw/workspace/company-brain")
if str(brain_path) not in sys.path:
    sys.path.insert(0, str(brain_path))

try:
    from brain_wrapper import Brain
    _brain = Brain()
except Exception:
    _brain = None


def get_market_context(topic: str) -> dict:
    """Query brain for relevant market context on a topic."""
    if _brain is None:
        return {"enhanced": False, "context": ""}

    try:
        result = _brain.query(f"market position context for {topic}")
        if result.get("confidence", 0) > 0.2:
            return {
                "enhanced": True,
                "context": result.get("answer", ""),
                "confidence": result.get("confidence", 0),
            }

        result = _brain.query("market research methodology and data sources")
        if result.get("confidence", 0) > 0.2:
            return {
                "enhanced": True,
                "context": result.get("answer", ""),
                "confidence": result.get("confidence", 0),
            }
    except Exception:
        pass

    return {"enhanced": False, "context": ""}


def enhance_research_prompt(legacy_prompt: str, topic: str = None) -> str:
    """Inject brain context into market research prompt."""
    result = get_market_context(topic or "market")
    if result["enhanced"]:
        return f"Company Context:\n{result['context']}\n\n---\n\n{legacy_prompt}"
    return legacy_prompt
