"""Resolve {{INTERPOLATE_env:key.path}} (alias `{{@env:key.path}}`) placeholders against loaded YAML config."""
import json
import re
from pathlib import Path
from typing import Any

from helpers.config import get_config_value, load_yaml, load_env

PATTERN = re.compile(r"\{\{(?:INTERPOLATE_|@)env:([^}]+)\}\}")

# Bootstrap-env writes these sentinel ids into a workflow YAML row before
# the n8n placeholder workflow has actually been minted. If hydrate sees
# any of these substituted as a real value, it would silently bake the
# sentinel into the deployed JSON — and dehydrate's reverse-sub explicitly
# skips workflows.* / credentials.*, so the corruption is irreversible.
# Refuse hydration with a clear remediation pointer instead.
_SENTINEL_VALUES = frozenset({"placeholder", ""})
_SENTINEL_PREFIXES = ("your-",)


def _is_sentinel(val: str) -> bool:
    return val in _SENTINEL_VALUES or any(val.startswith(p) for p in _SENTINEL_PREFIXES)


def resolve(text: str, env_name: str, workspace: Path) -> str:
    """Replace all {{INTERPOLATE_env:...}} / {{@env:...}} tokens in text with config values."""
    data = load_yaml(env_name, workspace)
    load_env(env_name, workspace)

    def _replace(match: re.Match) -> str:
        dot_path = match.group(1)
        try:
            val = get_config_value(data, dot_path)
        except KeyError:
            raise ValueError(f"Placeholder {{{{@env:{dot_path}}}}} not found in {env_name}.yml")
        # List/dict values: emit a JSON-escaped JSON literal, suitable for
        # embedding into a JSON-string field in a workflow template (e.g. a
        # Code-node `jsCode`). The double-json.dumps + [1:-1] mirrors
        # js_resolver's escape pattern.
        if isinstance(val, (list, dict)):
            return json.dumps(json.dumps(val))[1:-1]
        sval = str(val)
        # Sentinel guard — only enforced for workflow / credential id paths,
        # since those are the resolver's most-load-bearing references and
        # the only ones reverse-sub can't repair.
        if _is_sentinel(sval) and (dot_path.startswith("workflows.") or dot_path.startswith("credentials.")):
            raise ValueError(
                f"Sentinel value '{sval}' resolved for {{{{@env:{dot_path}}}}} in {env_name}.yml. "
                f"Run `python3 <harness>/helpers/bootstrap_env.py --env {env_name}` to mint real IDs."
            )
        return sval

    return PATTERN.sub(_replace, text)
