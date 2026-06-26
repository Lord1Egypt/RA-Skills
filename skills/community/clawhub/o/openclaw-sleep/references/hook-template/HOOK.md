---
name: session-sleep-wake
description: "在 session 被 /new 或 /reset 重置后首次启动时，读取对应 session 的 preview 文件并注入未完成事项到新 session 上下文"
homepage: https://docs.openclaw.ai/automation/hooks
metadata:
  {
    "openclaw": {
      "emoji": "🌙",
      "events": ["agent:bootstrap"],
      "requires": { "config": ["workspace.dir"] },
      "install": [{ "id": "workspace", "kind": "workspace", "label": "Workspace hooks" }]
    }
  }
---

# Session Sleep-Wake Hook

## 触发条件

**本 hook 在 `agent:bootstrap` 事件时触发**，即 session 被 `/new` 或 `/reset` 重置之后、bootstrap 文件注入之前。

⚠️ **重要**：说"去睡觉"或发 `/sleep` 消息本身**不会**触发本 hook。必须有人执行 `/new` 或 `/reset`（或通过 Gateway API 触发 session reset），才会触发 `agent:bootstrap`，进而触发本 hook。

## 工作原理

1. **保存 preview**：在 session 结束前，将未完成事项写入 `workspace/previews/{sessionKey}.md`，状态设为 `pending`
2. **Session reset**：有人调用 `/new`/`/reset` 或 Gateway API `sessions.reset`
3. **Hook 触发**：`agent:bootstrap` 事件 firing
4. **注入**：本 hook 读取 preview 文件，将未完成事项注入 `event.context.bootstrapFiles`
5. **新 session 启动**：bootstrap file 被 prepend 到系统提示之前，新 session 一启动就能看到恢复信息

## Preview 文件格式

```
# Sleep Preview — {sessionKey}
# 生成时间：YYYY-MM-DD HH:mm

## 本次 session 摘要
一句话描述本次 session 主题

## 未完成事项
- [ ] 待办1
- [ ] 待办2

## 醒来后第一步
下一步要做什么

## 关键上下文
重要信息、数字、配置等

## 状态
pending
```

状态为 `pending` 时注入，为 `all_done` 时跳过。

## Event Structure

`agent:bootstrap` 事件的字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `event.type` | string | 恒为 `"agent"` |
| `event.action` | string | 恒为 `"bootstrap"` |
| `event.sessionKey` | string | 用于定位 preview 文件（如 `agent:main:feishu:group:oc_xxx`） |
| `event.workspaceDir` | string | 工作空间路径（**直接位于 event 顶层**） |
| `event.context` | object | bootstrap 上下文 |
| `event.context.bootstrapFiles` | array | 注入内容的目标数组 |

注入方式：`event.context.bootstrapFiles.unshift({ path, content, isInline: true })`
