# 专业模式 — 完整技术数据面板

> 专业模式包含系统全部运行指标、详细配置参数、API 状态与安全策略。
> 适合技术人员深度排查和开发者参考。

## 系统核心指标

| 参数 | 值 | 说明 |
|------|-----|------|
| Agent ID | main | 当前 Agent |
| 运行时 | direct | 直接模式 |
| Shell | PowerShell | Windows 环境 |
| Node.js | v22.x | Node 版本 |
| OpenClaw 版本 | 2026.3.x | 主版本号 |
| Build | 61d171a | Git commit |
| 架构 | x64 | CPU 架构 |

## 会话配置参数

| 参数 | 值 | 说明 |
|------|-----|------|
| 超时 | 72000s | 单次会话超时 |
| 最大并发 | 3 | 同时最多3个会话 |
| 子智能体上限 | 8 | subagent 并发上限 |
| 会话重置 | idle (关闭) | 从不自动重置 |
| 保留期限 | 365天 | 日志保留时间 |
| 日志轮转 | 1GB | 单文件大小上限 |
| 最大条目 | 1,000,000 | 单会话消息上限 |

## 模型与 Token 消耗

| 参数 | 值 | 说明 |
|------|-----|------|
| 模型 | qclaw/modelroute | 当前模型 |
| Provider | qclaw · OpenAI兼容 | API 兼容模式 |
| Base URL | 127.0.0.1:19000 | 本地代理 |
| 上下文窗口 | 200,000 tokens | 最大上下文 |
| 上下文压力 | 上下文使用 / 200k | 建议 >70% 预警 |
| 最大输出 | 8192 tokens | 单次最大输出 |

### 上下文压力判定

| 压力区间 | 状态 | 建议 |
|---------|------|------|
| < 50% | 绿色 | 正常 |
| 50-70% | 黄色 | 注意，可考虑重置 |
| 70-90% | 橙色 | 建议重置会话 |
| > 90% | 红色 | 必须重置 |

## Gateway 配置

| 参数 | 值 | 说明 |
|------|-----|------|
| 端口 | 28789 | Gateway 监听端口 |
| 绑定模式 | loopback | 仅本机访问 🔒 |
| 认证方式 | token | Bearer token 鉴权 |
| 运行模式 | local | 本地模式 |
| WebSocket | ws://127.0.0.1:28789 | 实时双向通信 |
| REST API | http://127.0.0.1:28789/api | HTTP 接口 |
| Tailscale | off | 未启用 |
| Control UI | 已启用 | Web UI 可用 |

## 定时任务 Cron Jobs 详情

### Job ID 详细信息（以 ltc-daily 为例）

| 参数 | 值 |
|------|-----|
| Job ID | a1aa8721-24b6-472f-bb1b-353c708c733d |
| Session Target | isolated（独立会话） |
| Payload Model | qclaw/modelroute |
| Timeout | 300s（5分钟） |
| Delivery | announce → webchat |
| Last Run | ok · 66,347ms |
| Last Delivered | not-delivered |
| Consecutive Errors | 0（正常） |

### Cron 表达式参考

| 任务 | 表达式 | 说明 |
|------|--------|------|
| 每天 08:00 | `0 8 * * *` | 每日定时 |
| 每周五 14:00 | `0 14 * * 5` | 每周五 |
| 每月1日 09:00 | `0 9 1 * *` | 每月首日 |

## 会话管理 Session 详情

| 参数 | 说明 |
|------|------|
| Session Key | 唯一标识符 |
| Model | 使用的模型 |
| Channel | 来源通道（webchat/signal等） |
| Context Limit | 上下文上限（通常 200k） |
| Total Tokens Used | 累计消耗 token |
| Last Active | 最后活跃时间 |
| Transcript Path | 完整会话记录路径（.jsonl） |

## 插件表格 Plugins

| 插件 | 类型 | 状态 | 说明 |
|------|------|------|------|
| wechat-access | 渠道 | 已启用 | 企业微信接入 |
| content-plugin | 内容 | 已启用 | 内容处理 |
| tool-sandbox | 沙箱 | 已禁用 | 工具执行隔离 |
| qmemory | 记忆 | 已启用 | 记忆增强 |
| pcmgr-ai-security | 安全 | 已启用 | AI 安全监控 |

## 安全配置 Safety Config

| 安全项 | 默认值 | 当前 | 说明 |
|--------|--------|------|------|
| READONLY_MODE | true | true | 禁止修改系统配置 |
| LOCAL_TOKEN_AUTH_REQUIRED | true | true | 需要 Authorization Bearer token |
| APPROVAL_ACTIONS_ENABLED | false | false | 高风险操作需审批 |
| APPROVAL_ACTIONS_DRY_RUN | true | true | 审批前先模拟执行 |
| IMPORT_MUTATION_ENABLED | false | false | 禁止导入修改 |

## API 端点一览

| 端点 | 方法 | 说明 |
|------|------|------|
| ws://127.0.0.1:28789 | WebSocket | 实时双向通信 |
| /api/sessions | GET | 获取会话列表 |
| /api/cron | GET/POST | 定时任务管理 |
| /api/config | GET | 配置查询 |
| /api/skills | GET | 技能列表 |
| /api/status | GET | 系统状态 |

> 🔑 所有修改型 API 需要请求头：`Authorization: Bearer {token}`

## OpenClaw 三层架构

```
🔧 Tools 工具层     →  exec · browser · web_search · cron · session · read/write/edit
   ↓
🧠 Skills 技能层    →  SKILL.md 引导何时 + 如何使用工具
   ↓
🧩 Plugins 插件层  →  注册额外工具 · 扩展渠道
```

### Lobster 工作流引擎

```
🔍 收集数据 → 🧠 AI决策 → ⚡ 执行步骤 → ✅ 人工审批 → 📤 输出结果
```

Lobster = 多步骤工具链确定性执行 + 内置审批点 + 可恢复状态 · JSON 驱动
