# Hooks & Webhooks 参考

## Hooks 概述
事件驱动自动化，响应智能体命令和生命周期事件。

### 发现目录 (优先级从高到低)
1. `<workspace>/hooks/` — 工作区级
2. `~/.openclaw/hooks/` — 用户级(跨工作区)
3. `<openclaw>/dist/hooks/bundled/` — 内置

### Hook 结构
```
my-hook/
├── HOOK.md      # 元数据(YAML frontmatter) + 文档
└── handler.ts   # 处理程序
```

### HOOK.md 格式
```yaml
---
name: my-hook
description: "描述"
metadata:
  openclaw:
    emoji: "🎯"
    events: ["command:new"]
    requires:
      bins: ["node"]
      env: ["MY_KEY"]
      os: ["darwin"]
---
```

### 事件类型
| 事件 | 触发时机 |
|------|----------|
| `command:new` | `/new` 命令 |
| `command:reset` | `/reset` 命令 |
| `command:stop` | `/stop` 命令 |
| `command` | 所有命令(通用) |
| `agent:bootstrap` | 注入引导文件前 |
| `gateway:startup` | 网关启动后 |
| `tool_result_persist` | 工具结果持久化前(同步) |

### 内置 Hooks
| Hook | 事件 | 功能 |
|------|------|------|
| `session-memory` | command:new | `/new`时保存会话到记忆 |
| `command-logger` | command | 记录命令到 `~/.openclaw/logs/commands.log` |
| `boot-md` | gateway:startup | 启动时运行 BOOT.md |

### CLI
```bash
openclaw hooks list [--eligible] [--verbose]
openclaw hooks info <name>
openclaw hooks check
openclaw hooks enable <name>
openclaw hooks disable <name>
openclaw hooks install <path-or-spec>  # 安装hook包
```

### 配置
```json5
hooks: {
  internal: {
    enabled: true,
    entries: {
      "session-memory": { enabled: true },
      "command-logger": { enabled: false }
    },
    load: {
      extraDirs: ["/path/to/more/hooks"]  // 额外目录
    }
  }
}
```

### 处理程序示例
```typescript
import type { HookHandler } from "../../src/hooks/hooks.js";
const handler: HookHandler = async (event) => {
  if (event.type !== "command" || event.action !== "new") return;
  // event.sessionKey, event.timestamp, event.context.workspaceDir
  event.messages.push("✨ Hook executed!");  // 发送消息给用户
};
export default handler;
```

### 最佳实践
- 保持处理程序快速(异步fire-and-forget)
- 优雅处理错误(try/catch，不要throw)
- 尽早过滤不相关事件
- 使用具体事件键而非通用 `command`

## Webhooks

### 概述
外部HTTP webhooks让其他系统触发OpenClaw工作。

### 配置
```json5
hooks: {
  webhooks: {
    enabled: true,
    entries: {
      "my-webhook": {
        enabled: true,
        secret: "${WEBHOOK_SECRET}",
        sessionTarget: "isolated",
        payload: { kind: "agentTurn", message: "处理webhook: {{body}}" },
        delivery: { mode: "announce", channel: "telegram", to: "123" }
      }
    }
  }
}
```

### Gmail Webhook
```bash
openclaw webhooks gmail setup    # 设置Gmail推送通知
openclaw webhooks gmail run      # 手动运行
```

配置:
```json5
hooks: {
  gmail: {
    enabled: true,
    model: "provider/model",     // 可选模型覆盖
    delivery: { mode: "announce", channel: "telegram", to: "123" }
  }
}
```

## 认证监控

### CLI检查
```bash
openclaw models status --check
```
退出码: 0=正常, 1=过期/缺失, 2=即将过期(24h内)

### 自动化告警
```bash
# crontab示例
0 */6 * * * openclaw models status --check || openclaw message send --target "+155..." --message "⚠️ OAuth即将过期"
```

## 投票 (Polls)

### 支持渠道
WhatsApp, Discord, MS Teams

### CLI
```bash
openclaw message poll --target +15551234567 \
  --poll-question "午餐?" --poll-option "是" --poll-option "否"
# Discord
openclaw message poll --channel discord --target channel:123 \
  --poll-question "?" --poll-option A --poll-option B --poll-duration-hours 24
```

### 工具调用
```json5
{ action: "send", channel: "whatsapp", to: "+155...",
  pollQuestion: "午餐?", pollOption: ["是", "否"], pollMulti: false }
```

## Webhook 端点

### 启用
```json5
hooks: {
  enabled: true,
  token: "shared-secret",
  path: "/hooks"
}
```

### 调用
```bash
curl -X POST http://localhost:18789/hooks \
  -H "Authorization: Bearer shared-secret" \
  -H "Content-Type: application/json" \
  -d '{"text": "外部触发消息"}'
```

### Webhook任务配置
```json5
hooks: {
  webhooks: {
    entries: {
      "deploy-notify": {
        enabled: true,
        secret: "${WEBHOOK_SECRET}",
        sessionTarget: "isolated",
        payload: { kind: "agentTurn", message: "部署通知: {{body}}" },
        delivery: { mode: "announce", channel: "telegram", to: "123" }
      }
    }
  }
}
```
