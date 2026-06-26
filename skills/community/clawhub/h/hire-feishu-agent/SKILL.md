---
name: hire-feishu-agent
description: |
  **当用户说出以下类似语句时触发本 Skill**：
  - "帮我招聘一个飞书助理"
  - "新增一个飞书渠道的 Agent"
  - "我要在飞书上部署一个新 Agent"
  - "hire a Feishu agent"
---

# Skill: 招聘飞书 Agent（hire-feishu-agent）

## 操作流程

### Step 1 — 收集参数（向用户确认以下信息）

如果用户没有主动提供，**主动询问**：

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `agentId` / `accountId` | Agent 唯一 ID，同时用于 account key 和 agentId | `mybot` |
| `agentName` | Agent 展示名称（botName） | `我的助手` |
| `appId` | 飞书应用的 App ID | `cli_abc123` |
| `appSecret` | 飞书应用的 App Secret | `xxxxxxxxxxxxxxxx` |

询问话术示例：
> 我需要以下信息来完成配置，请逐一确认：
> 1. Agent ID（同时作为飞书账号 key）：
> 2. Agent 展示名称（botName）：
> 3. 飞书 App ID（cli_ 开头）：
> 4. 飞书 App Secret：

---

### Step 2 — 修改 `~/.openclaw/openclaw.json` 三处位置

参考 `schema.md` 中的结构说明，按以下顺序修改：

#### 修改位置 1：`channels.feishu.accounts`
在 `accounts` 对象中**新增一个 key**，key 名 = `{agentId}`：
```json
"channels": {
  "feishu": {
    "accounts": {
      "{agentId}": {
        "appId": "{appId}",
        "appSecret": "{appSecret}"
      }
    }
  }
}
```

#### 修改位置 2：`agents.list`
在数组中**追加一个对象**：
```json
"agents": {
  "list": [
    {
      "id": "{agentId}",
      "workspace": "/Users/${USER}/.openclaw/workspace/[agentId]",
      "name": "{agentName}"
    }
  ]
}
```

#### 修改位置 3：`bindings`
在数组中**追加一个绑定规则**（DM 默认路由）：
```json
"bindings": [
  {
    "agentId": "{agentId}",
    "match": {
      "channel": "feishu",
      "accountId": "{agentId}"
    }
  }
]
```

---

### Step 3 — 向用户输出最终合并后的 JSON 片段

将三处修改合并展示，方便用户直接复制粘贴进 `openclaw.json`，并提示：
```
修改完成后请运行：
  openclaw gateway restart
以使配置生效。
```

---

## 注意事项
- 如果 `channels.feishu.accounts` 已有其他 account，**只追加新 key，不要覆盖已有 key**。
- 如果 `agents.list` 已有其他 agent，**只追加，不要替换整个数组**。
- 如果 `bindings` 已有其他规则，**只追加，不要替换整个数组**。
- `agentId` 只允许使用小写字母、数字、连字符（`-`），不能含空格。