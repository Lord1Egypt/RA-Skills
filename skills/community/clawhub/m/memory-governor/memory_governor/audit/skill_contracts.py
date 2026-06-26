"""Machine-readable capability declarations embedded in skill contracts."""

from __future__ import annotations

import tomllib

from memory_governor.contract.capabilities import CAPABILITY_FAMILIES


def parse_capability_declaration(text: str) -> tuple[list[str] | None, str | None]:
    heading = "### Capability Declaration"
    start = text.find(heading)
    if start == -1:
        return None, None

    section = text[start + len(heading) :]
    next_heading = section.find("\n## ")
    if next_heading != -1:
        section = section[:next_heading]

    fence_start = section.find("```toml")
    if fence_start == -1:
        return None, "machine-readable capability declaration must use a fenced toml block"

    payload = section[fence_start + len("```toml") :]
    fence_end = payload.find("```")
    if fence_end == -1:
        return None, "machine-readable capability declaration is missing a closing fenced code block"

    raw_toml = payload[:fence_end].strip()
    try:
        parsed = tomllib.loads(raw_toml)
    except tomllib.TOMLDecodeError as exc:
        return None, f"machine-readable capability declaration failed to parse ({exc})"

    capabilities = parsed.get("capabilities")
    if not isinstance(capabilities, dict):
        return None, "machine-readable capability declaration must define a [capabilities] table"

    families = capabilities.get("families")
    if not isinstance(families, list) or not families or not all(isinstance(item, str) for item in families):
        return None, "machine-readable capability declaration must define capabilities.families as a non-empty string array"

    unknown = sorted(set(families) - set(CAPABILITY_FAMILIES))
    if unknown:
        return None, f"machine-readable capability declaration references unknown families: {', '.join(unknown)}"

    return families, None
