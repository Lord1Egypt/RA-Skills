#!/usr/bin/env python3
"""
Reusable config loader for OCAS / Hermes skills.

Hermes policy (AGENTS.md `env-var-for-config`): non-secret behavioral settings
(thresholds, paths, flags, feature toggles) MUST come from config.yaml under
`skills.config.<skill>.<key>`, never from GENIE_* / <NAME>_* environment
variables. Secrets stay in ~/.hermes/.env (read via os.environ /
`required_environment_variables`). HERMES_HOME / HERMES_PROFILE are the only
permitted non-secret env inputs -- they locate the runtime, not behavior.

Drop this into a skill's scripts/ (or inline the two functions) and call
_skill_config("<skill>", "mykey", default) to read any declared setting.
The shipped `telephony.py` optional-skill uses the same pattern. Reference:
spec-ocas-scripts.md -> "Configuration -- behavioral vs. secrets".
"""

import os


def _load_root_config():
    """Read $HERMES_HOME/config.yaml via PyYAML. Returns {} if absent/unreadable."""
    path = os.path.join(
        os.environ.get("HERMES_HOME", os.path.expanduser("~/.hermes")), "config.yaml"
    )
    if not os.path.exists(path):
        return {}
    try:
        import yaml  # Hermes already ships PyYAML
    except Exception:
        return {}
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _skill_config(skill, key, default):
    """Resolve ``skills.config.<skill>.<key>`` from config.yaml.

    Falls back to ``default`` when unset or empty. Bool/int coercion follows the
    declared default's type. Declare the key in SKILL.md frontmatter:

        metadata:
          hermes:
            config:
              - key: <skill>.<key>
                description: "..."
                default: "<default>"

    Storage key becomes ``skills.config.<skill>.<key>`` in config.yaml.
    """
    node = _load_root_config()
    for part in ("skills", "config", skill, key):
        if isinstance(node, dict) and part in node:
            node = node[part]
        else:
            return default
    if node is None or (isinstance(node, str) and not node.strip()):
        return default
    if isinstance(default, bool):
        return str(node).strip().lower() in {"1", "true", "yes", "on"}
    if isinstance(default, int):
        try:
            return int(node)
        except (TypeError, ValueError):
            return default
    return node


# Example usage inside a skill script:
# SNAPSHOT_MAX_AGE_DAYS = _skill_config("genie", "snapshot_max_age_days", 7)
# DRY_RUN = _skill_config("genie", "dry_run", False)