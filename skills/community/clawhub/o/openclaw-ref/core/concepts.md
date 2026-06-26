# 核心概念

## 会话管理

### 会话键映射
- 私信(DM): `agent:<agentId>:<mainKey>` (默认 mainKey=main)
- 群组: `agent:<agentId>:<channel>:group:<id>`
- Telegram话题: `...group:<id>:topic:<threadId>`
- 定时任务: `cron:<job.id>`
- Webhooks: `hook:<uuid>`
- 节点: `node-<nodeId>`

### dmScope 模式
| 模式 | 说明 |
|------|------|
| `main` | 所有私信共享主会话(默认) |
| `per-peer` | 按发送者ID隔离 |
| `per-channel-peer` | 按渠道+发送者隔离 |
| `per-account-channel-peer` | 按账户+渠道+发送者隔离 |

### 身份链接 (跨渠道共享会话)
```json5
session: {
  identityLinks: {
    alice: ["telegram:123456789", "discord:987654321"]
  }
}
```

### 会话重置
- 默认: 每日凌晨4:00(网关主机本地时间)
- 可选: `idleMinutes` 滑动窗口，先过期者生效
- 触发器: `/new` `/reset` (可通过 `resetTriggers` 自定义)
- `/new <model>` 重置并切换模型

### 按类型/渠道覆盖
```json5
session: {
  reset: { mode: "daily", atHour: 4, idleMinutes: 120 },
  resetByType: {
    dm: { mode: "idle", idleMinutes: 240 },
    group: { mode: "idle", idleMinutes: 120 },
    thread: { mode: "daily", atHour: 4 }
  },
  resetByChannel: {
    discord: { mode: "idle", idleMinutes: 10080 }
  }
}
```

### 发送策略
```json5
session: {
  sendPolicy: {
    rules: [
      { action: "deny", match: { channel: "discord", chatType: "group" } },
      { action: "deny", match: { keyPrefix: "cron:" } }
    ],
    default: "allow"
  }
}
```
运行时: `/send on|off|inherit`

### 存储位置
- 会话状态: `~/.openclaw/agents/<agentId>/sessions/sessions.json`
- 对话记录: `~/.openclaw/agents/<agentId>/sessions/<SessionId>.jsonl`

## 压缩 (Compaction)

### 工作原理
会话接近上下文窗口时，自动将旧消息总结为摘要，保留近期消息。摘要持久化到JSONL。

### 配置
```json5
compaction: {
  mode: "default",           // default|safeguard
  reserveTokensFloor: 20000, // 最小预留token
  memoryFlush: {
    enabled: true,            // 压缩前记忆刷新
    softThresholdTokens: 4000 // 触发阈值
  }
}
```

### 手动压缩
```
/compact Focus on decisions and open questions
```

### 压缩 vs 修剪
- 压缩: 总结+持久化到JSONL
- 修剪(contextPruning): 仅裁剪旧工具结果，内存中按请求进行，不写JSONL

## 记忆系统

### 文件布局
- `memory/YYYY-MM-DD.md` — 每日日志(仅追加)
- `MEMORY.md` — 长期记忆(仅主会话加载)

### 记忆刷新 (压缩前)
会话接近压缩时自动触发静默回合，提醒模型写入持久记忆。

### 向量记忆搜索
- 默认启用，语义搜索 MEMORY.md + memory/*.md
- 嵌入提供商自动选择: local → openai → gemini
- 索引存储: `~/.openclaw/memory/<agentId>.sqlite`

### 混合搜索 (BM25 + 向量)
```json5
memorySearch: {
  query: {
    hybrid: {
      enabled: true,
      vectorWeight: 0.7,
      textWeight: 0.3
    }
  }
}
```

### 额外记忆路径
```json5
memorySearch: {
  extraPaths: ["../team-docs", "/srv/shared-notes/overview.md"]
}
```

### 会话记忆搜索 (实验性)
```json5
memorySearch: {
  experimental: { sessionMemory: true },
  sources: ["memory", "sessions"]
}
```

## 上下文修剪 (Context Pruning)

裁剪旧工具结果以释放上下文空间，不影响JSONL历史。

```json5
contextPruning: {
  mode: "adaptive",          // off|adaptive|aggressive
  keepLastAssistants: 3,     // 保护最近N条
  softTrimRatio: 0.3,        // 软裁剪触发比率
  hardClearRatio: 0.5,       // 硬清除触发比率
  minPrunableToolChars: 50000,
  softTrim: { maxChars: 4000, head: 1500, tail: 1500 },
  hardClear: { enabled: true },
  tools: { deny: ["memory_search"] }  // 跳过裁剪的工具
}
```

## 多Agent系统

### 智能体列表
```bash
openclaw agents list
openclaw agents add myagent --workspace ~/myproject --model openai/gpt-5.2
openclaw agents delete myagent
```

### 每个智能体可覆盖
- model (主力模型)
- workspace (工作区)
- 渠道绑定 (--bind telegram:bot1)

### 子智能体
- `sessions_spawn` 创建隔离子智能体
- `subagents list|steer|kill` 管理子智能体
- 子智能体完成后自动通知父会话

## 流式传输

### 分块流式 (Block Streaming)
```json5
blockStreamingDefault: "on",
blockStreamingBreak: "text_end",
blockStreamingChunk: { min: 800, max: 1200 },
blockStreamingCoalesce: { idleMs: 1000 }
```

### 人类延迟
```json5
humanDelay: {
  mode: "linear",  // off|linear|random
  baseMs: 500,
  perCharMs: 10,
  maxMs: 3000
}
```

## 输入指示器
```json5
typingMode: "instant",        // instant|streaming|off
typingIntervalSeconds: 6      // 刷新频率
```

## 检查命令
- `openclaw status` — 会话状态+诊断
- `openclaw sessions --json` — 导出会话
- `/status` — 聊天内快速诊断
- `/context list` — 查看系统提示内容
- `/context detail` — 详细上下文贡献者
- `/stop` — 中止当前运行+子智能体
- `/compact` — 手动压缩

## 多智能体路由

### 概念
- `agentId`: 独立大脑(工作区+认证+会话)
- `accountId`: 渠道账户实例
- `binding`: 入站消息路由规则 (channel, accountId, peer) → agentId

### 路由优先级 (最具体优先)
1. `peer` 匹配(精确私信/群组/频道ID)
2. `guildId` (Discord)
3. `teamId` (Slack)
4. `accountId` 匹配
5. 渠道级匹配
6. 默认智能体

### CLI
```bash
openclaw agents list [--bindings]
openclaw agents add <id> [--workspace <dir>] [--model <id>] [--bind channel[:accountId]]
openclaw agents delete <id> [--force]
```

### 配置示例
```json5
{
  agents: {
    list: [
      { id: "home", default: true, workspace: "~/.openclaw/workspace-home" },
      { id: "work", workspace: "~/.openclaw/workspace-work", model: "anthropic/claude-opus-4-5" }
    ]
  },
  bindings: [
    { agentId: "work", match: { channel: "whatsapp", peer: { kind: "dm", id: "+155..." } } },
    { agentId: "home", match: { channel: "whatsapp" } },
    { agentId: "work", match: { channel: "telegram" } }
  ]
}
```

### 每智能体覆盖
- `model`: 主力模型
- `workspace`: 工作区路径
- `agentDir`: 状态目录
- `sandbox`: 沙箱配置
- `tools`: 工具策略(allow/deny)
- `heartbeat`: 心跳配置
- `groupChat.mentionPatterns`: 提及模式

### 认证隔离
每个智能体独立认证: `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`
主智能体凭证不自动共享。

## 系统提示词

### 组装结构
1. Tooling — 工具列表+描述
2. Safety — 防护提醒
3. Skills — 可用Skills列表(按需加载)
4. OpenClaw Self-Update — config/update说明
5. Workspace — 工作目录
6. Documentation — 文档路径
7. Workspace Files — 引导文件注入
8. Sandbox — 沙箱信息(启用时)
9. Current Date & Time — 时区
10. Reply Tags — 回复标签语法
11. Heartbeats — 心跳提示
12. Runtime — 主机/OS/模型/思考级别

### 引导文件注入
注入到 Project Context: AGENTS.md, SOUL.md, TOOLS.md, IDENTITY.md, USER.md, HEARTBEAT.md, BOOTSTRAP.md
截断上限: `agents.defaults.bootstrapMaxChars` (默认20000)

### 提示模式
| 模式 | 用途 | 包含 |
|------|------|------|
| `full` | 默认 | 所有部分 |
| `minimal` | 子智能体 | 省略Skills/Memory/Self-Update/Reply Tags/Heartbeats |
| `none` | 基本 | 仅身份行 |

### 检查上下文
```
/context list    # 查看注入文件贡献
/context detail  # 详细上下文
```

## 命令队列
- 入站消息按会话键序列化
- 并发受 `agents.defaults.maxConcurrent` 限制(默认1)
- 队列满时新消息等待
- `/stop` 中止当前运行

## 重试策略
出站提供商调用失败时指数退避重试:
```json5
retry: { attempts: 3, minDelayMs: 1000, maxDelayMs: 30000, jitter: true }
```
适用于: 模型API调用、渠道API调用(Telegram/Discord等)

## OAuth 认证

### 存储位置
- 认证配置文件: `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`
- 运行时缓存: `~/.openclaw/agents/<agentId>/agent/auth.json` (自动管理)
- 旧版: `~/.openclaw/credentials/oauth.json` (首次使用时自动导入)

### 令牌汇聚
同一提供商的多个OAuth登录可能互相失效。OpenClaw用auth-profiles.json作为统一存储。

### Anthropic setup-token
```bash
claude setup-token                                    # 任意机器生成
openclaw models auth setup-token --provider anthropic # 网关主机粘贴
openclaw models auth paste-token --provider anthropic # 远程粘贴
```

### OpenAI Codex OAuth
```bash
openclaw onboard --auth-choice openai-codex
# 或
openclaw models auth login --provider openai-codex
```

### 多配置文件路由
```bash
openclaw models auth order set --provider anthropic profile1 profile2
/model anthropic/claude-opus-4-5@profile2  # 手动固定
```

### 常见问题
- "OAuth token refresh failed": 重新运行 setup-token
- 认证按智能体独立，新智能体需单独设置
- 冷却: 指数退避 1min→5min→25min→1h

## 上下文管理

### 上下文组成
1. 系统提示词 (OpenClaw构建)
2. 对话历史 (消息+助手回复)
3. 工具调用/结果 + 附件

### 检查命令
```
/status          # 窗口使用率
/context list    # 注入文件+大小
/context detail  # 详细分解(每个文件/工具schema/Skills)
/usage tokens    # 每次回复的token使用量
/compact [focus] # 手动压缩释放空间
```

### 上下文窗口
- `agents.defaults.contextTokens`: 上下文token上限(默认200000)
- 接近上限时自动触发压缩
- 工具结果可通过contextPruning裁剪

### 减少上下文消耗
1. 保持HEARTBEAT.md小巧
2. 使用contextPruning裁剪旧工具结果
3. 定期/compact压缩
4. 大文件用bootstrapMaxChars截断
