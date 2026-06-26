from scripts import markdown_helpers


def test_scan_knowledge_base_normalizes_tags_and_keywords(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    note = vault / "article.md"
    note.write_text(
        """---
tags:
  - alpha
keywords: beta
---

# Title

Body
""",
        encoding="utf-8",
    )

    articles = markdown_helpers.scan_knowledge_base(str(vault))
    assert articles, "Expected at least one article"
    article = articles[0]
    assert article["tags"] == ["alpha"]
    assert article["keywords"] == ["beta"]


def test_load_frontmatter_respects_top_level_fence():
    content = """---
tags:
  - alpha
---

# Title

Body
---
Later fence fragments should not matter.
"""

    frontmatter = markdown_helpers.load_frontmatter(content)
    assert frontmatter == {"tags": ["alpha"]}


def test_load_frontmatter_requires_closing_fence():
    content = """---
tags:
  - alpha

# Missing closing fence
Body"""

    assert markdown_helpers.load_frontmatter(content) == {}


def test_scan_knowledge_base_logs_frontmatter_errors(tmp_path, capfd):
    vault = tmp_path / "vault"
    vault.mkdir()
    note = vault / "article.md"
    note.write_text(
        """---
tags:
  - alpha
keywords: [unclosed
---

# Title

Body
""",
        encoding="utf-8",
    )

    articles = markdown_helpers.scan_knowledge_base(str(vault))
    stderr = capfd.readouterr().err

    assert articles, "Expected article despite invalid frontmatter"
    assert articles[0]["tags"] == []
    assert "Error parsing frontmatter for" in stderr


def test_strip_frontmatter_removes_section():
    content = """---
tags:
  - alpha
---

Body
"""

    assert markdown_helpers.strip_frontmatter(content) == "Body"


def test_load_frontmatter_handles_parse_errors():
    content = """---
tags:
  - alpha
keywords: [unclosed
---

# Title

Body
"""
    errors: list[str] = []

    assert markdown_helpers.load_frontmatter(
        content, on_error=lambda exc: errors.append(str(exc))
    ) == {}
    assert errors, "Expected on_error to be called when YAML fails"
