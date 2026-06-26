## Skill Generator（OpenClaw）

一个 OpenClaw skill：当你在对话中明确说“我想生成一个 skill / 帮我创建一个 skill ……”时，它会作为交互式向导，帮你把想法整理成一个可部署的 OpenClaw skill 文件夹（包含必需的 `SKILL.md`，以及可选的辅助脚本）。

### Features

- Interactive, phase-based wizard (Phase 0–7): collect requirements → generate draft → deploy → test & fix
- Draft + deploy workflow to avoid transient paths (`.drafts/<skill-name>` → `<skill-name>`)
- Cross-platform helper scripts (Node.js) for writing files, listing files, deploying, and backup
- Safety guardrails: rejects routed/system messages; restricts writes to the `.openclaw` boundary

---

## 快速开始（安装）

把本仓库作为一个目录放进你的 OpenClaw skills 目录即可。

常见 skills 目录位置：

- Windows: `C:\Users\<你的用户名>\.openclaw\skills`
- macOS/Linux: `~/.openclaw/skills`

安装方式（任选其一）：

1) 直接复制文件夹

- 复制整个 `openclaw-skill-generator` 目录到你的 skills 目录下，并确保目录名为 `skill-generator`

2) Git clone（推荐）

```bash
git clone https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPO>.git
```

然后把仓库目录移动/链接到：

- `~/.openclaw/skills/skill-generator`（macOS/Linux）
- `C:\Users\<你>\.openclaw\skills\skill-generator`（Windows）

---

## 使用方式

在一个新的 OpenClaw 对话中，明确发起“创建 skill”的请求，例如：

- 我想生成一个skill
- 帮我创建一个skill
- 新建一个skill，用来……
- I want to build a skill that…

之后按向导提问逐步补齐信息即可。向导的核心节奏写在 [SKILL.md](./SKILL.md) 中。

---

## 工作原理（Phase 0–7）

- Phase 0：确认环境能力（自动模式 / 手动模式）
- Phase 1–2：采集并验证需求（最多追问 3 轮，不足则征求“默认兜底”）
- Phase 3：解析 OpenClaw `skillsPath`，并确定草稿/目标目录
- Phase 4：在草稿目录生成 `SKILL.md` 与可选脚本
- Phase 5：部署安装到目标 skill 目录（可处理同名冲突、替换安装）
- Phase 6：在真实 OpenClaw 路由入口中测试与修复（修复前强制备份）
- Phase 7：交付最终路径与文件清单

---

## 仓库结构

- [SKILL.md](./SKILL.md)：skill 的主逻辑与交互协议（向导本体）
- [scripts/](./scripts)：
  - `find_openclaw_path.js`：定位/创建 `.openclaw/skills` 并输出 `skillsPath`
  - `write_file.js`：写文件（限制在 `.openclaw` 边界内）
  - `write_skill.js`：把草稿 skill 部署到目标目录（含 replace / rollback / cleanup）
  - `list_files.js`：递归列目录文件清单（JSON）
  - `backup_skill.js`：备份一个已安装的 skill 目录
- [references/](./references)：设计与排错资料目录；其中 `tool-setup-guide.md` 会在执行阶段用于处理工具/环境/依赖故障，其余文档默认供人工参考

---

## Requirements

- OpenClaw installed and working
- Node.js available on PATH (`node --version`)

如果环境无法自动写文件或无法运行 Node.js，这个 skill 会切换到“手动模式”，由你在本机执行文件保存与命令。

---

## License

MIT License. See [LICENSE](./LICENSE).

---

## English

### What is this?

An OpenClaw skill that acts as an interactive wizard for creating a brand-new OpenClaw skill folder (required `SKILL.md` + optional helper scripts). It should trigger only when a human explicitly asks to create a new skill in the conversation.

### Install

Copy/clone this folder into your OpenClaw skills directory:

- Windows: `C:\Users\<you>\.openclaw\skills\skill-generator`
- macOS/Linux: `~/.openclaw/skills/skill-generator`

### Use

In a new OpenClaw chat, say something like:

- "I want to build a skill…"
- "Create a skill for…"

Then follow the wizard prompts.

### License

MIT License. See [LICENSE](./LICENSE).
