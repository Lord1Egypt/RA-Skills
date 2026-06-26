# Templates

## 1. 角色清单模板

先让用户补齐这张表：

```markdown
| agentId | roleName | accountId | appId | appSecret | openId | workspace | agentDir | responsibility | triggerTerms | isCoordinator |
|---|---|---|---|---|---|---|---|---|---|---|
| main | Coordinator | coordinator | cli_xxx | secret_xxx | ou_xxx | /path/to/workspace | /path/to/agent | 默认总调度 | @Boss @Coordinator | yes |
| design | Design Lead | design | cli_xxx | secret_xxx | ou_xxx | /path/to/workspace | /path/to/agent | 设计/交互/视觉 | @设计 @Design | no |
| engineering | Engineering Lead | engineering | cli_xxx | secret_xxx | ou_xxx | /path/to/workspace | /path/to/agent | 技术/实现/架构 | @开发 @Engineering | no |
| ops | Operations Lead | ops | cli_xxx | secret_xxx | ou_xxx | /path/to/workspace | /path/to/agent | 运营/传播/增长 | @运营 @Ops | no |
```
```

## 2. `PROTOCOL.md` 核心段落模板

```markdown
## 飞书通信协议

飞书不会把 bot 消息传递给其他 bot，必须通过 `sessions_send` 直接联系。

### 总原则

飞书里的 `<at>` 只有“给人看”的作用，OpenClaw 里的 `sessions_send` 才有“唤醒另一个 agent”的作用。

所以，只要一个 agent 想让另一个 agent 在群里发言，必须同时做两件事：

1. 在飞书群里发一条带 `<at>` 标签的消息
2. 立刻用 `sessions_send` 把同样的任务投递给目标 agent

### 委派步骤

1. 从当前 session key 提取群组 ID（`oc_xxx`）
2. 构造目标 session key：`agent:{targetAgentId}:feishu:group:oc_xxx`
3. 在飞书群消息中使用 `<at>` 标签点名目标 agent
4. 调用 `sessions_send`
5. 要求对方直接用 `message` 工具回复到：
   - `target: chat:oc_xxx`
   - `accountId: {targetAccountId}`

### 收到 sessions_send 时

直接回群，不回复发起者。

如需继续拉另一个 agent：

1. 先在群里 `<at>`
2. 再发 `sessions_send`
```

## 3. 协调者 `IDENTITY.md` 模板

```markdown
## 飞书群协作

你是默认总调度。群里出现一个新问题时，先判断：

1. 这件事值不值得做
2. 该由谁主答
3. 是否需要多人并行讨论

只要需要别人参与，就必须同时做两步：

1. 在群里用飞书 `<at>` 显式点名
2. 对目标 agent 调用 `sessions_send`

绝对禁止：

- 只发裸文本 `@角色`
- 只发 `<at>` 不发 `sessions_send`
- 给 `sessions_send` 传 `agentId`
```

## 4. 专业角色 `IDENTITY.md` 模板

```markdown
## 飞书群协作

如果协调者或其他 agent 通过 `sessions_send` 把你拉进群聊，你要直接用 `message` 回复飞书群，而不是回复发起者。

如果你的判断需要另一个 agent 补位，也必须同时做：

1. 在群里用 `<at>` 显式点名
2. 用 `sessions_send` 实际通知对方
```

## 5. `openclaw.json` 模板片段

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "workspace": "/path/to/workspace",
        "agentDir": "/path/to/agent"
      },
      {
        "id": "design",
        "workspace": "/path/to/workspace",
        "agentDir": "/path/to/agent"
      }
    ]
  },
  "tools": {
    "sessions": {
      "visibility": "all"
    },
    "agentToAgent": {
      "enabled": true,
      "allow": ["main", "design", "engineering", "ops"]
    }
  },
  "bindings": [
    {
      "agentId": "main",
      "match": {
        "channel": "feishu",
        "accountId": "coordinator"
      }
    },
    {
      "agentId": "design",
      "match": {
        "channel": "feishu",
        "accountId": "design"
      }
    }
  ]
}
```

## 6. `<at>` 模板

```text
<at user_id="{openId}">{roleName}</at>
```

## 7. `sessions_send` 模板

```text
sessionKey: agent:{targetAgentId}:feishu:group:oc_xxx

message:
{coordinatorName} 在群 oc_xxx 中需要你的意见。

请直接用 message 工具回复到飞书群：
  target: chat:oc_xxx
  accountId: {targetAccountId}

请从 {responsibility} 角度回答：
- ...

如果你认为还需要另一位 agent 参与，你可以在群里显式 @ 对方，
但必须同时再发一次 sessions_send 给对方。

不需要回我，直接回群。
```

## 8. 群 session 修复模板

如果某个群 session 被错误写成 `webchat`，目标形态应为：

```json
{
  "channel": "feishu",
  "chatType": "group",
  "displayName": "feishu:g-oc_xxx",
  "subject": "oc_xxx",
  "deliveryContext": {
    "channel": "feishu",
    "to": "chat:oc_xxx",
    "accountId": "targetAccountId"
  },
  "lastChannel": "feishu",
  "lastTo": "chat:oc_xxx",
  "lastAccountId": "targetAccountId"
}
```

## 9. 测试话术模板

```text
@{coordinatorTrigger} 让其他人一起讨论一下这个问题，分别从各自角度给我判断。
```

```text
@{coordinatorTrigger} 这件事你来判断该让谁处理，如果需要多人讨论就直接拉起他们。
```
