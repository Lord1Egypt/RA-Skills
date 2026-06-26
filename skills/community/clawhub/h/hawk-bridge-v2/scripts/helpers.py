# Helper functions — depends on core
import json
from pathlib import Path
from typing import Optional

from .core import *


# ---- Learnings -----------------------------------------------------------

# Per-persona learnings directory (not inside skill folder)
_LEARNINGS_DIR_DEFAULT = Path.home() / ".openclaw" / "workspace" / ".learnings"


def _detect_persona() -> str:
    """Detect current agent persona from OPENCLAW_AGENT_ID env var or cwd."""
    import os
    persona = os.environ.get("OPENCLAW_AGENT_ID", "").strip().lower()
    if persona in ("main", "tseng", "wukong", "bajie", "bailong", "shaseng"):
        return persona
    cwd = os.getcwd()
    for p in ("workspace-tseng", "workspace-wukong", "workspace-bajie",
              "workspace-bailong", "workspace-shaseng"):
        if p in cwd:
            return p.replace("workspace-", "")
    return "main"


def _workspace_for_persona(persona: str) -> Path:
    """Return workspace path for a given persona."""
    home = Path.home()
    if persona == "main":
        return home / ".openclaw" / "workspace"
    return home / ".openclaw" / f"workspace-{persona}"


def get_learnings_dir(persona: str = "") -> Path:
    """Return per-persona .learnings directory (auto-created)."""
    p = persona or _detect_persona()
    return _workspace_for_persona(p) / ".learnings"


def ensure_learnings_dir(persona: str = "") -> Path:
    """Ensure per-persona .learnings directory exists."""
    d = get_learnings_dir(persona)
    d.mkdir(parents=True, exist_ok=True)
    return d


def load_learnings(persona: str = "") -> dict:
    """Load learnings from per-persona .learnings directory."""
    d = ensure_learnings_dir(persona)
    approvals, rejections = [], []
    try:
        with open(d / "approvals.json", "r") as f:
            approvals = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    try:
        with open(d / "rejections.json", "r") as f:
            rejections = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return {"approvals": approvals, "rejections": rejections}


def save_learnings(data: dict, persona: str = "") -> None:
    """Save learnings to per-persona .learnings directory."""
    d = ensure_learnings_dir(persona)
    for key in ("approvals", "rejections"):
        fp = d / f"{key}.json"
        with open(fp, "w") as f:
            json.dump(data.get(key, []), f, ensure_ascii=False, indent=2)


def record_learning(
    item: dict,
    result: str,
    repo: str,
) -> None:
    """
    Record an execution result to learnings.
    - result == "ok" → approvals.json
    - result != "ok" → rejections.json (includes reason)

    Enhanced v4.0: saves richer context including perspective, scenario, impact.

    Args:
        item: Change item dict with keys: description, type, file_path,
              perspective, risk, scenario, suggested_direction, impact_score
        result: "ok" for success, or error reason string for failure
        repo: repository path
    """
    from datetime import datetime

    learning = {
        "timestamp": datetime.now().isoformat(),
        "description": item.get("description", ""),
        "type": item.get("type", ""),
        "perspective": item.get("perspective", ""),
        "risk": item.get("risk", ""),
        "scenario": item.get("scenario", ""),
        "suggested_direction": item.get("suggested_direction", ""),
        "impact_score": float(item.get("impact_score", 0.5)),
        "result": result,
        "file_path": item.get("file_path", ""),
        "repo": repo,
    }

    persona = _detect_persona()
    d = ensure_learnings_dir(persona)

    approvals, rejections = [], []
    try:
        with open(d / "approvals.json") as f:
            approvals = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    try:
        with open(d / "rejections.json") as f:
            rejections = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    if result == "ok":
        approvals.append(learning)
    else:
        learning["reason"] = result
        rejections.append(learning)

    with open(d / "approvals.json", "w") as f:
        json.dump(approvals, f, ensure_ascii=False, indent=2)
    with open(d / "rejections.json", "w") as f:
        json.dump(rejections, f, ensure_ascii=False, indent=2)


def record_iteration_metrics(
    iteration_id: str,
    todo_count: int = 0,
    todo_resolved: int = 0,
    duplicate_count: int = 0,
    duplicate_resolved: int = 0,
    auto_executed: int = 0,
    approved: int = 0,
    rejected: int = 0,
    llm_cost_usd: float = 0.0,
) -> dict:
    """
    Record iteration metrics for trend tracking.
    
    Saves metrics to .learnings/metrics/{iteration_id}.json
    """
    from datetime import datetime
    
    metrics = {
        "iteration_id": iteration_id,
        "timestamp": datetime.now().isoformat(),
        "todo_count": todo_count,
        "todo_resolved": todo_resolved,
        "duplicate_count": duplicate_count,
        "duplicate_resolved": duplicate_resolved,
        "auto_executed": auto_executed,
        "approved": approved,
        "rejected": rejected,
        "llm_cost_usd": llm_cost_usd,
    }
    
    metrics_dir = get_learnings_dir(_detect_persona()) / "metrics"
    metrics_dir.mkdir(parents=True, exist_ok=True)
    
    with open(metrics_dir / f"{iteration_id}.json", "w") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)
    
    return metrics


def is_rejected(change_desc: str, repo: str, learnings: dict) -> bool:
    """Check if a change was previously rejected in learnings."""
    for r in learnings.get("rejections", []):
        if r.get("repo") == repo and r.get("description", "") == change_desc:
            return True
    return False


def infer_value_score(item: ChangeItem) -> int:
    """Infer value score (1-10) for a change item."""
    keywords_high = [
        "test", "bug", "fix", "security", "vulnerability",
        "crash", "leak", "performance", "optimize", "critical",
    ]
    keywords_medium = [
        "refactor", "improve", "update", "enhance", "add feature",
        "compatibility", "deprecate",
    ]
    desc_lower = item.description.lower()
    if any(kw in desc_lower for kw in keywords_high):
        return 8
    if any(kw in desc_lower for kw in keywords_medium):
        return 5
    return 3


def infer_risk_score(risk: RiskLevel) -> int:
    """Convert risk level to numeric score (1-5)."""
    mapping = {
        RiskLevel.LOW: 1,
        RiskLevel.MEDIUM: 3,
        RiskLevel.HIGH: 4,
        RiskLevel.CRITICAL: 5,
    }
    return mapping.get(risk, 2)


def infer_cost_score(item: ChangeItem) -> int:
    """Infer implementation cost score (1-10)."""
    cost_keywords_low = ["comment", "docs", "typo", "format", "whitespace"]
    cost_keywords_high = [
        "database", "migration", "api change", "refactor",
        "redesign", "breaking", "schema",
    ]
    desc_lower = item.description.lower()
    if any(kw in desc_lower for kw in cost_keywords_low):
        return 2
    if any(kw in desc_lower for kw in cost_keywords_high):
        return 8
    return 4


def calculate_priority(item: ChangeItem) -> float:
    """
    Calculate priority score: higher = more important.
    Formula: value_score * 0.4 + (1 - risk/5) * 0.3 + (1 - cost/10) * 0.3
    """
    vs = infer_value_score(item)
    rs = infer_risk_score(item.risk)
    cs = infer_cost_score(item)
    return vs * 0.4 + (1 - rs / 5) * 0.3 + (1 - cs / 10) * 0.3


def enrich_change_with_priority(item: ChangeItem) -> ChangeItem:
    """Calculate and set priority for a change item."""
    item.value_score = float(infer_value_score(item))
    item.cost_score = float(infer_cost_score(item))
    item.priority = calculate_priority(item)
    return item


def sort_by_priority(items: list[ChangeItem]) -> list[ChangeItem]:
    """Sort change items by priority descending."""
    return sorted(items, key=lambda i: i.priority, reverse=True)
