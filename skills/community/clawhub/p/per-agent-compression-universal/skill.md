# Per-Agent Memory Compression Skill (Universal)

## Purpose | 目的

This skill automates weekly memory consolidation for every agent in your OpenClaw system. It discovers all agents with workspaces and creates a dedicated cron task for each, ensuring that each agent maintains its own long-term memory (USER.md, IDENTITY.md, SOUL.md, MEMORY.md) with extracted preferences, decisions, and personal information.

本技能为 OpenClaw 系统中的每个代理自动化每周记忆整合。它发现所有带有工作区的代理，并为每个创建专用的 cron 任务，确保每个代理维护自己的长期记忆（USER.md、IDENTITY.md、SOUL.md、MEMORY.md），包含提取的偏好、决策和个人信息。

## Features | 特性

- Zero-config auto-discovery | 零配置自动发现
- Per-agent workspace isolation | 每个代理工作区隔离
- State persistence & checkpoint | 状态持久化与断点
- Deduplication | 去重
- Domain-aware extraction | 领域感知提取
- Moved-file marking | 移动文件标记
- DingTalk summary notifications | 钉钉摘要通知

## Installation | 安装

```bash
cd /root/.openclaw/workspace
chmod +x skills/per-agent-compression-universal/install.sh
./skills/per-agent-compression-universal/install.sh
```

## How It Works | 工作原理

1. **Discovery**: Runs `openclaw agents list --json` to find all agents with a `workspace`.
2. **Task Creation**: For each agent, creates a cron task named `per_agent_compression_<agent_id>` with schedule staggered from Sunday 03:00 Shanghai.
3. **Execution**: When triggered, the `main` agent executes the consolidation logic:
   - Reads daily notes older than 7 days from `{workspace}/memory/`
   - Extracts user preferences, key decisions, personal info (domain-specific)
   - Appends to `USER.md`, `IDENTITY.md`, `SOUL.md`, `MEMORY.md` with date headers
   - Moves processed notes to `{workspace}/memory/processed/`
   - Updates `{workspace}/memory/.compression_state.json` for checkpoint
   - Sends summary to DingTalk

## Configuration | 配置

No configuration needed. To customize schedule or domain context, edit `install.sh` before running.

## Uninstall | 卸载

```bash
./skills/per-agent-compression-universal/uninstall.sh
```

## Notes | 注意

- This skill is in active testing; see CHANGELOG.md for known issues.
- The task messages are concise due to CLI length limits; full details are in README.
- If you need to edit a task's message manually: `openclaw cron edit per_agent_compression_<agent_id> --message "..."`

## Support | 支持

- Changelog: CHANGELOG.md
- Issues: Report via GitHub or ClawHub
