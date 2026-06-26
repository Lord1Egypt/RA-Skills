# 配置字段说明

## agents.list

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "name": "智能助手",
        "workspace": "/root/.openclaw/workspace",
        "agentDir": "/root/.openclaw/agents/main/agent",
        "model": "minimax-cn/MiniMax-M2.5"
      }
    ]
  }
}
```

| 字段 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `id` | 是 | Agent 唯一标识 | `main`, `agent2`, `fund-manager` |
| `name` | 否 | 显示名称 | `智能助手`, `基金管理员` |
| `workspace` | 否 | 工作目录 | `/root/.openclaw/workspace2` |
| `agentDir` | 否 | Agent 状态目录 | `/root/.openclaw/agents/agent2/agent` |
| `model` | 否 | 指定模型 | `minimax-cn/MiniMax-M2.5` |

## bindings

```json
{
  "bindings": [
    {
      "agentId": "agent2",
      "match": {
        "channel": "feishu",
        "accountId": "xiaozhushou"
      }
    }
  ]
}
```

| 字段 | 说明 |
|------|------|
| `agentId` | 对应 agents.list 中的 id |
| `match.channel` | 渠道类型，当前支持 `feishu` |
| `match.accountId` | 账号标识，对应 channels.feishu.accounts 中的 key |

## channels.feishu.accounts

```json
{
  "channels": {
    "feishu": {
      "accounts": {
        "main": {
          "appId": "cli_xxx",
          "appSecret": "xxx"
        }
      }
    }
  }
}
```

| 字段 | 说明 |
|------|------|
| `appId` | 飞书应用 ID，格式 `cli_xxxx` |
| `appSecret` | 飞书应用密钥 |

## 完整配置示例

```json
{
  "agents": {
    "list": [
      {"id": "main", "name": "智能助手"},
      {"id": "agent2", "name": "小助手", "workspace": "/root/.openclaw/workspace2"},
      {"id": "agent3", "name": "skill调试员", "workspace": "/root/.openclaw/workspace3"},
      {"id": "fund-manager", "name": "基金管理员", "workspace": "/root/.openclaw/workspace4"}
    ]
  },
  "bindings": [
    {"agentId": "main", "match": {"channel": "feishu", "accountId": "main"}},
    {"agentId": "agent2", "match": {"channel": "feishu", "accountId": "xiaozhushou"}},
    {"agentId": "agent3", "match": {"channel": "feishu", "accountId": "agent3"}},
    {"agentId": "fund-manager", "match": {"channel": "feishu", "accountId": "fund-manager"}}
  ],
  "channels": {
    "feishu": {
      "accounts": {
        "main": {"appId": "cli_xxx1", "appSecret": "xxx1"},
        "xiaozhushou": {"appId": "cli_xxx2", "appSecret": "xxx2"},
        "agent3": {"appId": "cli_xxx3", "appSecret": "xxx3"},
        "fund-manager": {"appId": "cli_xxx4", "appSecret": "xxx4"}
      }
    }
  }
}
```
