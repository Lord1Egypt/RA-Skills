# Knowledge Organizer

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-cjke84%2Fknowledge--organizer-blue?logo=github)](https://github.com/cjke84/knowledge-organizer)

A knowledge-base workflow skill that turns article links, drafts, and notes into structured Markdown. You can write directly into Obsidian or sync to Feishu Knowledge Base and Tencent IMA.

## What it does

- process articles, links, and drafts into structured notes
- check duplicates and return a structured decision
- generate tags, summaries, and metadata
- download images into `assets/` and keep readable references, including common fields like `src`, `data_src`, `data-original`, `data-lazy-src`, `srcset`, `url`, `image_url`, and `original`
- write directly to Obsidian vault files
- orchestrate `destination=obsidian|feishu|ima` and `mode=once|sync`
- sync to Feishu through the official OpenClaw `openclaw-lark` plugin
- sync to Tencent IMA through the direct `import_doc` OpenAPI flow

## Capabilities

- OpenClaw- and Codex-compatible skill for knowledge organization
- Supports public-account posts, Xiaohongshu links, and ordinary web pages
- Works for Obsidian vault writes, Feishu sync, and IMA sync
- validates tags against the repository tag contract
- recommends directly linkable related notes
- supports one-shot import and incremental sync into Obsidian, Feishu, or IMA

## Use cases

- store in the knowledge base
- organize articles
- apply tags
- archive notes
- generate summaries
- suggest related notes

## How to use

1. Give OpenClaw an article link, a markdown draft, or a folder of drafts.
2. Choose a destination: `obsidian`, `feishu`, or `ima`.
3. Choose a mode: `once` for a single run or `sync` for incremental updates.
4. For Obsidian, provide a vault root. For Feishu and IMA, make sure the plugin or API credentials are ready.
5. The tool will dedupe first, then render the note or sync payload, then write or upload it.
6. You can call the sync orchestrator directly:

```bash
python3 -m scripts.knowledge_sync --destination obsidian --mode once --state .sync-state.json --vault-root /path/to/vault --markdown-path draft.md
python3 -m scripts.knowledge_sync --destination feishu --mode once --state .sync-state.json --markdown-path draft.md --dry-run
python3 -m scripts.knowledge_sync --destination ima --mode sync --state .sync-state.json --folder-path drafts/
python3 -m scripts.knowledge_sync --destination obsidian --mode once --state .sync-state.json --vault-root /path/to/vault --markdown-path draft.md --disable feishu,ima
```

Real Feishu imports require an OpenClaw host/plugin transport, which means `openclaw-lark` must expose `feishu_create_doc` / `feishu_update_doc` inside the OpenClaw host. The bare `python3 -m scripts.knowledge_sync` entrypoint is for validation and `--dry-run`, not a standalone Feishu transport.
If your OpenClaw host needs an explicit Feishu destination, use routing envs such as `FEISHU_WIKI_SPACE`, `FEISHU_FOLDER_TOKEN`, `FEISHU_WIKI_NODE`, `FEISHU_KB_ID`, or `FEISHU_FOLDER_ID`. These are optional placement hints, not always-required secrets.
`FEISHU_IMPORT_ENDPOINT` is only for intentional custom transport overrides and should stay unset for the normal `openclaw-lark` path.

## OpenClaw 2026.3.22 install notes

- Prefer native `openclaw skills install` / `openclaw skills update` for skill management
- If you distribute this repository as a release package, you can also use ClawHub or bundle flows, but keep the skill name as `knowledge-organizer`
- Keep `SKILL.md`, `scripts/`, `references/`, and `tests/` together as one directory skill in a location OpenClaw can discover
- Obsidian workflows need a valid absolute vault root and should prefer `OPENCLAW_KB_ROOT`
- Feishu sync depends on the official `openclaw-lark` plugin, with `feishu_create_doc` / `feishu_update_doc` available in the OpenClaw host
- Feishu CLI examples require an OpenClaw host/plugin transport; the bare `python3 -m scripts.knowledge_sync` entrypoint will fail clearly when transport is missing
- `FEISHU_WIKI_SPACE`, `FEISHU_FOLDER_TOKEN`, `FEISHU_WIKI_NODE`, `FEISHU_KB_ID`, and `FEISHU_FOLDER_ID` are optional Feishu placement envs rather than universally required credentials
- Xiaohongshu imports depend on `xiaohongshu-mcp`
- IMA sync depends on `IMA_OPENAPI_CLIENTID` and `IMA_OPENAPI_APIKEY`

## `draft.images` example

```yaml
images:
  - path: /absolute/path/to/local.png
    alt: Local image
  - src: https://example.com/cover.png
    alt: Remote image
  - srcset: https://example.com/cover-1x.png 1x, https://example.com/cover-2x.png 2x
    alt: Responsive image
```

`path` is for local files. `src` / `data_src` / `data-original` / `data-lazy-src` / `original` etc. are used for remote images; `srcset` prefers the highest-value candidate.

## Quick start

```bash
pytest -q
python scripts/check_duplicate.py "New Title" --content "$(cat draft.md)" --json
python scripts/find_related.py alpha beta --title "New Title" --json
```

## Related

- [中文介绍](README_CN.md)
- [Install Skill for Agent](INSTALL.md)
- [GitHub Repository](https://github.com/cjke84/knowledge-organizer)
