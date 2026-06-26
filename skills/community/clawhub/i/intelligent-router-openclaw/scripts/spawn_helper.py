#!/usr/bin/env python3
"""
Intelligent Router - Spawn Helper (Enforced Core Skill)

MANDATORY: Call this before ANY sessions_spawn or cron job creation.
It classifies the task and outputs the exact model to use.

Usage (show command):
    python3 skills/intelligent-router/scripts/spawn_helper.py "task description"

Usage (just get model id):
    python3 skills/intelligent-router/scripts/spawn_helper.py --model-only "task description"

Usage (validate payload has model set):
    python3 skills/intelligent-router/scripts/spawn_helper.py --validate '{"kind":"agentTurn","message":"..."}'
"""

import sys
import json
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR.parent / "config.json"

TIER_COLORS = {
    "SIMPLE": "🟢",
    "MEDIUM": "🟡",
    "COMPLEX": "🟠",
    "REASONING": "🔵",
    "CRITICAL": "🔴",
}


def load_config():
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"Router config not found: {CONFIG_FILE}")
    with open(CONFIG_FILE) as f:
        return json.load(f)


_CODING_PATTERNS = [
    # direct fix/debug/implement verbs
    r"\bimplement\b", r"\brefactor\b", r"\bdebug\b", r"\bfix\b",
    r"\bwrite\s+\w+\s+(code|script|function|class|module|test)",
    # code artifacts
    r"\bcode\b", r"\bbugs?\b", r"\bunit\s+test", r"\bintegration\s+test",
    r"\btdd\b", r"\btest\s+(coverage|suite|passing)\b",
    r"\btests?\s+pass", r"\bpytest\b", r"\brspec\b",
    # languages / ecosystems
    r"\bpython\b", r"\btypescript\b", r"\bjavascript\b", r"\breact\b",
    r"\brust\b", r"\bgolang\b", r"\bgo\s+module", r"\bpallet\b",
    r"\bsmart\s+contract", r"\bsolidity\b",
    # structural terms
    r"\bapi\s+(client|server|endpoint)", r"\bmicroservice",
    r"\bwire\s+(up|into)", r"\brepo\b", r"\brepository\b",
    r"\bcoverage\b", r"\blint\b", r"\bmypy\b", r"\bruff\b",
    r"\bpyproject\b", r"\bcargo\b", r"\bpackage\.json\b",
]

def _is_coding_task(task_description: str) -> bool:
    """Return True if task description has clear coding intent."""
    import re
    text = task_description.lower()
    for pattern in _CODING_PATTERNS:
        if re.search(pattern, text):
            return True
    return False

# [llmfit-integration-start]
# Hardware fitness filtering for fallback chains.
# Added by: uv run python skills/llmfit/scripts/integrate.py
# Do NOT remove the marker comments — they allow re-patching to be idempotent.
import functools as _functools

_HARDWARE_FITS_FILE = Path(__file__).parent.parent.parent / "llmfit" / "data" / "hardware_fits.json"
_DEPRIORITIZE_FITS = {"marginal", "none"}  # fits to push to end of fallback chain


@_functools.lru_cache(maxsize=1)
def _load_hardware_fits() -> dict:
    """Load llmfit hardware fitness cache (cached for process lifetime)."""
    if not _HARDWARE_FITS_FILE.exists():
        return {}
    try:
        with open(_HARDWARE_FITS_FILE) as _f:
            return json.load(_f)
    except Exception:
        return {}


def get_hardware_fit(model_id: str) -> str:
    """
    Return the canonical fit string for a model_id (e.g. "good", "marginal", "none").
    Looks up the hardware_fit field added by integrate.py in config.json.
    Falls back to "unknown" if not found.
    """
    try:
        cfg = load_config()
        for entry in cfg.get("models", []):
            eid = entry.get("id", "")
            provider = entry.get("provider", "")
            # Match by full "provider/id" or bare "id"
            full_id = f"{provider}/{eid}" if provider else eid
            if model_id in (eid, full_id) or full_id.endswith(model_id):
                hw = entry.get("hardware_fit", {})
                return hw.get("fit", "unknown")
    except Exception:
        pass
    return "unknown"


def rerank_fallback_chain(chain: list) -> list:
    """
    Move models with fit="marginal" or fit="none" to the end of the fallback chain.
    Models with unknown/good/perfect fit keep their original order.
    This does NOT remove any models — just reranks for hardware awareness.
    """
    fits = [(model_id, get_hardware_fit(model_id)) for model_id in chain]
    preferred = [mid for mid, fit in fits if fit not in _DEPRIORITIZE_FITS]
    deprioritized = [mid for mid, fit in fits if fit in _DEPRIORITIZE_FITS]
    return preferred + deprioritized
# [llmfit-integration-end]

    text = task_description.lower()
    return any(re.search(p, text) for p in _CODING_PATTERNS)


def _get_complex_primary() -> str:
    """Return the forced COMPLEX primary from tier_overrides, or config primary."""
    try:
        with open(CONFIG_FILE) as f:
            cfg = json.load(f)
        override = cfg.get("tier_overrides", {}).get("COMPLEX", {})
        if override.get("forced_primary"):
            return override["forced_primary"]
        return cfg.get("routing_rules", {}).get("COMPLEX", {}).get("primary", "")
    except Exception:
        return ""


def classify_task(task_description):
    """Run router.py classify and return (tier, full_model_id, confidence).
    
    full_model_id is always provider/id (e.g. 'ollama-gpu-server/glm-4.7-flash'),
    which is the format required by sessions_spawn(model=...) and cron payloads.

    User override: coding tasks always route to COMPLEX (Sonnet 4.6 per tier_overrides).
    """
    result = subprocess.run(
        [sys.executable, str(SCRIPT_DIR / "router.py"), "classify", task_description],
        capture_output=True, text=True, check=True
    )
    lines = result.stdout.strip().split('\n')
    tier = None
    bare_id = None
    provider = None
    confidence = None

    for line in lines:
        if line.startswith("Classification:"):
            tier = line.split(":", 1)[1].strip()
        elif "  ID:" in line:
            bare_id = line.split(":", 1)[1].strip()
        elif "  Provider:" in line:
            provider = line.split(":", 1)[1].strip()
        elif line.startswith("Confidence:"):
            confidence = line.split(":", 1)[1].strip()

    # Combine provider + id for the full model identifier
    if bare_id and provider:
        model_id = f"{provider}/{bare_id}"
    else:
        model_id = bare_id

    # User rule: ALL coding tasks → COMPLEX (Sonnet 4.6 via tier_overrides)
    if tier in ("SIMPLE", "MEDIUM") and _is_coding_task(task_description):
        complex_primary = _get_complex_primary()
        if complex_primary:
            tier = "COMPLEX"
            model_id = complex_primary
            confidence = "OVERRIDE (coding task → COMPLEX)"

    return tier, model_id, confidence


def validate_payload(payload_json):
    """
    Validate a cron job payload has the model field set.
    Returns (ok: bool, message: str)
    """
    try:
        payload = json.loads(payload_json) if isinstance(payload_json, str) else payload_json
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON payload: {e}"

    if payload.get("kind") != "agentTurn":
        return True, "Non-agentTurn payload — model not required"

    model = payload.get("model")
    if not model:
        return False, (
            "❌ VIOLATION: agentTurn payload missing 'model' field!\n"
            "   Without model, OpenClaw defaults to Sonnet = expensive waste.\n"
            "   Fix: add \"model\": \"<model-id>\" to the payload.\n"
            "   Run: python3 skills/intelligent-router/scripts/spawn_helper.py \"<task>\" to get the right model."
        )

    # Check if Sonnet/Opus is used for a non-critical payload
    expensive = ["claude-sonnet", "claude-opus", "claude-3"]
    for keyword in expensive:
        if keyword in model.lower():
            msg = payload.get("message", "")[:80]
            return None, (
                f"⚠️  WARNING: Expensive model '{model}' set for potentially simple task.\n"
                f"   Task preview: {msg}...\n"
                f"   Consider: python3 skills/intelligent-router/scripts/spawn_helper.py \"{msg}\""
            )

    return True, f"✅ Model set: {model}"


def _health_check_and_reroute(model_id: str, config: dict, tier: str) -> str:
    """
    Proactive health-based routing.
    If the chosen provider is rate-limited or has too many active sessions,
    walk the fallback chain until we find a healthy one.
    Returns the best healthy model_id available.
    """
    try:
        from provider_health import is_healthy, pick_healthy
    except ImportError:
        sys.path.insert(0, str(SCRIPT_DIR))
        try:
            from provider_health import is_healthy, pick_healthy
        except ImportError:
            return model_id  # health module not available, pass through

    healthy, reason = is_healthy(model_id)
    if healthy:
        return model_id

    # Primary is degraded — walk fallback chain
    rules = config.get("routing_rules", {}).get(tier, {})
    fallback_chain = rules.get("fallback_chain", [])
    candidates = [model_id] + fallback_chain

    chosen = pick_healthy(candidates)
    if chosen and chosen != model_id:
        print(f"⚠️  {model_id.split('/')[0]} is degraded ({reason})", file=sys.stderr)
        print(f"   → Rerouting to: {chosen}", file=sys.stderr)
        return chosen

    # All degraded — return original and let caller handle failure
    print(f"⚠️  All providers degraded for tier {tier}, using {model_id} anyway", file=sys.stderr)
    return model_id


def main():
    args = sys.argv[1:]

    if not args:
        print(__doc__)
        sys.exit(1)

    # --validate mode
    if args[0] == "--validate":
        if len(args) < 2:
            print("Usage: spawn_helper.py --validate '<payload_json>'")
            sys.exit(1)
        ok, msg = validate_payload(args[1])
        print(msg)
        sys.exit(0 if ok else 1)

    # --model-only mode (just print the model id)
    if args[0] == "--model-only":
        if len(args) < 2:
            print("Usage: spawn_helper.py --model-only 'task description'")
            sys.exit(1)
        task = " ".join(args[1:])
        config = load_config()
        tier, model_id, _ = classify_task(task)
        if not model_id:
            rules = config.get("routing_rules", {}).get(tier, {})
            model_id = rules.get("primary", "anthropic-proxy-4/glm-4.7")
        # Health check — skip degraded providers proactively
        model_id = _health_check_and_reroute(model_id, config, tier)
        print(model_id)
        sys.exit(0)

    # Default: classify and show spawn command
    task = " ".join(args)
    config = load_config()
    tier, model_id, confidence = classify_task(task)

    if not model_id:
        rules = config.get("routing_rules", {}).get(tier, {})
        model_id = rules.get("primary", "anthropic-proxy-4/glm-4.7")

    # Health check — skip degraded providers proactively
    model_id = _health_check_and_reroute(model_id, config, tier)

    icon = TIER_COLORS.get(tier, "⚪")
    fallback_chain = config.get("routing_rules", {}).get(tier, {}).get("fallback_chain", [])
    fallback_chain = rerank_fallback_chain(fallback_chain)  # [llmfit-rerank-applied]

    print(f"\n{icon} Task classified as: {tier} (confidence: {confidence})")
    print(f"💰 Recommended model: {model_id}")
    if fallback_chain:
        print(f"🔄 Fallbacks: {' → '.join(fallback_chain[:2])}")
    print(f"\n📋 Use in sessions_spawn:")
    print(f"""   sessions_spawn(
       task=\"{task[:60]}{'...' if len(task)>60 else ''}\",
       model=\"{model_id}\",
       label=\"<label>\"
   )""")
    print(f"\n📋 Use in cron job payload:")
    print(f"""   {{
       "kind": "agentTurn",
       "message": "...",
       "model": "{model_id}"
   }}""")


if __name__ == "__main__":
    main()
