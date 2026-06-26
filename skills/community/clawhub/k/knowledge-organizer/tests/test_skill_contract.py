from pathlib import Path

from scripts import check_duplicate, find_related, markdown_helpers, obsidian_note, settings


def test_skill_contract_mentions_obsidian_frontmatter_wikilinks_and_embeds():
    repo_root = Path(__file__).resolve().parents[1]
    skill_text = (repo_root / "SKILL.md").read_text(encoding="utf-8")
    tag_text = (repo_root / "references" / "tag-system.md").read_text(encoding="utf-8")

    required_skill_phrases = [
        "structured Markdown",
        "optional sync targets for Obsidian, Feishu, and Tencent IMA",
        "YAML frontmatter",
        "wikilink",
        "embed",
        "destination_path",
        "OPENCLAW_KB_ROOT",
        "absolute path",
        "frontmatter / wikilink / embed / block id",
        "prefer `xiaohongshu-mcp` for Xiaohongshu links",
        "For WeChat public-account imports, read `references/wechat-import.md`",
        "Before running script-based import flows, prefer checking `scripts/check_runtime.py`",
        "destination=obsidian|feishu|ima",
        "mode=once|sync",
        "openclaw-lark",
        "feishu_create_doc",
        "feishu_update_doc",
        "import_doc OpenAPI",
    ]
    required_tag_phrases = [
        "至少 1 个领域标签 + 1 个类型标签",
        "总标签数 5-10 个",
        "复用优先",
        "技能契约对齐",
    ]

    for phrase in required_skill_phrases:
        assert phrase in skill_text

    for phrase in required_tag_phrases:
        assert phrase in tag_text


def test_skill_contract_mentions_openclaw_2026_install_and_dependency_notes():
    repo_root = Path(__file__).resolve().parents[1]
    skill_text = (repo_root / "SKILL.md").read_text(encoding="utf-8")

    required_skill_phrases = [
        "description: Use when",
        "OpenClaw 2026.3.22 Notes",
        "`openclaw skills install`",
        "ClawHub",
        "Install this repository as a directory skill",
        "`openclaw-lark` plugin",
        "`feishu_create_doc`",
        "`feishu_update_doc`",
        "OpenClaw host/plugin transport",
        "`xiaohongshu-mcp`",
        "`OPENCLAW_KB_ROOT`",
    ]

    for phrase in required_skill_phrases:
        assert phrase in skill_text


def test_skill_frontmatter_declares_runtime_requirements_for_openclaw():
    repo_root = Path(__file__).resolve().parents[1]
    skill_text = (repo_root / "SKILL.md").read_text(encoding="utf-8")

    required_metadata_phrases = [
        "metadata:",
        "openclaw:",
        "requires:",
        "env:",
        "- OPENCLAW_KB_ROOT",
        "- IMA_OPENAPI_CLIENTID",
        "- IMA_OPENAPI_APIKEY",
        "bins:",
        "- python3",
        "anyBins:",
        "- openclaw",
        "integrations:",
        "- openclaw-lark",
        "- xiaohongshu-mcp",
        "optionalEnv:",
        "- FEISHU_WIKI_SPACE",
        "- FEISHU_FOLDER_TOKEN",
        "- FEISHU_WIKI_NODE",
        "- FEISHU_KB_ID",
        "- FEISHU_FOLDER_ID",
        "- FEISHU_IMPORT_ENDPOINT",
    ]

    for phrase in required_metadata_phrases:
        assert phrase in skill_text

    for phrase in [
        "- FEISHU_APP_ID",
        "- FEISHU_APP_SECRET",
        "- FEISHU_ACCESS_TOKEN",
    ]:
        assert phrase not in skill_text


def test_docs_mention_openclaw_2026_install_flow_and_dependencies():
    repo_root = Path(__file__).resolve().parents[1]
    readme_text = (repo_root / "README.md").read_text(encoding="utf-8")
    readme_en_text = (repo_root / "README_EN.md").read_text(encoding="utf-8")
    readme_cn_text = (repo_root / "README_CN.md").read_text(encoding="utf-8")
    install_text = (repo_root / "INSTALL.md").read_text(encoding="utf-8")

    for phrase in [
        "OpenClaw 2026.3.22",
        "`openclaw skills install`",
        "ClawHub",
        "`OPENCLAW_KB_ROOT`",
        "`openclaw-lark`",
        "`feishu_create_doc`",
        "`feishu_update_doc`",
        "OpenClaw host/plugin transport",
        "`FEISHU_WIKI_SPACE`",
        "`FEISHU_FOLDER_TOKEN`",
        "`FEISHU_KB_ID`",
        "`FEISHU_FOLDER_ID`",
    ]:
        assert phrase in readme_en_text

    for phrase in [
        "OpenClaw 2026.3.22",
        "`openclaw skills install`",
        "ClawHub",
        "`OPENCLAW_KB_ROOT`",
        "`openclaw-lark`",
        "`feishu_create_doc`",
        "`feishu_update_doc`",
        "OpenClaw host/plugin transport",
        "`FEISHU_WIKI_SPACE`",
        "`FEISHU_FOLDER_TOKEN`",
        "`FEISHU_KB_ID`",
        "`FEISHU_FOLDER_ID`",
    ]:
        assert phrase in readme_text

    for phrase in [
        "OpenClaw 2026.3.22",
        "`openclaw skills install`",
        "ClawHub",
        "`OPENCLAW_KB_ROOT`",
        "`openclaw-lark`",
        "`feishu_create_doc`",
        "`feishu_update_doc`",
        "OpenClaw host/plugin transport",
        "`FEISHU_WIKI_SPACE`",
        "`FEISHU_FOLDER_TOKEN`",
        "`FEISHU_KB_ID`",
        "`FEISHU_FOLDER_ID`",
    ]:
        assert phrase in readme_cn_text

    for phrase in [
        "`openclaw skills install`",
        "ClawHub",
        "`OPENCLAW_KB_ROOT`",
        "`openclaw-lark`",
        "`feishu_create_doc`",
        "`feishu_update_doc`",
        "`xiaohongshu-mcp`",
    ]:
        assert phrase in install_text


def test_skill_scripts_import_without_manual_path_tweaks():
    assert callable(check_duplicate.decide_duplicate)
    assert callable(find_related.find_related)
    assert callable(markdown_helpers.scan_knowledge_base)
    assert callable(obsidian_note.render_obsidian_note)
    assert callable(settings.resolve_vault_root)
