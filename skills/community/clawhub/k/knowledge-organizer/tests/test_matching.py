from scripts import check_duplicate as check_duplicate_module
from scripts import find_related as find_related_module
import json
import subprocess
import sys


def _write_note(
    path,
    *,
    title,
    source_url=None,
    canonical_hash=None,
    aliases=None,
    tags=None,
    body="Body",
):
    frontmatter_lines = ["---", f"title: {title}"]
    if aliases is not None:
        frontmatter_lines.append("aliases:")
        for alias in aliases:
            frontmatter_lines.append(f"  - {alias}")
    if tags is not None:
        frontmatter_lines.append("tags:")
        for tag in tags:
            frontmatter_lines.append(f"  - {tag}")
    if source_url is not None:
        frontmatter_lines.append(f"source_url: {source_url}")
    if canonical_hash is not None:
        frontmatter_lines.append(f"canonical_hash: {canonical_hash}")
    frontmatter_lines.append("---")
    frontmatter_lines.extend(["", f"# {title}", "", body, ""])
    path.write_text("\n".join(frontmatter_lines), encoding="utf-8")


def test_exact_url_match_returns_non_similarity_decision(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    note = vault / "existing.md"
    _write_note(
        note,
        title="Existing Note",
        aliases=["Alt Existing"],
        source_url="https://example.com/article",
        canonical_hash="hash-1",
        tags=["alpha"],
        body="Completely different body.",
    )

    decision = check_duplicate_module.decide_duplicate(
        "Incoming Note",
        """---
title: Incoming Note
source_url: https://example.com/article
canonical_hash: hash-2
---

# Incoming Note

Different body entirely.
""",
        kb_path=str(vault),
        threshold=0.99,
    )

    assert decision["matches"], "Expected at least one match for canonical URL duplicate"
    assert decision["matches"][0]["match_type"] == "canonical_url"
    assert "url" in decision["reason"].lower()


def test_exact_canonical_hash_match_returns_decision(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    note = vault / "existing.md"
    _write_note(
        note,
        title="Existing Note",
        aliases=["Alt Existing"],
        source_url="https://example.com/other",
        canonical_hash="same-hash",
        tags=["alpha"],
        body="Shared body text.",
    )

    decision = check_duplicate_module.decide_duplicate(
        "Incoming Note",
        """---
title: Incoming Note
source_url: https://example.com/new
---

# Incoming Note

Shared body text.
""",
        kb_path=str(vault),
        threshold=0.99,
    )

    assert decision["matches"], "Expected at least one match for canonical hash duplicate"
    assert decision["matches"][0]["match_type"] == "sanitized_content_hash"
    assert "hash" in decision["reason"].lower()


def test_related_note_discovery_returns_wikilink_ready_titles(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    note = vault / "alpha.md"
    _write_note(
        note,
        title="Alpha Article",
        aliases=["Alpha Alt"],
        tags=["alpha", "reading-notes"],
        body="Some content.",
    )

    related = find_related_module.find_related(["alpha"], "Unrelated Title", str(vault), limit=5)

    assert related, "Expected a related note"
    assert related[0]["title"] == "Alpha Article"
    assert related[0]["wikilink"] == "[[Alpha Article]]"


def test_duplicate_cli_exits_successfully_for_duplicate_match(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    note = vault / "existing.md"
    _write_note(
        note,
        title="Existing Note",
        source_url="https://example.com/article",
        canonical_hash="same-hash",
        tags=["alpha"],
        body="Shared body text.",
    )

    script = check_duplicate_module.__file__
    result = subprocess.run(
        [
            sys.executable,
            script,
            "Incoming Note",
            "--content",
            """---
title: Incoming Note
source_url: https://example.com/article
---

# Incoming Note

Different body entirely.
""",
            "--kb",
            str(vault),
            "--json",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    decision = json.loads(result.stdout)
    assert decision["matches"], "Expected the CLI to return a structured duplicate decision"
    assert decision["action"] in {"skip", "merge", "overwrite", "create_new_version"}
