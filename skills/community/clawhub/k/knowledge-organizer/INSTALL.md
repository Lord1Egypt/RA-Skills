# Install Skill

## English

```text
Please install cjke84/knowledge-organizer as a usable directory skill for OpenClaw 2026.3.22 or newer. Prefer `openclaw skills install` / `openclaw skills update`, or package it through ClawHub / bundle flows while keeping the skill name as knowledge-organizer. Keep SKILL.md, scripts/, references/, and tests/ together, confirm it works in OpenClaw and Codex, run pytest -q and verify it passes, and follow the repository instructions for any paths or environment variables. The skill supports destination=obsidian|feishu|ima and mode=once|sync, prefers `OPENCLAW_KB_ROOT` for the Obsidian vault root, uses the official `openclaw-lark` plugin plus `feishu_create_doc` / `feishu_update_doc` for Feishu, treats `FEISHU_WIKI_SPACE` / `FEISHU_FOLDER_TOKEN` / `FEISHU_WIKI_NODE` / `FEISHU_KB_ID` / `FEISHU_FOLDER_ID` as optional Feishu placement envs, leaves `FEISHU_IMPORT_ENDPOINT` unset unless a custom transport override is intended, depends on `xiaohongshu-mcp` for Xiaohongshu imports, and uses import_doc OpenAPI for IMA.
```

## 中文

```text
请把 cjke84/knowledge-organizer 安装成适用于 OpenClaw 2026.3.22 及以上版本的目录型 skill。优先使用 `openclaw skills install` / `openclaw skills update`，或通过 ClawHub / bundle 方式分发，并保持 skill 名称为 knowledge-organizer。保留 SKILL.md、scripts/、references/、tests/ 在同一个 skill 目录中，确认它可在 OpenClaw 和 Codex 中使用，安装后运行 pytest -q 并确认通过，路径或环境变量优先遵循仓库说明。这个 skill 支持 destination=obsidian|feishu|ima 和 mode=once|sync，Obsidian 优先使用 `OPENCLAW_KB_ROOT` 作为 vault root，飞书通过官方 `openclaw-lark` 插件和 `feishu_create_doc` / `feishu_update_doc` 接入，`FEISHU_WIKI_SPACE` / `FEISHU_FOLDER_TOKEN` / `FEISHU_WIKI_NODE` / `FEISHU_KB_ID` / `FEISHU_FOLDER_ID` 只是可选的飞书落点配置，`FEISHU_IMPORT_ENDPOINT` 仅在明确需要自定义 transport 覆盖时才设置，小红书导入依赖 `xiaohongshu-mcp`，IMA 通过 import_doc OpenAPI 接入。
```
