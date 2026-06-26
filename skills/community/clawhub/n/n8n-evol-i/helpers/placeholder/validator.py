"""Post-hydration validation: check for residual placeholders.

Recognises the canonical long form (`INTERPOLATE_<type>:...`) and short alias
(`@<type>:...`). Any leftover token after hydration is treated as a residual —
including stale older-syntax forms (`{{@:type:...}}`, `{{INTERPOLATE:type:...}}`,
`{{HYDRATE:type:...}}`), which won't match the new patterns and will therefore
surface as residuals if a template hasn't been migrated yet.
"""
import re
from pathlib import Path

# Match the canonical new forms (`INTERPOLATE_<type>:...`, `@<type>:...`) AND the
# stale older syntaxes (`{{INTERPOLATE:type:...}}`, `{{@:type:...}}`, legacy
# `{{HYDRATE:type:...}}`) so a forgotten template surfaces loudly post-hydrate
# rather than silently shipping literal placeholder text into n8n.
RESIDUAL_PATTERN = re.compile(r"\{\{(?:HYDRATE:|INTERPOLATE_|INTERPOLATE:|@:|@)[^}\s][^}]*\}\}")


def check_residuals(text: str) -> list[str]:
    """Return list of all residual placeholder tokens found in text."""
    return RESIDUAL_PATTERN.findall(text)


def validate(text: str, source_label: str = "") -> None:
    """Raise ValueError if any residual placeholders remain after hydration."""
    residuals = check_residuals(text)
    if residuals:
        label = f" in {source_label}" if source_label else ""
        raise ValueError(
            f"Residual placeholders found{label}: {', '.join(residuals)}\n"
            "Check that all placeholder paths resolve correctly."
        )


def validate_no_absolute_paths(text: str) -> None:
    """Raise ValueError if any placeholder contains an absolute path."""
    absolutes = re.findall(r"\{\{(?:INTERPOLATE_|@)\w+:(/[^}]+)\}\}", text)
    if absolutes:
        raise ValueError(
            f"Absolute paths are forbidden in placeholders: {', '.join(absolutes)}"
        )
