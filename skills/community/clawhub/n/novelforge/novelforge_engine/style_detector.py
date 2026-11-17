"""Optional style diagnostics. They are advisory unless project policy opts in."""

import re


DEFAULT_PATTERNS = (
    {"id": "author-reference", "pattern": "猫腻"},
    {"id": "work-reference", "pattern": "庆余年"},
    {"id": "work-reference", "pattern": "将夜"},
)


def policy_for_profile(profile=None):
    """Translate a project profile into detector policy without changing it."""
    profile = dict(profile or {})
    patterns = profile["style_detectors"] if "style_detectors" in profile else list(DEFAULT_PATTERNS)
    policies = profile.get("policies") or {}
    blocking_rules = list(profile.get("blocking_rules") or [])
    blocking_rules.extend(policies.get("blocking_rules") or [])
    mode = policies.get("style_detector_mode", "warning")
    if mode not in ("warning", "blocking"):
        raise ValueError("style_detector_mode must be warning or blocking")
    return {"patterns": patterns, "blocking_rules": blocking_rules, "blocking": mode == "blocking"}


def detect_style(text, policy=None):
    policy = dict(policy or {})
    patterns = policy["patterns"] if "patterns" in policy else list(DEFAULT_PATTERNS)
    matches = []
    for item in patterns:
        pattern = str(item.get("pattern", ""))
        if pattern and re.search(pattern, text):
            matches.append({"id": item.get("id", pattern), "pattern": pattern})
    blocking = bool(policy.get("blocking", False))
    blocking_rules = set(policy.get("blocking_rules") or [])
    blocking_matches = [item for item in matches if blocking or item["id"] in blocking_rules]
    return {
        "status": "FAIL" if blocking_matches else ("WARNING" if matches else "PASS"),
        "blocking": bool(blocking_matches),
        "matches": matches,
    }
