# Human-Like Memory Plugin for OpenClaw

[![npm version](https://img.shields.io/npm/v/@humanlikememory/human-like-mem.svg)](https://www.npmjs.com/package/@humanlikememory/human-like-mem)

OpenClaw 长期记忆插件。让你的 Agent 能够记住过去的对话、用户偏好和重要上下文。

**功能特性：**
- 自动记忆召回（每次回答前）
- 自动对话存储（每次回答后）
- Agent 可调用的工具：`memory_search` 和 `memory_store`
- 注册为一等记忆引擎（`kind: "memory"`）
- 运行时只读取 OpenClaw plugin config，不读取环境变量或 secrets 文件
- 默认启用隐私优先模式：不发送平台用户 ID，除非显式开启
- 需要 OpenClaw >= 2026.2.0

## 快速开始

### 1. 安装

```bash
openclaw plugins install @humanlikememory/human-like-mem
```

### 2. 获取 API Key

访问 [https://plugin.human-like.me](https://plugin.human-like.me) 获取你的 API Key（以 `mp_` 开头）。

### 3. 配置

```bash
# 设置 API Key（必填）
openclaw config set plugins.entries.human-like-mem.config.apiKey "mp_你的key"

# 设为默认记忆引擎
openclaw config set plugins.slots.memory human-like-mem

# 启用 Agent 记忆搜索
openclaw config set agents.defaults.memorySearch '{"enabled":true}' --strict-json
```

### 4. 重启

```bash
openclaw restart
```

### 5. 验证

```bash
openclaw status
```

你应该看到：

```
Memory │ 0 files · 0 chunks · sources remote-api · plugin human-like-mem · vector ready
```

## 配置项

所有选项通过 `openclaw config set plugins.entries.human-like-mem.config.<key> <value>` 设置：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `apiKey` | string | **（必填）** | 你的 API Key，从 https://plugin.human-like.me 获取 |
| `baseUrl` | string | `https://plugin.human-like.me` | API 地址 |
| `userId` | string | `openclaw-user` | 用户标识 |
| `agentId` | string | `main` | 用于记忆范围隔离的 Agent 标识 |
| `scenario` | string | `openclaw-plugin` | 写入和检索共同使用的场景名 |
| `recallEnabled` | boolean | `true` | 启用自动记忆召回 |
| `addEnabled` | boolean | `true` | 启用自动记忆存储 |
| `recallGlobal` | boolean | `true` | 全局搜索记忆（不限当前对话） |
| `memoryLimitNumber` | number | `6` | 每轮最多召回记忆条数 |
| `minScore` | number | `0.1` | 最低相关性分数 (0-1) |
| `minTurnsToStore` | number | `5` | 对话满 N 轮后存储 |
| `sessionTimeoutMs` | number | `300000` | 自动刷新超时（毫秒） |
| `stripPlatformMetadata` | boolean | `true` | 默认不发送飞书/Discord 平台用户 ID，除非显式关闭 |

**示例 — 完整配置：**

```bash
openclaw config set plugins.entries.human-like-mem.config '{"apiKey":"mp_xxx","recallEnabled":true,"addEnabled":true,"memoryLimitNumber":8}' --strict-json
```

## 重要：多个 AI Agent 共享记忆时

**如果你希望多个 AI agent 共享同一批记忆，必须显式对齐 `agentId` 和 `scenario`。**

这两个字段决定了记忆的作用域：

- `agentId` 决定这批记忆属于哪个 agent
- `scenario` 决定写入和检索所使用的客户端 / 工作流命名空间

OpenClaw 侧默认兼容的值是：

```bash
openclaw config set plugins.entries.human-like-mem.config.agentId "main"
openclaw config set plugins.entries.human-like-mem.config.scenario "openclaw-plugin"
```

如果另一端客户端用的是别的值，这里也要保持完全一致。比如另一端写入时使用的是 `agentId=default`、`scenario=claude`：

```bash
openclaw config set plugins.entries.human-like-mem.config.agentId "default"
openclaw config set plugins.entries.human-like-mem.config.scenario "claude"
openclaw restart
```

如果这两个字段没有对齐，就可能出现“写入成功了，但跨 agent 检索不到同一批记忆”的情况。

## Agent 工具

安装后，Agent 可以主动使用记忆：

- **`memory_search`** — 搜索过去的对话和存储的知识
- **`memory_store`** — 主动保存重要信息供将来召回

这些工具会自动注册，Agent 开箱即用。

## 工作机制

1. **回答前**（`before_prompt_build`）：插件根据当前 prompt 搜索相关记忆并注入上下文
2. **回答后**（`agent_end`）：插件缓存对话轮次，满足轮次阈值或超时后写入长期存储
3. **会话结束时**：刷新所有缓存的对话

## 常见问题

- **"API key not configured"** — 执行：`openclaw config set plugins.entries.human-like-mem.config.apiKey "mp_xxx"`
- **status 显示 "unavailable"** — 确认 `plugins.slots.memory` 设为 `human-like-mem`
- **请求超时** — 调大 config 中的 `timeoutMs`
- **查看日志：**

```bash
openclaw logs | grep "Memory Plugin"
```

## 升级说明

`1.0.0` 延续并稳定了 `v0.4.x` 引入的自动记忆架构：

- 插件类型为 `memory`
- 自动召回运行在 `before_prompt_build`
- 自动存储运行在 `agent_end` 和 `session_end`
- 默认注册 Agent 工具 `memory_search` 和 `memory_store`

升级后请确认 memory slot 已设置：

```bash
openclaw config set plugins.slots.memory human-like-mem
openclaw restart
```

## 许可证

Apache-2.0
