"""Resolve {{INTERPOLATE_txt|json|html:path}} (alias `{{@...}}`) placeholders against workspace files."""
import json
import re
from pathlib import Path

PATTERN = re.compile(r"\{\{(?:INTERPOLATE_|@)(txt|json|html):([^}]+)\}\}")


def resolve(text: str, workspace: Path) -> str:
    """Replace all {{INTERPOLATE_txt|json|html:...}} / {{@...}} tokens with file contents."""

    def _replace(match: re.Match) -> str:
        kind = match.group(1)
        rel_path = match.group(2).strip()
        if rel_path.startswith("/"):
            raise ValueError(
                f"Absolute paths in placeholders are forbidden: {{{{@{kind}:{rel_path}}}}}"
            )
        full = workspace / rel_path
        if not full.exists():
            placeholder = "{{@" + kind + ":" + rel_path + "}}"
            raise FileNotFoundError(f"Placeholder file not found: {full} (from {placeholder})")
        content = full.read_text(encoding="utf-8")
        if kind == "json":
            # Return a JSON-stringified version (as a JSON string value)
            return json.dumps(content)
        return content

    return PATTERN.sub(_replace, text)
