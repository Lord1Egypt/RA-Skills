# Knowledge to ClawHub Skill Publisher

This skill helps turn a solved workflow into canonical knowledge docs and a self-contained skill bundle that can be published to ClawHub.
这个 skill 用来把一个已验证流程整理成规范知识文档，并打包成可发布到 ClawHub 的自包含 skill。

## What This Skill Is For | 适用场景

Use it when:
适用于：

- a troubleshooting or operations flow has already been proven
- you want to preserve the flow in `knowledge/`
- you want agents to reuse the same flow via a skill
- you want to publish that skill to ClawHub

## What It Produces | 产出物

The skill aims to produce:
这个 skill 目标产出：

- canonical Markdown docs
- a self-contained skill folder
- a changelog-backed release
- an optionally installed local copy under `~/.openclaw/skills/`

## Included Files | 包含文件

- `SKILL.md`
- `README.md`
- `WORKFLOW.md`
- `FAQ.md`
- `CHANGELOG.md`

## Local Use | 本地使用

Place this folder under one of these locations:
把这个目录放到以下任一位置：

- `<workspace>/skills/`
- `~/.openclaw/skills/`

Then start a new OpenClaw session or refresh skills.
然后重新开始一个 OpenClaw 会话，或刷新 skills。

## ClawHub Publish Shape | ClawHub 发布方式

This folder is self-contained so it can be published to ClawHub as a single bundle.
这个目录是自包含的，可以直接作为一个 skill 包发布到 ClawHub。

Example publish command:
发布示例命令：

```bash
clawhub publish ./skills/shared/knowledge-to-clawhub-skill-publisher \
  --slug knowledge-to-clawhub-skill-publisher \
  --name "Knowledge to ClawHub Skill Publisher" \
  --version 1.0.0 \
  --tags latest,workflow,knowledge,skill,clawhub
```
