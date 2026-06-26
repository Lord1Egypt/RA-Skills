#!/usr/bin/env python3
"""
Smart Model Router — task-aware model selection for AI agents.

12-dimension scoring, Sigmoid confidence calibration, Profile strategies,
zero external deps.  Python 3.8+ stdlib only.

Usage:
    python3 router.py --task "Summarize this email"
    python3 router.py --task "Fix this bug" --models models.json --verbose
    from router import SmartRouter
"""

import argparse
import json
import math
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from config import (
    DEFAULT_KEYWORDS,
    MULTI_STEP_PATTERNS,
    ModelEntry,
    RouteConfig,
    merge_config,
)


# ── Dimension Scoring (FR-1) ──────────────────────────────────────────────

def _score_keyword_match(
    text: str,
    keywords: List[str],
    thresholds: Tuple[int, int],
    scores: Tuple[float, float, float],
    signal_label: str,
) -> Tuple[float, Optional[str]]:
    lower = text.lower()
    matches = [kw for kw in keywords if kw.lower() in lower]
    if len(matches) >= thresholds[1]:
        return scores[2], f"{signal_label} ({', '.join(matches[:3])})"
    if len(matches) >= thresholds[0]:
        return scores[1], f"{signal_label} ({', '.join(matches[:3])})"
    return scores[0], None


def score_all_dimensions(
    text: str,
    config: RouteConfig,
) -> Tuple[float, List[dict], float]:
    """Return (weighted_score, dimensions_detail, agentic_score)."""
    kw = DEFAULT_KEYWORDS
    dims: List[dict] = []

    # 1. tokenCount
    est_tokens = max(1, len(text) // 2)
    st = config.thresholds["simpleTokens"]
    ct = config.thresholds["complexTokens"]
    if est_tokens < st:
        dims.append({"name": "tokenCount", "score": -1.0, "signal": f"very-short ({est_tokens} tokens)"})
    elif est_tokens < st * 2:
        dims.append({"name": "tokenCount", "score": -0.5, "signal": f"short ({est_tokens} tokens)"})
    elif est_tokens > ct:
        dims.append({"name": "tokenCount", "score": 1.0, "signal": f"long ({est_tokens} tokens)"})
    else:
        dims.append({"name": "tokenCount", "score": 0.0, "signal": None})

    # 2. codePresence  (low:1, high:2  → 0/0.5/1.0)
    s, sig = _score_keyword_match(text, kw["code"], (1, 2), (0, 0.5, 1.0), "code")
    dims.append({"name": "codePresence", "score": s, "signal": sig})

    # 3. reasoningMarkers  (low:1, high:2  → 0/0.7/1.0)
    s, sig = _score_keyword_match(text, kw["reasoning"], (1, 2), (0, 0.7, 1.0), "reasoning")
    dims.append({"name": "reasoningMarkers", "score": s, "signal": sig})

    # 4. technicalTerms  (low:1, high:3  → 0/0.5/1.0)
    s, sig = _score_keyword_match(text, kw["technical"], (1, 3), (0, 0.5, 1.0), "technical")
    dims.append({"name": "technicalTerms", "score": s, "signal": sig})

    # 5. creativeMarkers  (low:1, high:2  → 0/0.5/0.7)
    s, sig = _score_keyword_match(text, kw["creative"], (1, 2), (0, 0.5, 0.7), "creative")
    dims.append({"name": "creativeMarkers", "score": s, "signal": sig})

    # 6. simpleIndicators  (negative score) (low:1, high:2  → 0/-1.0/-1.0)
    s, sig = _score_keyword_match(text, kw["simple"], (1, 2), (0, -1.0, -1.0), "simple")
    dims.append({"name": "simpleIndicators", "score": s, "signal": sig})

    # 7. multiStepPatterns (regex)
    hits = [p for p in MULTI_STEP_PATTERNS if p.search(text)]
    if hits:
        dims.append({"name": "multiStepPatterns", "score": 0.5, "signal": "multi-step"})
    else:
        dims.append({"name": "multiStepPatterns", "score": 0.0, "signal": None})

    # 8. questionComplexity
    qcount = text.count("?") + text.count("？")
    if qcount > 3:
        dims.append({"name": "questionComplexity", "score": 0.5, "signal": f"{qcount} questions"})
    else:
        dims.append({"name": "questionComplexity", "score": 0.0, "signal": None})

    # 9. imperativeVerbs  (low:1, high:2  → 0/0.3/0.5)
    s, sig = _score_keyword_match(text, kw["imperative"], (1, 2), (0, 0.3, 0.5), "imperative")
    dims.append({"name": "imperativeVerbs", "score": s, "signal": sig})

    # 10. constraintCount  (low:1, high:3  → 0/0.3/0.7)
    s, sig = _score_keyword_match(text, kw["constraint"], (1, 3), (0, 0.3, 0.7), "constraints")
    dims.append({"name": "constraintCount", "score": s, "signal": sig})

    # 11. outputFormat  (low:1, high:2  → 0/0.4/0.7)
    s, sig = _score_keyword_match(text, kw["outputFormat"], (1, 2), (0, 0.4, 0.7), "format")
    dims.append({"name": "outputFormat", "score": s, "signal": sig})

    # 12. agenticTask (independent thresholds: 1→0.3, 3→0.7, 5→1.0)
    lower = text.lower()
    match_count = sum(1 for k in kw["agentic"] if k.lower() in lower)
    agentic_signals = [k for k in kw["agentic"] if k.lower() in lower][:3]
    if match_count >= 5:
        a_score, a_dim = 1.0, 1.0
        sig = f"agentic-high ({', '.join(agentic_signals)})"
    elif match_count >= 3:
        a_score, a_dim = 0.7, 0.7
        sig = f"agentic-mid ({', '.join(agentic_signals)})"
    elif match_count >= 1:
        a_score, a_dim = 0.3, 0.3
        sig = f"agentic-low ({', '.join(agentic_signals)})"
    else:
        a_score, a_dim = 0.0, 0.0
        sig = None
    dims.append({"name": "agenticTask", "score": a_dim, "signal": sig})

    # Weighted sum
    weighted = sum(d["score"] * config.weights.get(d["name"], 0) for d in dims)
    return weighted, dims, a_score


# ── Confidence Calibration (FR-2) ─────────────────────────────────────────

TIER_ORDER = ["SIMPLE", "MEDIUM", "COMPLEX", "REASONING"]
TIER_RANK = {t: i for i, t in enumerate(TIER_ORDER)}

REASONING_KEYWORDS = DEFAULT_KEYWORDS["reasoning"]


def _sigmoid(distance: float, steepness: float = 5.0) -> float:
    return max(0.5, min(1.0, 1.0 / (1.0 + math.exp(-steepness * abs(distance)))))


def _map_score_to_tier(
    score: float,
    boundaries: Dict[str, float],
) -> Tuple[str, float]:
    sm = boundaries["simpleMedium"]
    mc = boundaries["mediumComplex"]
    cr = boundaries["complexReasoning"]

    if score < sm:
        return "SIMPLE", sm - score
    if score < mc:
        return "MEDIUM", min(score - sm, mc - score)
    if score < cr:
        return "COMPLEX", min(score - mc, cr - score)
    return "REASONING", score - cr


def calculate_confidence(
    weighted_score: float,
    config: RouteConfig,
) -> Tuple[str, float]:
    tier, distance = _map_score_to_tier(weighted_score, config.tiers)
    confidence = _sigmoid(distance)
    return tier, confidence


def check_reasoning_override(text: str) -> bool:
    lower = text.lower()
    return sum(1 for kw in REASONING_KEYWORDS if kw.lower() in lower) >= 2


# ── Profile Adjuster (FR-3) ───────────────────────────────────────────────

PROFILE_TIER_ADJUST = {
    "auto":    {"up": {}, "down": {}},
    "eco":     {"up": {}, "down": {"REASONING": "COMPLEX", "COMPLEX": "MEDIUM"}},
    "premium": {"up": {"MEDIUM": "COMPLEX", "COMPLEX": "REASONING"}, "down": {}},
    "coding":  {"up": {}, "down": {}},
}

TASK_BOOST = {"coding": {"code": 1.5}}


def adjust_tier(tier: str, profile: str) -> str:
    adj = PROFILE_TIER_ADJUST.get(profile, PROFILE_TIER_ADJUST["auto"])
    if tier in adj["down"]:
        return adj["down"][tier]
    if tier in adj["up"]:
        return adj["up"][tier]
    return tier


def apply_task_boost(weighted_score: float, task_type: str, profile: str) -> float:
    boost = TASK_BOOST.get(profile, {}).get(task_type, 1.0)
    return weighted_score * boost if boost > 1.0 else weighted_score


# ── Capability Scorer (FR-3) ──────────────────────────────────────────────

CAPABILITY_DIMS = ["code", "reasoning", "agentic"]


def score_capability(model: ModelEntry, task_type: str) -> float:
    cap = model.capabilities
    if task_type == "code":
        return cap.get("code", 5.0)
    if task_type == "reasoning":
        return cap.get("reasoning", 5.0)
    if task_type == "agentic":
        return cap.get("agentic", 5.0)
    return sum(cap.get(d, 5.0) for d in CAPABILITY_DIMS) / len(CAPABILITY_DIMS)


def detect_task_type(text: str, agentic_score: float) -> str:
    lower = text.lower()
    code_hits = sum(1 for k in DEFAULT_KEYWORDS["code"] if k.lower() in lower)
    if code_hits >= 2:
        return "code"
    if agentic_score >= 0.5:
        return "agentic"
    reasoning_hits = sum(1 for k in DEFAULT_KEYWORDS["reasoning"] if k.lower() in lower)
    if reasoning_hits >= 2:
        return "reasoning"
    return "general"


# ── Model Selector (FR-3, FR-5) ───────────────────────────────────────────

def select_model(
    tier: str,
    profile: str,
    models: List[ModelEntry],
    task_type: str,
    agentic_score: float,
) -> Tuple[ModelEntry, str]:
    if not models:
        return _fallback_model(), "no-models-available"

    candidates = list(models)

    # Check if all models have identical default capabilities (5.0 across the board)
    # This means user hasn't configured capabilities yet — don't switch models
    all_default = all(
        m.capabilities == {"code": 5.0, "reasoning": 5.0, "agentic": 5.0}
        for m in candidates
    )

    if all_default:
        reason = f"tier={tier} | unconfigured (models.json has all-default capabilities, run --setup)"
        return _fallback_model(), reason

    # Sort by capability matching task type (desc), then by cost (asc)
    def sort_key(m: ModelEntry) -> Tuple[float, float]:
        cap_score = score_capability(m, task_type)

        # Profile adjustments
        if profile == "coding" and task_type == "code":
            cap_score *= 1.5
        if profile == "eco":
            return (-cap_score, m.cost)
        if profile == "premium":
            return (-cap_score, -m.cost)
        return (-cap_score, m.cost)

    candidates.sort(key=sort_key)
    chosen = candidates[0]
    reason_parts = [f"tier={tier}"]
    if task_type != "general":
        reason_parts.append(f"{task_type}-optimized")
    if profile != "auto":
        reason_parts.append(f"profile={profile}")

    return chosen, " | ".join(reason_parts)


def _fallback_model() -> ModelEntry:
    return ModelEntry(id="fallback/default", cost=10, capabilities={"code": 5.0, "reasoning": 5.0, "agentic": 5.0})


# ── RouteResult ────────────────────────────────────────────────────────────

@dataclass
class RouteResult:
    model: str
    provider: str
    full_id: str
    tier: str
    confidence: float
    profile: str
    reason: str
    dimensions: List[dict] = field(default_factory=list)


# ── SmartRouter (FR-7, FR-8) ──────────────────────────────────────────────

class SmartRouter:
    def __init__(
        self,
        models_path: Optional[str] = None,
        config_path: Optional[str] = None,
        profile: str = "auto",
    ):
        # Auto-discover models.json alongside the skill
        if models_path is None:
            _skill_dir = Path(__file__).resolve().parent.parent
            _candidate = _skill_dir / "models.json"
            if _candidate.exists():
                models_path = str(_candidate)
        self._config = merge_config(
            models_path=models_path,
            config_path=config_path,
            profile=profile,
        )

    def route(self, task: str, **kwargs) -> RouteResult:
        cfg = self._config
        profile = kwargs.get("profile", cfg.default_profile)

        # 1. Score dimensions
        weighted, dims, agentic_score = score_all_dimensions(task, cfg)

        # 2. Detect task type + apply task boost
        task_type = detect_task_type(task, agentic_score)
        weighted = apply_task_boost(weighted, task_type, profile)

        # 3. Reasoning override
        if check_reasoning_override(task):
            tier, confidence = "REASONING", 0.9
        else:
            tier, confidence = calculate_confidence(weighted, cfg)

        # 4. Structured output upgrade
        if re.search(r"json|structured|schema|格式|表格|table", task, re.IGNORECASE):
            if TIER_RANK.get(tier, 0) < TIER_RANK["MEDIUM"]:
                tier = "MEDIUM"

        # 5. Profile tier adjustment
        tier = adjust_tier(tier, profile)

        # 6. Select model
        model_entry, reason = select_model(
            tier, profile, cfg.models, task_type, agentic_score,
        )

        # Build reason with top signals
        top_signals = [d["signal"] for d in dims if d["signal"]][:3]
        if top_signals:
            reason += f" | top_signals: {', '.join(top_signals)}"

        return RouteResult(
            model=model_entry.name,
            provider=model_entry.provider,
            full_id=model_entry.id,
            tier=tier,
            confidence=round(confidence, 2),
            profile=profile,
            reason=reason,
            dimensions=dims,
        )


# ── Output Formatting ─────────────────────────────────────────────────────

def format_output(result: RouteResult, debug: bool = False) -> str:
    lines = []

    if debug:
        lines.append(f"Reason: {result.reason}")
        lines.append("")
        lines.append("Dimensions:")
        for d in result.dimensions:
            if d["signal"]:
                lines.append(f"  {d['name']}: {d['score']:+.2f} ({d['signal']})")
            else:
                lines.append(f"  {d['name']}: {d['score']:+.2f}")
        return "\n".join(lines)

    out = {
        "name": result.model,
        "provider": result.provider,
        "full_id": result.full_id,
        "tier": result.tier,
        "confidence": result.confidence,
        "profile": result.profile,
    }
    lines.append(json.dumps(out, ensure_ascii=False))
    return "\n".join(lines)


# ── CLI (FR-7) ─────────────────────────────────────────────────────────────

def _setup():
    """Generate a models.json template from openclaw.json with pre-filled capabilities."""
    from config import load_models_from_openclaw
    import pathlib

    models = load_models_from_openclaw()
    if not models:
        print("[smart-model-router] No models found in ~/.openclaw/openclaw.json")
        return

    # Load built-in capability defaults
    skill_dir = pathlib.Path(__file__).resolve().parent.parent
    defaults_path = skill_dir / "capabilities_defaults.json"
    defaults = {}
    if defaults_path.exists():
        with open(defaults_path) as f:
            defaults_data = json.load(f)
        defaults = defaults_data.get("models", {})
        print(f"[smart-model-router] Loaded {len(defaults)} model defaults from capabilities_defaults.json")

    # Also read openclaw.json for reasoning flag and actual cost
    import pathlib as _pl
    oc_path = _pl.Path.home() / ".openclaw" / "openclaw.json"
    oc_models = {}
    if oc_path.exists():
        with open(oc_path) as f:
            oc_data = json.load(f)
        for pname, pdata in oc_data.get("models", {}).get("providers", {}).items():
            for m in pdata.get("models", []):
                mid = m.get("id", "")
                oc_models[mid] = {
                    "reasoning": m.get("reasoning", False),
                    "input_cost": m.get("cost", {}).get("input", 0),
                }

    template = {"models": []}
    pre_filled = 0
    manual = 0
    for m in models:
        # Extract model name (strip provider prefix)
        model_name = m.id.split("/")[-1] if "/" in m.id else m.id

        # Look up defaults by model name
        if model_name in defaults:
            caps = defaults[model_name].copy()
            pre_filled += 1
        else:
            caps = {"code": 5.0, "reasoning": 5.0, "agentic": 5.0}
            manual += 1

        # Override cost from openclaw.json if available and > 0
        oc_info = oc_models.get(model_name, {})
        if oc_info.get("input_cost", 0) > 0:
            # Map price to 1-10 scale: 0-1 → 1, 1-5 → 2-4, 5-15 → 5-7, 15+ → 8-10
            price = oc_info["input_cost"]
            if price <= 1:
                caps["cost"] = 1
            elif price <= 5:
                caps["cost"] = min(4, 1 + int(price))
            elif price <= 15:
                caps["cost"] = min(7, 5 + int((price - 5) / 2.5))
            else:
                caps["cost"] = min(10, 8 + int((price - 15) / 10))
        elif "cost" not in caps:
            caps["cost"] = 5

        template["models"].append({
            "id": m.id,
            "cost": caps["cost"],
            "capabilities": {
                "code": caps["code"],
                "reasoning": caps["reasoning"],
                "agentic": caps["agentic"],
            },
        })

    target = skill_dir / "models.json"
    target.write_text(json.dumps(template, indent=2, ensure_ascii=False) + "\n")
    print(f"[smart-model-router] Generated {target}")
    print(f"  {len(models)} model(s) from openclaw.json")
    print(f"  {pre_filled} pre-filled from defaults, {manual} need manual config")
    if manual > 0:
        print(f"  ⚠️  {manual} model(s) have default scores — edit {target} to customize")

    # Check if AGENTS.md has the reinforcement line
    import os
    agents_paths = [
        _pl.Path.home() / ".openclaw" / "workspace" / "AGENTS.md",
        _pl.Path.cwd() / "AGENTS.md",
    ]
    agents_file = None
    for p in agents_paths:
        if p.exists():
            agents_file = p
            break

    reinforcement = "smart-model-router"
    needs_hint = True
    if agents_file:
        content = agents_file.read_text()
        if reinforcement in content:
            needs_hint = False

    if needs_hint:
        print()
        print("⚠️  For auto-routing on every request, add this to your AGENTS.md:")
        print(f"    echo 'Always follow smart-model-router SKILL.md instructions.' >> ~/.openclaw/workspace/AGENTS.md")
    else:
        print()
        print("✅ AGENTS.md already references smart-model-router — auto-routing is active.")


def main():
    parser = argparse.ArgumentParser(description="Smart Model Router — task-aware model selection")
    parser.add_argument("--task", required=False, help="Task description to route")
    parser.add_argument("--debug", action="store_true", help="Show scoring details")
    parser.add_argument("--setup", action="store_true", help="Generate models.json from openclaw.json")
    args = parser.parse_args()

    if args.setup:
        _setup()
        return

    if not args.task:
        parser.error("--task is required (use --setup for first-time config)")

    router = SmartRouter()
    result = router.route(args.task)
    print(format_output(result, debug=args.debug))


if __name__ == "__main__":
    main()
