# Agent instruction file compatibility

不同工具读取不同入口文件，但项目事实应尽量只有一份来源。

| Tool family | Conventional file | Recommended handling |
| --- | --- | --- |
| OpenAI/Codex | `AGENTS.md` | Put shared repository rules here. |
| Claude Code | `CLAUDE.md` | Use a compatible pointer or synchronized thin wrapper. |
| Gemini CLI | `GEMINI.md` | Add only when the project uses Gemini. |
| GitHub Copilot | `.github/copilot-instructions.md` | Add only repository-specific Copilot guidance. |

When `AGENTS.md` and `CLAUDE.md` both exist, read both. Do not assume one tool reads the other automatically. Prefer a short compatibility file:

```markdown
# Claude project instructions

Read and follow `AGENTS.md` first. Shared project memory lives in `docs/`.
Do not duplicate or contradict the rules in `AGENTS.md`.
```

If no instruction file exists, create `AGENTS.md` by default. Create `CLAUDE.md` too only when the user requests Claude compatibility or the repository clearly targets Claude Code. Keep tool-specific differences limited to discovery and invocation; put shared engineering rules in project documentation.
