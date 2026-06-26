# openclaw.json 飞书 Agent 配置结构说明

本文件说明新增一个飞书 Agent 时需要修改的三处位置，每处均附完整示例。

---

## 位置 1：`channels.feishu.accounts`

**作用**：注册飞书 Bot 凭据，每个 account key 对应一个独立的飞书应用。

**路径**：`channels > feishu > accounts > {accountId}`

### 已有 1 个 account 时，新增第 2 个的示例：
```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "dmPolicy": "pairing",
      "accounts": {
        "main": {
          "appId": "cli_existing111",
          "appSecret": "existing_secret",
        },
        "mybot": {
          "appId": "cli_abc123",
          "appSecret": "new_secret_xxx"
        }
      }
    }
  }
}
```

---

## 位置 2：`agents.list`

**作用**：声明 Agent 实例，每个 id 唯一。`workspace` 指定工作目录。

**路径**：`agents > list > []（数组追加）`

### 已有 1 个 agent 时，新增第 2 个的示例：
```json
{
  "agents": {
    "list": [
      {
        "id": "main"
      },
      {
        "id": "mybot",
        "workspace": "/Users/username/.openclaw/workspace/mybot",
        "name":"我的新助手"
      }
    ]
  }
}
```

---

## 位置 3：`bindings`

**作用**：将飞书渠道的消息路由到指定 Agent。`accountId` 与 `channels.feishu.accounts` 的 key 对应。

**路径**：`bindings > []（数组追加）`

### 已有 1 条 binding 时，新增第 2 条的示例（DM 路由）：
```json
{
  "bindings": [
    {
      "agentId": "main",
      "match": {
        "channel": "feishu",
        "accountId": "main",
      }
    },
    {
      "agentId": "mybot",
      "match": {
        "channel": "feishu",
        "accountId": "mybot"
      }
    }
  ]
}
```