# GInstall OneClick — OpenClaw skill

**One-click installation of GitHub projects** for **Node.js** repositories: produce a setup plan, clone, install dependencies, and run a typical dev workflow — driven by OpenClaw from natural language.

| | |
|---|---|
| **Skill id** | `ginstall-oneclick` |
| **Current version** | `0.1.0` (see [`SKILL.md`](SKILL.md) frontmatter) |
| **Primary artifact** | [`SKILL.md`](SKILL.md) — instructions the agent loads at runtime |

## What users get

- Paste **`owner/repo`**, a full **`github.com`** URL, or a **monorepo tree URL** (`/tree/<branch>/<path>`).
- The agent invokes the **`ginstall`** CLI so the checkout lands in the right subfolder when using monorepos.
- Private repos: operators set **`GITHUB_TOKEN`** (optional for public repos only).

## Requirements on the machine

| Requirement | Purpose |
|---------------|---------|
| [**`ginstall` CLI**](https://github.com/ginstall-oneclick/ginstall-oneclick) | Does clone, installs, scripts (this skill teaches the agent **how** to call it). |
| **Node.js** & **Git** | Declared via `metadata.openclaw.requires.bins`; expected by typical Node/GitHub installs. |

Optional **`GITHUB_TOKEN`**: PAT with at least **`contents:read`** when the target repo is private or unauthenticated GitHub APIs fail — declared in [`SKILL.md`](SKILL.md) as optional `envVars`. Do **not** paste secrets into chat; use env or host secret storage.

## OpenClaw / ClawHub

This folder is meant to bundle as **one skill**: **required file** is **`SKILL.md`** per [OpenClaw skill format](https://docs.openclaw.ai/clawhub/skill-format).  
`homepage` for the upstream CLI lives in **`metadata.openclaw.homepage`** inside [`SKILL.md`](SKILL.md).

---

## 简介（中文）

**GInstall OneClick** 是面向 OpenClaw 的 **Skill**，让 AI 按流程调用 **`ginstall`**，实现 GitHub **Node** 仓库的 **一键安装思路**：生成方案、克隆代码、安装依赖、运行常见开发脚本。支持 **`owner/repo`**、完整 **`github.com` 链接**，以及 **monorepo 的 `/tree/...` 路径**。公有仓可直接用；**私有仓**需在环境中配置 **`GITHUB_TOKEN`**（不要将令牌粘贴到对话里）。技能和机器侧要求均以 **[`SKILL.md`](SKILL.md)** 为准。
