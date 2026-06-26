# OpenClaw 多 Agent TG 群组系统

配置多 Agent Telegram 群组系统，共享 Workspace + MemOS 记忆。

## 架构说明

### Workspace：共享模式

所有 Agent 共享同一个 workspace（`.openclaw/workspace`）。

- 主 Agent 的文件在 workspace 根目录（SOUL.md, AGENTS.md 等）
- 每个子 Agent 的专属文件在 `workspace/agents/{agent_id}/` 子目录
- 共享上下文在 `workspace/shared-context/` — 所有 Agent 都可读取
- 协作通过文件完成：一个 Agent 写文件，另一个 Agent 读文件

### 记忆：MemOS Cloud

- MemOS Cloud 插件已安装并启用，挂载在 OpenClaw 实例级别
- **所有 Agent 自动共享同一个记忆池**
- 不需要创建 memory/ 目录或 YYYY-MM-DD.md 日志文件

### 目录结构

```
workspace/
├── SOUL.md                    # 主 Agent 的灵魂
├── IDENTITY.md                # 主 Agent 身份卡
├── AGENTS.md                  # 主 Agent 行为规则
├── USER.md                    # 用户信息（所有 Agent 共享读取）
├── HEARTBEAT.md               # 主 Agent 心跳任务
├── shared-context/            # 跨 Agent 共享层
│   ├── FEEDBACK-LOG.md        # 通用反馈/修正记录
│   └── SIGNALS.md             # 当前关注的趋势/信号
└── agents/
    ├── {agent_id}/            # 子 Agent 专属目录
    │   ├── SOUL.md            # 子 Agent 灵魂
    │   ├── IDENTITY.md        # 子 Agent 身份卡
    │   └── AGENTS.md          # 子 Agent 行为规则
    └── {另一个agent_id}/
        └── ...
```

## 配置步骤

### 前置要求

1. **BotFather 设置**：每个子 Bot → `/setprivacy` → **Disable**
2. **拉 Bot 进群**：所有 Bot（主 + 子）必须先被添加到目标 TG 群组
3. **获取信息**：
   - TG 群组 ID（负数，如 -1002345678901）
   - 你的 TG 用户 ID
   - 每个子 Bot 的 Token

### 执行配置

运行 `/multiagent setup` 开始配置流程。

## 参考

- 完整指南：https://github.com/bozhouDev/openclaw_agent_create_prompt
