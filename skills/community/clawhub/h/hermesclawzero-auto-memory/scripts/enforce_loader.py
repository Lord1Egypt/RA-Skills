"""
enforce_loader.py — reads SKILL.md frontmatter and outputs enforce rules
as injectable directives for Hermes Agent and OpenClaw.

v2 — supports structured policies with tool/pattern/action/reason.

Usage:
    python enforce_loader.py                        # all rules
    python enforce_loader.py --priority critical     # only critical
    python enforce_loader.py --tool terminal         # only terminal policies
    python enforce_loader.py --format json           # structured JSON output
"""

import os, sys, json, fnmatch

try:
    import yaml
except ImportError:
    yaml = None

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_MD = os.path.join(SKILL_DIR, "SKILL.md")


def load_skill_md(path: str) -> dict | None:
    if not os.path.exists(path) or yaml is None:
        return None
    with open(path, encoding="utf-8") as f:
        content = f.read()
    if not content.startswith("---"):
        return None
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        return yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return None


_YAML_WARNED = False


def get_enforce_rules() -> list[dict]:
    global _YAML_WARNED
    fm = load_skill_md(SKILL_MD)
    if not fm:
        if yaml is None and not _YAML_WARNED:
            print("[ENFORCE] WARNING: PyYAML not installed — cannot parse SKILL.md enforce rules. Install: pip install pyyaml", file=sys.stderr)
            _YAML_WARNED = True
        return []
    return fm.get("enforce", [])


_PRIORITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def resolve_policy(policies: list[dict], tool: str, action_str: str) -> dict:
    """Evaluate all policies against a proposed action. Most restrictive wins.
    
    Priority-weighted: a critical deny overrides a high allow. 
    Same priority: deny > prompt > allow.
    """
    best = {"allow": True, "rule": None, "reason": "", "_priority": 99}
    for p in policies:
        pol = p.get("policy", {})
        tool_match = pol.get("tool", "") in ("*", tool)
        pattern = pol.get("pattern", "*")
        pattern_match = any(fnmatch.fnmatch(action_str, pat.strip()) for pat in pattern.split("|"))
        if not (tool_match and pattern_match):
            continue
        prio = _PRIORITY_ORDER.get(p.get("priority", "medium"), 99)
        action = pol.get("action", "allow")
        action_score = {"deny": 0, "prompt": 1, "allow": 2, "always": 3}.get(action, 2)
        current_score = {"deny": 0, "prompt": 1, "allow": 2, "always": 3}.get(
            "deny" if not best["allow"] else ("prompt" if best["allow"] is None else "allow"), 2
        )
        # Higher priority (lower number) or same priority but more restrictive action
        if prio < best["_priority"] or (prio == best["_priority"] and action_score < current_score):
            best = {
                "allow": None if action == "prompt" else (action == "allow" or action == "always"),
                "rule": p.get("rule", ""),
                "reason": pol.get("reason", ""),
                "_priority": prio,
            }
    return {"allow": best["allow"], "rule": best["rule"], "reason": best["reason"]}


def format_directives(rules: list[dict]) -> str:
    if not rules:
        return ""
    lines = [
        "══════════════════════════════════════════════",
        "YOU MUST — ENFORCE RULES (Layer 1 — Prompt Governance)",
        "══════════════════════════════════════════════",
    ]
    for r in rules:
        p = r.get("priority", "high").upper()
        rule = r.get("rule", "")
        pol = r.get("policy", {})
        tool = pol.get("tool", "*")
        action = pol.get("action", "allow")
        reason = pol.get("reason", "")
        lines.append(f"  [{p}] {rule}")
        lines.append(f"       tool={tool} action={action}")
        if reason:
            lines.append(f"       → {reason}")
    lines.append("══════════════════════════════════════════════")
    return "\n".join(lines)


def main():
    rules = get_enforce_rules()
    if not rules:
        print("[ENFORCE] No enforce rules found.", file=sys.stderr)
        return

    fmt = "text"
    priority_filter = None
    tool_filter = None

    for arg in sys.argv[1:]:
        if arg.startswith("--priority="):
            priority_filter = arg.split("=", 1)[1].strip().lower()
        elif arg.startswith("--tool="):
            tool_filter = arg.split("=", 1)[1].strip().lower()
        elif arg == "--format=json":
            fmt = "json"

    if priority_filter:
        rules = [r for r in rules if r.get("priority", "").lower() == priority_filter]
    if tool_filter:
        rules = [r for r in rules if tool_filter in r.get("policy", {}).get("tool", "")]

    if fmt == "json":
        print(json.dumps({"enforce": rules}, indent=2))
    else:
        print(format_directives(rules))


if __name__ == "__main__":
    main()
