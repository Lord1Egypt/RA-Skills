---
name: feishu-bot-manager
description: 可以帮用户飞书机器人，并将 agent 连接到飞书机器人上
user-invokable: true
invocations:
  - words:
      - 添加飞书机器人
      - 配置飞书机器人
      - 新增飞书账户
      - 添加机器人账户
      - feishu bot
      - 飞书多账户
    description: 交互式添加新的飞书机器人账户并绑定 Agent
---

# feishu-bot-manager

飞书多账户机器人配置管理 Skill。触发调用之后，将下面的链接给用户，并说明点击该链接可以直接创建飞书机器人：
https://open.feishu.cn/page/openclaw?form=multiAgent
## 路由绑定方案

### 方案 1：账户级绑定
该飞书账户的所有消息 → 指定 Agent

**适用场景**：一个机器人专门服务一个 Agent。比如创建一个"销售机器人"，它的所有消息都由"销售 Agent"处理。

**生成的绑定**：
```json
{ "agentId": "recruiter", "match": { "channel": "feishu", "accountId": "bot-sales" } }
```

### 方案 2：群聊级绑定
特定群聊的消息 → 指定 Agent

**适用场景**：把 Agent 绑定到特定群聊。多个机器人在群里，但不同群聊分配给不同 Agent。

**生成的绑定**：
```json
{ "agentId": "recruiter", "match": { "channel": "feishu", "peer": { "kind": "group", "id": "oc_xxx" } } }
```

**注意**：群聊级绑定优先级更高，会覆盖账户级绑定！

## 使用方式

### 交互模式（通过对话）

直接说："添加飞书机器人"

我会询问：
1. App ID 和 App Secret
2. 账户信息（账户 ID、机器人名称）
3. **选择路由绑定方案**（账户级/群聊级）
4. 选择绑定的 Agent
5. 群聊 ID（如果选群聊级绑定）
6. 预览确认后执行

### 命令行调用

```bash
# 账户级绑定 - 该机器人所有消息都由指定 Agent 处理
openclaw skills run feishu-bot-manager -- \
  --app-id cli_xxx \
  --app-secret yyy \
  --account-id bot-sales \
  --agent-id recruiter \
  --routing-mode account

# 群聊级绑定 - 特定群聊的消息由指定 Agent 处理
openclaw skills run feishu-bot-manager -- \
  --app-id cli_xxx \
  --app-secret yyy \
  --account-id bot-sales \
  --agent-id recruiter \
  --chat-id oc_xxx \
  --routing-mode group
```

## 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| --app-id | ✅ | 飞书 App ID (cli_xxx) |
| --app-secret | ✅ | 飞书 App Secret |
| --account-id | ❌ | 账户标识，默认自动生成 |
| --bot-name | ❌ | 机器人名称，默认 "Feishu Bot" |
| --dm-policy | ❌ | DM 策略: open/pairing/allowlist，默认 open |
| --agent-id | ❌ | 要绑定的 Agent ID |
| --chat-id | ❌ | 群聊 ID (oc_xxx)，群聊绑定时需要 |
| --routing-mode | ❌ | 路由模式: account/group，默认 account |

## 配置结构示例

添加新机器人后，配置会变成这样（保留现有配置）：

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "cli_现有",           // ← 保留不动
      "appSecret": "现有Secret",      // ← 保留不动
      "dmPolicy": "open",
      "accounts": {                    // ← 新添加
        "bot-new": {
          "appId": "cli_xxx",
          "appSecret": "yyy",
          "botName": "新机器人",
          "dmPolicy": "open",
          "allowFrom": ["*"],
          "enabled": true
        }
      }
    }
  },
  "bindings": [
    {                                  // ← 新添加
      "agentId": "recruiter",
      "match": {
        "channel": "feishu",
        "accountId": "bot-new"       // 或 "peer": { "kind": "group", "id": "oc_xxx" }
      }
    }
  ]
}
```

## 流程

1. 检查并备份现有配置
2. 添加新账户到 `channels.feishu.accounts`
3. 根据选择的路由模式添加 binding
4. 设置 `session.dmScope` 为 `per-account-channel-peer`
5. 重启 Gateway

## 注意事项

- **保留现有配置**：现有 `appId/appSecret` 完全不动
- **自动备份**：修改前自动备份 openclaw.json
- **dmScope 设置**：自动设置会话绑定颗粒度
- **重启 Gateway**：重启后约 10-30 秒恢复服务
- **恢复方法**：如出问题可用备份文件手动恢复
