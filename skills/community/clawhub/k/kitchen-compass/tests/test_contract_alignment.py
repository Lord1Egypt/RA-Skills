"""Contract test: recipe-schema.md and contract.py must declare the same enums.

This is the highest-value test in the suite. A diff here means either the
docs or the code drifted; both must be fixed in the same commit.
"""
import re
from pathlib import Path

from contract import ENUM_VALUES, COMPOSITION_VALUE_SET


SCHEMA = Path(__file__).resolve().parents[1] / "references" / "recipe-schema.md"
ENUM_HEADING_RE = re.compile(r"^### `([^`]+)`\s*$", re.MULTILINE)
BULLET_VALUE_RE = re.compile(r"^-\s+`([^`]+)`\s*$")


def _parse_enums(text):
    enums = {}
    for match in ENUM_HEADING_RE.finditer(text):
        name = match.group(1)
        start = match.end()
        next_section = re.search(r"^#", text[start:], re.MULTILINE)
        block = text[start:start + next_section.start()] if next_section else text[start:]
        values = []
        for line in block.splitlines():
            m = BULLET_VALUE_RE.match(line.strip())
            if m:
                values.append(m.group(1))
        if values:
            enums[name] = set(values)
    return enums


def test_enums_align_with_schema_doc():
    parsed = _parse_enums(SCHEMA.read_text())
    # Composition is documented under its own subsection, not as a ### enum, so handled separately.
    composition_block = SCHEMA.read_text().split("### `Composition`", 1)[1]
    composition = {m.group(1) for line in composition_block.splitlines() if (m := BULLET_VALUE_RE.match(line.strip()))}

    for enum_key, code_values in ENUM_VALUES.items():
        assert enum_key in parsed, f"recipe-schema.md does not document enum '{enum_key}'"
        assert parsed[enum_key] == code_values, (
            f"Enum '{enum_key}' mismatch.\n"
            f"  contract.py: {sorted(code_values)}\n"
            f"  recipe-schema.md: {sorted(parsed[enum_key])}"
        )

    assert composition == COMPOSITION_VALUE_SET, (
        f"Composition values mismatch.\n"
        f"  contract.py: {sorted(COMPOSITION_VALUE_SET)}\n"
        f"  recipe-schema.md: {sorted(composition)}"
    )
