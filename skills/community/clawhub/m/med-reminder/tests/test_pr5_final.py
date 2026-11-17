"""
PR 5 final tests — SKILL.md and docs (issue #1 §8, AC 38).

SKILL.md must have valid frontmatter, route every write through reply.py
(no dispatch.py confirm/defer, no safe-write.sh write instructions, no
agent full-state writes), document the reply intents and exit codes, and
carry the interview quiet-hours rules. CLAUDE.md is not shipped, and the
retired safe-write.sh shim stays gone (#11).
"""
import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).parent.parent
SKILL = REPO / "SKILL.md"

# The one sanctioned non-reply writer: the §4 creation write, whose token
# asserts the file does not exist yet and whose content is global-only.
CREATION_WRITE = "safe_write.py --expected-sha256 absent"


def skill_text() -> str:
    return SKILL.read_text(encoding="utf-8")


def bash_blocks(text: str):
    """Yield (section_title, [command lines]) for every ```bash block."""
    section = "(frontmatter)"
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("## "):
            section = line[3:].strip()
        if line.strip() == "```bash":
            block, i = [], i + 1
            while i < len(lines) and lines[i].strip() != "```":
                block.append(lines[i])
                i += 1
            yield section, block
        i += 1


# ── Frontmatter (AC 38) ───────────────────────────────────────────────────────

def test_skill_md_has_valid_frontmatter():
    text = skill_text()
    assert text.startswith("---\n"), "SKILL.md must start with a YAML block"
    end = text.index("\n---\n", 4)
    fm = text[4:end]
    fields = dict(
        line.split(":", 1) for line in fm.splitlines() if ":" in line
    )
    assert fields.get("name", "").strip() == "med-reminder"
    description = fields.get("description", "").strip()
    assert description, "frontmatter needs a one-line description"
    assert "\n" not in description


# ── Every write goes through reply.py (AC 38) ────────────────────────────────

def test_no_dispatch_confirm_or_defer_instructions():
    text = skill_text()
    assert not re.search(r"dispatch\.py (confirm|defer)", text), (
        "reply handling must use reply.py, not the legacy dispatch writers"
    )


def test_no_safe_write_sh_invocations():
    for section, block in bash_blocks(skill_text()):
        for line in block:
            assert "safe-write.sh" not in line, (
                f"{section}: safe-write.sh must not be invoked — "
                "it is a deprecated shim, writes go through reply.py"
            )


def test_reply_handler_commands_are_all_reply_py():
    """Section 7 onward: every runnable command invokes reply.py."""
    saw_section_7 = False
    for section, block in bash_blocks(skill_text()):
        if section.startswith("Section 7"):
            saw_section_7 = True
        if not saw_section_7:
            continue
        for line in block:
            code = line.split("#", 1)[0].strip()
            if not code or code.startswith(("echo", "EOF", "{", "}", '"')):
                continue
            assert "reply.py" in code, (
                f"§{section}: non-reply.py write command: {code!r}"
            )


def test_only_non_reply_writer_is_the_creation_write():
    """safe_write.py appears only as the §4 creation write (absent token)."""
    text = skill_text()
    for section, block in bash_blocks(skill_text()):
        for line in block:
            if "safe_write.py" in line:
                assert CREATION_WRITE in line, (
                    f"{section}: safe_write.py may only be used with the "
                    "creation token --expected-sha256 absent"
                )


def test_no_full_state_write_instructions():
    text = skill_text()
    for banned in (
        "write the state file",
        "echo <updated-json>",
        "Build the full updated state",
        "Write via `safe-write.sh`",
    ):
        assert banned not in text, f"full-state write instruction: {banned!r}"


# ── Reply intents and exit codes are documented (issue §8) ───────────────────

def test_reply_intents_documented():
    text = skill_text()
    for needle in (
        "reply.py snooze",
        "reply.py skip",
        "reply.py undo",
        "--taken-at",
        "--position",
        "--dose-taken",
    ):
        assert needle in text, f"missing reply intent/option: {needle}"


def test_exit_code_handling_documented():
    text = skill_text()
    assert "exits 3" in text and "--force" in text, (
        "exit 3 (duplicate) and the gated --force nonce must be documented"
    )
    assert "exits 4" in text and "--dose" in text, (
        "exit 4 (ambiguous dose) and --dose must be documented"
    )


# ── Interview quiet-hours rules (issue §8) ────────────────────────────────────

def test_interview_quiet_hours_rules_present():
    text = skill_text()
    assert "No dose time inside the quiet window" in text
    assert "T+late" in text, "the T+late nudge vs quiet-hours check is missing"
    assert "quiet_policy" in text, (
        "interval meds must be asked for schedule.quiet_policy (ignore|shift)"
    )


# ── CLAUDE.md is not shipped (AC 38) ─────────────────────────────────────────

def test_claude_md_not_shipped():
    assert not (REPO / "CLAUDE.md").exists()


# ── safe-write.sh is retired (#11) ───────────────────────────────────────────

def test_safe_write_sh_removed():
    assert not (REPO / "safe-write.sh").exists()
