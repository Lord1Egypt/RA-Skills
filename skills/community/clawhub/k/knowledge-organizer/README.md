# Knowledge Organizer

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-cjke84%2Fknowledge--organizer-blue?logo=github)](https://github.com/cjke84/knowledge-organizer)

一个面向知识库工作流的整理工具，用于把文章、链接和草稿整理成结构化笔记。你可以直接写入 Obsidian，也可以同步到飞书知识库和腾讯 IMA。

## 文档入口

- [English README](README_EN.md)
- [中文介绍](README_CN.md)
- [Install Skill for Agent](INSTALL.md)
- [GitHub 仓库](https://github.com/cjke84/knowledge-organizer)

## 能力概览

- 一次处理文章、链接和草稿，输出可直接落盘的结构化笔记
- 在写入前执行重复检测，支持结构化决策结果（decision）
- 生成标签、摘要、元数据和相关文章建议
- 自动下载图片到 `assets/` 并保留可读引用，支持 `src` / `data_src` / `data-original` / `data-lazy-src` / `srcset` / `url` / `image_url` / `original` 等常见字段
- 支持多来源输入，包括公众号文章、小红书链接和普通网页
- 统一编排 `destination=obsidian|feishu|ima` 和 `mode=once|sync`
- Obsidian 直接写入本地 vault
- Feishu 通过 OpenClaw 官方 `openclaw-lark` 插件接入
- IMA 通过 `import_doc` OpenAPI 直连

## 快速使用

```bash
pytest -q
python scripts/check_duplicate.py "新标题" --content "$(cat draft.md)" --json
python scripts/find_related.py alpha beta --title "新标题" --json
```

## 使用方法

1. 把文章链接或草稿交给 OpenClaw。
2. 选择目标：`obsidian`、`feishu` 或 `ima`。
3. 选择模式：`once` 一次导入，或 `sync` 增量同步。
4. Obsidian 需要提供 vault 路径；Feishu 和 IMA 需要先准备好对应插件或 API 凭据。
5. 工具会先去重，再生成摘要、标签和元数据，最后写入本地笔记或同步到飞书 / IMA。
6. 你也可以直接调用同步编排器，例如：

```bash
python3 -m scripts.knowledge_sync --destination obsidian --mode once --state .sync-state.json --vault-root /path/to/vault --markdown-path draft.md
python3 -m scripts.knowledge_sync --destination feishu --mode once --state .sync-state.json --markdown-path draft.md --dry-run
python3 -m scripts.knowledge_sync --destination ima --mode sync --state .sync-state.json --folder-path drafts/
python3 -m scripts.knowledge_sync --destination obsidian --mode once --state .sync-state.json --vault-root /path/to/vault --markdown-path draft.md --disable feishu,ima
```

飞书真实导入需要 OpenClaw host/plugin transport；也就是要让 `openclaw-lark` 在 OpenClaw 主机里暴露 `feishu_create_doc` / `feishu_update_doc`，裸 `python3 -m scripts.knowledge_sync` 入口只适合校验参数或 `--dry-run`。
如果 OpenClaw 主机需要明确的飞书落点，可以设置 `FEISHU_WIKI_SPACE`、`FEISHU_FOLDER_TOKEN`、`FEISHU_WIKI_NODE`、`FEISHU_KB_ID` 或 `FEISHU_FOLDER_ID`。这些是可选的路由提示，不是所有场景都必须提供的密钥。
`FEISHU_IMPORT_ENDPOINT` 只用于你明确想覆盖默认 transport 的自定义接入，正常 `openclaw-lark` 路径下不要随手设置。

## OpenClaw 2026.3.22 安装说明

- 推荐使用原生 `openclaw skills install` / `openclaw skills update` 管理 skill
- 如果你通过发布包分发，也可以走 ClawHub 或 bundle 安装，但需要保持 skill 名称为 `knowledge-organizer`
- 安装时请保留 `SKILL.md`、`scripts/`、`references/` 和 `tests/`，按目录型 skill 一起放入 OpenClaw 可发现的位置
- Obsidian 工作流需要可用的绝对路径 vault root，优先使用 `OPENCLAW_KB_ROOT`
- 飞书同步依赖官方 `openclaw-lark` 插件，以及 OpenClaw 主机里可用的 `feishu_create_doc` / `feishu_update_doc`
- 飞书 CLI 示例依赖 OpenClaw host/plugin transport；裸 `python3 -m scripts.knowledge_sync` 入口会在缺少 transport 时明确报错
- `FEISHU_WIKI_SPACE`、`FEISHU_FOLDER_TOKEN`、`FEISHU_WIKI_NODE`、`FEISHU_KB_ID`、`FEISHU_FOLDER_ID` 属于可选的飞书落点配置，不是统一必填凭据
- 小红书导入依赖 `xiaohongshu-mcp`
- IMA 同步依赖 `IMA_OPENAPI_CLIENTID` 和 `IMA_OPENAPI_APIKEY`

## 适用场景

- 定期整理微信收藏的文章
- 建立个人知识库体系
- 团队知识沉淀
- 学术资料归档
- 需要把同一份内容同步到 Obsidian、飞书和 IMA

## `draft.images` 示例

```yaml
images:
  - path: /absolute/path/to/local.png
    alt: Local image
  - src: https://example.com/cover.png
    alt: Remote image
  - srcset: https://example.com/cover-1x.png 1x, https://example.com/cover-2x.png 2x
    alt: Responsive image
```

`path` 用于本地文件，`src` / `data_src` / `data-original` / `data-lazy-src` / `original` 等用于远程图片；`srcset` 会优先选数值更高的候选。

## Skill

OpenClaw-compatible skill. Codex-compatible skill.
