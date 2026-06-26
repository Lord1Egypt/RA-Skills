"""Generate audit-trail prompt files alongside exported artifacts.

Phase 1: every export path writes a timestamped ``generation-prompt-*.md``
into the export directory so humans can trace what blueprint was rendered,
with what theme, and by which CLI invocation.

Anti-stale invariant:
  - Always regenerated, never reused as cache/input.
  - Filename includes timestamp to preserve history.
"""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def generate_prompt_file(
    blueprint: dict[str, Any],
    output_dir: Path,
    *,
    theme: str = "light",
    fmt: str = "svg",
) -> Path:
    """Write a timestamped audit-prompt file and return its path."""
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")[:-3]
    prompt_path = output_dir / f"generation-prompt-{timestamp}.md"  # includes milliseconds

    meta = blueprint.get("meta", {})
    lib = blueprint.get("library", {})

    blueprint_hash = hashlib.sha256(
        json.dumps(blueprint, sort_keys=True, ensure_ascii=False).encode()
    ).hexdigest()

    prompt_path.write_text(
        _build_content(
            blueprint_hash=blueprint_hash,
            schema_version=meta.get("version", "1.0"),
            industry=meta.get("industry", ""),
            n_caps=len(lib.get("capabilities", [])),
            n_actors=len(lib.get("actors", [])),
            n_systems=len(lib.get("systems", [])),
            n_flow_steps=len(lib.get("flowSteps", [])),
            theme=theme,
            fmt=fmt,
            timestamp=timestamp,
            cli_args=sys.argv.copy(),
        ),
        encoding="utf-8",
    )

    return prompt_path


def _build_content(
    *,
    blueprint_hash: str,
    schema_version: str,
    industry: str,
    n_caps: int,
    n_actors: int,
    n_systems: int,
    n_flow_steps: int,
    theme: str,
    fmt: str,
    timestamp: str,
    cli_args: list[str],
) -> str:
    generated_at = datetime.now().isoformat()
    cli_yaml = "\n".join(f"  - {_yaml_str(a)}" for a in cli_args)

    return f"""\
# Blueprint Export Prompt

**Generated**: {generated_at}
**Timestamp**: {timestamp}
**Blueprint Hash**: sha256:{blueprint_hash[:16]}...
**Schema Version**: {schema_version}

---

## Blueprint Summary

- **Industry**: {industry or "common"}
- **Capabilities**: {n_caps}
- **Actors**: {n_actors}
- **Systems**: {n_systems}
- **Flow Steps**: {n_flow_steps}

## Export Configuration

- **Format**: {fmt}
- **Theme**: {theme}

---

## Provenance

blueprint_hash: sha256:{blueprint_hash}
schema_version: "{schema_version}"
generated_at: "{generated_at}"
timestamp: "{timestamp}"
cli_args:
{cli_yaml}
"""


def _yaml_str(s: str) -> str:
    """Minimal YAML scalar quoting."""
    if not s:
        return '""'
    if any(c in s for c in (":", "{", "}", "[", "]", ",", "&", "*", "#", "?", "|", "-", "<", ">", "=", "!", "%", "@", "`", '"', "'")):
        return json.dumps(s)
    if s.strip() != s:
        return json.dumps(s)
    return s
