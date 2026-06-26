from scripts import find_related as find_related_module


def test_find_related_uses_keywords_when_tags_miss(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    note = vault / "article.md"
    note.write_text(
        """---
tags:
  - alpha
keywords:
  - beta
---

# Alpha Article

Some content.
""",
        encoding="utf-8",
    )

    without_keywords = find_related_module.find_related(
        ["gamma"], "Unrelated Title", str(vault), limit=1
    )
    assert without_keywords == []

    with_keywords = find_related_module.find_related(
        ["gamma"], "Unrelated Title", str(vault), limit=1, keywords=["beta"]
    )
    assert with_keywords, "Expected related article when auxiliary keywords overlap"
    assert with_keywords[0]["score"] > 0.1
