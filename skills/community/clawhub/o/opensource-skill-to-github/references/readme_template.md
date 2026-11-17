# README.md 模板

`scripts/scaffold.sh` 会生成此模板的实例化版（作者/handle 从 `OSG_AUTHOR_NAME` / `OSG_GITHUB_HANDLE` 环境变量或 git config 取，不写死）。模板原文如下，供手工调整参考。

## 模板正文（占位用 `<your-name>` / `<your-github-handle>`）

```markdown
# <slug>

> One-line description here (从 SKILL.md 抄过来即可)

## Features

- Feature 1
- Feature 2
- Feature 3

## Quick Start

\`\`\`bash
# Install (clawhub)
clawhub install <slug>

# Or clone directly
git clone https://github.com/<your-github-handle>/<slug>.git
\`\`\`

## Usage

详细使用方法见 [SKILL.md](./SKILL.md)。

## Install in your AI agent

| Agent | Install |
|---|---|
| OpenClaw | `clawhub install <slug>` |
| Claude Code | Manual: copy to `~/.claude/skills/` |
| Cursor | Manual: copy to `.cursor/skills/` |

## License

MIT (see [LICENSE](./LICENSE))

## Author

<your-name> · [github.com/<your-github-handle>](https://github.com/<your-github-handle>)

## Changelog

### v1.0.0 (YYYY-MM-DD)

- Initial release
```

## 关于 Part of <suite> 章节

如果这个 skill 是某个 suite repo 的一员（如 build-better-skills 套件），README 末尾还要加：

```markdown
## Part of build-better-skills

This skill is part of the [build-better-skills](https://github.com/<handle>/build-better-skills) suite:

| Stage | Skill | Status |
|---|---|---|
| Creation | `skill-creator` | 🚧 Not yet released |
| **Audit** | **`glic-check`** | ✅ **v1.0.1** |
| Release | `skill-release` | 🚧 Not yet released |
| Testing | `skill-regression` | 🚧 Not yet released |
| Sediment | `skill-sediment` | 🚧 Not yet released |

(🚧 占位也要列，避免用户读 README 以为某成员 ready，装了报 not found)
```

## 关键原则

- **README 模板写得再漂亮，clawhub 卡片只解析 SKILL.md 顶部 4 行**（Version/License/Author/Repository）
- 不要在 README 里塞内部决策记录、变更原因、agent 沉淀经验——那些放 memory
- Quick Start 必须 1 个命令能跑通，3+ 命令的安装流程要拆步骤
