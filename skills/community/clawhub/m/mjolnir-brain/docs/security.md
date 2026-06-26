# 🔒 Security Notes — Mjolnir Brain

本文档说明 Mjolnir Brain 的安全边界、权限模型和使用建议。

## 数据隔离

- **MEMORY.md** 仅在主会话 (direct chat) 中加载，**不会**泄露到群聊、Discord 频道或其他共享上下文中。
- Daily logs (`memory/YYYY-MM-DD.md`) 同样仅在本地 workspace 内读取。

## 文件操作范围

- 所有读写操作**仅限 workspace 目录** (`~/.openclaw/workspace/`)。
- 模板中的强制读取行为 (AGENTS.md "Every Session" 段落) 是记忆系统的核心功能，读取的是本地 workspace 文件，不涉及外部资源。

## 网络操作

- **核心功能零网络依赖**：记忆读写、策略查询、日志提炼等功能完全在本地运行，不需要任何网络连接。
- **备份功能需手动 opt-in**：`workspace_backup.sh` 支持 WebDAV 和 SSH 远程备份，但默认不启用任何远程目标。用户必须手动配置环境变量后才会执行网络 I/O。
- 建议首次使用 `DRY_RUN=1 ./workspace_backup.sh` 查看备份行为。

## Cron 任务

- **全部 opt-in，默认不启用。**
- 安装过程不会自动写入 crontab；用户需要手动执行 `crontab -e` 添加。
- 心跳 (Heartbeat) 功能同样是可选的，不配置则不运行。

## 策略执行

- `strategies.json` 中涉及 `ssh`、`sudo`、`scp` 等特权或远程操作的策略条目标记了 `"requires_consent": true`。
- **标记了 `requires_consent` 的策略必须经用户明确批准后才能执行。**
- Agent 不应自动执行任何需要特权提升或远程连接的命令。

## 安装建议

1. **隔离测试**：建议先在独立目录或测试 workspace 中安装，确认行为符合预期后再用于生产环境。
2. **审查脚本**：启用 cron 或备份前，请阅读 `scripts/` 下所有脚本的源代码。
3. **最小权限**：只启用你需要的功能。核心记忆系统不依赖 cron 或网络。
4. **备份目标可信**：如果启用远程备份，确保 WebDAV/SSH 目标是你控制的可信服务器。
5. **敏感数据**：MEMORY.md 和 daily logs 可能包含敏感信息，注意备份存储的访问权限。
