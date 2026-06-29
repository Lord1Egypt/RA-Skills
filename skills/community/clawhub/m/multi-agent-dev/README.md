# multi-agent-dev

> OpenClaw + Ralph Loop 多智能体协作开发工作流

**底部执行器可切换**：默认 OpenCode，支持 Claude Code / Codex / Copilot / Cursor Agent / Qwen Code。

## 安装

```bash
openclaw skills install multi-agent-dev
# 或
clawhub install hehe973781230/multi-agent-dev
```

## 功能

- **任务分类路由**：简单任务 → OpenClaw 直接执行；中等任务 → sessions_spawn；复杂迭代任务 → Ralph Loop
- **执行器可切换**：统一通过 `ACTIVE_AGENT` 配置，Ralph 命令格式不变
- **自主迭代收敛**：Ralph Loop 持续循环直到输出 `<promise>COMPLETE</promise>` 或达上限
- **协作记忆**：任务上下文持久化，agent 间共享

## 快速开始

### Ralph Loop（迭代任务）

```bash
cd ~/GitHub/my-project
ralph "优化 SKILL.md，增加 xxx 章节。完成后输出 <promise>COMPLETE</promise>。"
  --agent opencode
  --model minimax/MiniMax-M2.7
  --max-iterations 5
  --no-plugins
```

### 切换执行器

修改 SKILL.md 顶部的配置区：

```yaml
ACTIVE_AGENT: claude-code   # 改成 claude-code / codex / copilot / cursor-agent / qwen-code
AGENT_MODEL: claude-sonnet-4
```

所有 `ralph` 命令格式不变，自动使用新执行器。

## 执行器选择参考

| 执行器 | 优势 | 推荐场景 |
|--------|------|---------|
| opencode | MiniMax/M3 支持好，默认 | 日常开发、Skill 改写 |
| claude-code | Claude 4 系列强 | 复杂推理、代码审查 |
| codex | GPT-5 支持 | OpenAI 相关项目 |
| copilot | GitHub 深度集成 | GitHub 项目维护 |
| cursor-agent | 上下文感知强 | Cursor 用户 |
| qwen-code | Qwen 系列强 | 阿里云/Qwen 项目 |

## 前置要求

- [Ralph Wiggum](https://github.com/Th0rgal/open-ralph-wiggum)（`npm install -g @th0rgal/ralph-wiggum`）
- 至少一种 AI 编码 CLI：opencode / claude / codex / copilot / cursor-agent / qwen

详见 [SKILL.md](./SKILL.md)

---

## Changelog

see [CHANGELOG.md](./CHANGELOG.md)
