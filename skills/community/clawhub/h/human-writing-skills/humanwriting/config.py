"""Small, explicit project defaults for repeatable writing audits."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


CONFIG_NAME = ".humanwriting.json"
SUPPORTED_KEYS = {"style", "document_type", "context", "allow"}


@dataclass(frozen=True)
class ProjectConfig:
    path: Path
    values: dict[str, Any]


def find_project_config(start: Path | None = None) -> Path | None:
    """Find the nearest project configuration without crossing the filesystem root."""

    current = (start or Path.cwd()).resolve()
    if current.is_file():
        current = current.parent
    for candidate_root in (current, *current.parents):
        candidate = candidate_root / CONFIG_NAME
        if candidate.is_file():
            return candidate
    return None


def load_project_config(start: Path | None = None) -> ProjectConfig | None:
    path = find_project_config(start)
    if path is None:
        return None
    try:
        values = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid {CONFIG_NAME}: {exc.msg}") from exc
    if not isinstance(values, dict):
        raise ValueError(f"{CONFIG_NAME} must contain one JSON object.")
    unknown = set(values) - SUPPORTED_KEYS
    if unknown:
        raise ValueError(f"Unsupported {CONFIG_NAME} keys: {', '.join(sorted(unknown))}")
    for key in ("style", "document_type", "context"):
        if key in values and (not isinstance(values[key], str) or not values[key].strip()):
            raise ValueError(f"{CONFIG_NAME} field '{key}' must be a non-empty string.")
    if "allow" in values and (
        not isinstance(values["allow"], list)
        or not all(isinstance(item, str) and item.strip() for item in values["allow"])
    ):
        raise ValueError(f"{CONFIG_NAME} field 'allow' must be a list of non-empty strings.")
    return ProjectConfig(path=path, values=values)


def apply_project_defaults(args: Any, raw_args: list[str]) -> ProjectConfig | None:
    """Apply only lightweight defaults; explicit flags always win.

    The configuration cannot activate audit profiles, sources, references, or other
    high-cost operations. It deliberately carries only stable project preferences.
    """

    if "--no-project-config" in raw_args:
        return None
    draft = getattr(args, "draft", None)
    start = Path.cwd() if not isinstance(draft, str) or draft == "-" else Path(draft).parent
    config = load_project_config(start)
    if config is None:
        return None
    values = config.values

    def supplied(*options: str) -> bool:
        return any(argument == option or argument.startswith(f"{option}=") for argument in raw_args for option in options)

    if "style" in values:
        if hasattr(args, "style") and not supplied("--style"):
            args.style = values["style"]
        if hasattr(args, "lint_style") and not supplied("--lint-style"):
            args.lint_style = values["style"]
    if "document_type" in values and hasattr(args, "document_type") and not supplied("--document-type"):
        args.document_type = values["document_type"]
    if "context" in values and hasattr(args, "context") and not args.context and not supplied("--context", "--outline"):
        configured_context = Path(values["context"])
        args.context = str(configured_context if configured_context.is_absolute() else config.path.parent / configured_context)
    if "allow" in values:
        for attribute, option in (("allow", "--allow"), ("lint_allow", "--lint-allow")):
            if hasattr(args, attribute) and not supplied(option):
                current = list(getattr(args, attribute) or [])
                setattr(args, attribute, list(dict.fromkeys([*values["allow"], *current])))
    return config
