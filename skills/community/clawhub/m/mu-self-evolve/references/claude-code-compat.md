# Claude Code 环境兼容说明

> 本 Skill 默认运行在 OpenClaw 环境。Claude Code 自动降级兼容。
> 所有 Python 脚本（`scripts/` 目录下）内置环境自动检测（`env_detect.py`），无需手动指定路径。

## 路径映射

| 用途 | OpenClaw（主） | Claude Code（降级） |
|------|---------------|-------------------|
| 工作区 | `<AGENT_HOME>/workspace/` | `~/.claude/` |
| 每日日记 | `<AGENT_HOME>/workspace/memory/YYYY-MM-DD.md` | `~/.claude/memory/daily/YYYY-MM-DD.md` |
| 经验记录 | `<AGENT_HOME>/workspace/.learnings/LEARNINGS.md` | `~/.claude/memory/.learnings/LEARNINGS.md` |
| 周度叙事 | `<AGENT_HOME>/workspace/memory/narratives/` | `~/.claude/memory/narratives/` |
| 归档 | `<AGENT_HOME>/workspace/memory/archive/` | `~/.claude/memory/archive/` |

## 调度命令映射

| 环境 | 查看任务 | 创建任务 |
|------|---------|---------|
| OpenClaw | `openclaw cron list` | `openclaw cron add ...` |
| Claude Code | 系统 crontab | 手动触发或 crontab |

### Claude Code 调度方案

Claude Code 没有内置的自动化 CLI，以下两种方案任选其一：

**方案 A：系统 crontab（推荐）**
```bash
# 每天19:30自动执行（需要 Claude Code CLI 支持 --prompt 参数）
crontab -e
# 添加：
30 19 * * * cd ~/.claude && claude --prompt "执行每日自我进化流程（见 mu-self-evolve SKILL.md）。今天是周几？如果是周五，额外执行【第六步：周度反思】。"
```

**方案 B：手动触发**
在 Claude Code 会话中直接说："执行每日自我进化"或"跑一下 mu-self-evolve"

## 首次初始化（含环境检测）

```bash
# 环境检测
if [ -d "$HOME/.openclaw/workspace" ]; then
  WS="$HOME/.openclaw/workspace"
  LEARNINGS_DIR="$WS/.learnings"
  NARRATIVES_DIR="$WS/memory/narratives"
  ARCHIVE_DIR="$WS/memory/archive"
elif [ -d "$HOME/.claude" ]; then
  WS="$HOME/.claude/memory"
  LEARNINGS_DIR="$WS/.learnings"
  NARRATIVES_DIR="$WS/narratives"
  ARCHIVE_DIR="$WS/archive"
else
  WS="$HOME/.openclaw/workspace"
  LEARNINGS_DIR="$WS/.learnings"
  NARRATIVES_DIR="$WS/memory/narratives"
  ARCHIVE_DIR="$WS/memory/archive"
fi

# 创建目录
mkdir -p "$LEARNINGS_DIR/archive" "$NARRATIVES_DIR" "$ARCHIVE_DIR"

# 初始化空文件
for f in LEARNINGS.md ERRORS.md FEATURE_REQUESTS.md; do
  [ ! -f "$LEARNINGS_DIR/$f" ] && echo "# ${f%.md} Log" > "$LEARNINGS_DIR/$f"
done

echo "✅ 初始化完成 | WS=$WS"
```

## Claude Code 注意事项

1. Claude Code 的日记文件在 `~/.claude/memory/daily/`（多了一层 `daily/` 子目录），手动 grep 等命令需注意路径差异
2. 脚本通过 `scripts/env_detect.py` 自动适配路径，正常情况下无需手动指定
3. Claude Code 环境下如果没有 SOUL.md/TOOLS.md/AGENTS.md 文件，提升目标统一写入 MEMORY.md
4. Claude Code 的记忆文件为 `CLAUDE.md`，可作为 MEMORY.md 的别名（首次初始化时自动创建 MEMORY.md 并在 CLAUDE.md 中引用）
