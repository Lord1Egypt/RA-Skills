"""
test_skill_docs_in_sync.py — SKILL.md's own claims, checked against the code.

`test_tool_docs_in_sync.py` covers references/agent.md's per-tool argument
table. Nothing covered SKILL.md itself, and a 2026-09-10 review found three
drifts there: a retention window documented as 30 days against code keeping 60,
a tool named `image` that has never existed (it is `view_image`), and a launchd
plist section pointing at a binary path that is not installed.

These assert contracts, not prose shape. Restructuring SKILL.md stays free.
"""
from __future__ import annotations

import re
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
DOCS = ("SKILL.md", "README.md", "references/agent.md")


def _read(name: str) -> str:
    return (SKILL_DIR / name).read_text()


def test_reliability_tracker_window_matches_the_code():
    """morning_briefing.py trims the tracker to a fixed number of days. The docs
    said 30 in three places while the code kept 60 -- a number a human would
    trust when reading household/briefing_reliability.json."""
    source = _read("features/briefing/morning_briefing.py")
    match = re.search(r'tracker\["days"\] = tracker\["days"\]\[-(\d+):\]', source)
    assert match, "retention slice not found in morning_briefing.py -- parser broken"
    days = match.group(1)
    for doc in ("SKILL.md", "README.md"):
        text = re.sub(r"\s+", " ", _read(doc))
        for wrong in re.findall(r"(\d+)-day reliability tracker", text):
            assert wrong == days, (
                f"{doc} says {wrong}-day reliability tracker; "
                f"morning_briefing.py keeps {days}"
            )


def test_docs_never_name_a_nonexistent_image_tool():
    """The runtime tool is `view_image`. SKILL.md used `image` in two places and
    `view_image` in two others, disagreeing with itself. An agent that looks for
    `image`, fails to find it, and falls back to describing the photo is the
    exact act-don't-describe failure that section exists to prevent."""
    for doc in DOCS:
        # Normalize first: this prose is hard-wrapped, so "with the" and
        # "`image`" routinely land on different lines and an unnormalized
        # pattern matches nothing and passes vacuously (caught by mutation).
        text = re.sub(r"\s+", " ", _read(doc))
        # `image` as a tool reference, not as a word (image_paths, an image, ...)
        bad = re.findall(r"(?:the|call|use|using) `image`", text)
        assert not bad, f"{doc} refers to a tool named `image`; it is `view_image`"


def test_no_doc_presents_the_retired_gateway_plist_as_installable():
    """com.openclaw.daemon.plist ran /usr/local/bin/openclaw, which does not
    exist, and loading it alongside OpenClaw's own ai.openclaw.gateway starts a
    second gateway contending for port 18789. The file was removed 2026-09-10;
    no doc may hand a reader an install command for it."""
    assert not (SKILL_DIR / "com.openclaw.daemon.plist").exists(), (
        "the retired plist is back on disk; docs tell readers not to install it"
    )
    for doc in DOCS:
        text = _read(doc)
        for line in text.splitlines():
            if "com.openclaw.daemon" not in line:
                continue
            assert not re.search(r"launchctl load|^\s*cp\s", line), (
                f"{doc} still shows an install step for the retired plist: {line.strip()!r}"
            )


def test_no_doc_instructs_populating_a_dotenv():
    """Credentials come from Keychain through gog. `.env.example` survived the
    migration telling readers to mint a refresh token with two scripts that were
    already deleted, and SKILL.md says plainly there is no .env any more."""
    assert not (SKILL_DIR / ".env.example").exists(), (
        ".env.example is back; SKILL.md says nothing reads a .env for credentials"
    )
    for doc in DOCS:
        text = re.sub(r"\s+", " ", _read(doc))
        assert not re.search(r"[Cc]opy (this file|\.env\.example) to `?\.env", text), (
            f"{doc} tells the reader to create a .env, which nothing reads"
        )
