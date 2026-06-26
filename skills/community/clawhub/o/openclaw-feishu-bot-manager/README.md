# OpenClaw Feishu Bot Manager

飞书多账户机器人配置管理 skill。

用于把新的飞书机器人账户接入 OpenClaw，并把该账户或指定群聊安全地绑定到某个 Agent。

## 解决什么问题

很多团队不是只有一个飞书机器人，而是会按职能拆分：
- 销售机器人
- 招聘机器人
- 内部运营机器人
- 某个群专用机器人

这个 skill 解决的是两类麻烦事：
1. 把新的飞书机器人账户加进 OpenClaw 配置
2. 把消息路由精确绑定到指定 Agent 或指定群聊

它会尽量避免手改 `openclaw.json` 这种高风险操作，并在写入前做备份、冲突检查和配置校验。

## 核心能力

- 新增飞书机器人账户到 `channels.feishu.accounts`
- 支持账户级绑定
- 支持群聊级绑定
- 自动检查账户 / 群聊 / Agent 绑定冲突
- 写入前自动备份配置
- 写入后自动校验配置结构
- 可选自动设置 `session.dmScope`
- 可选自动重启 Gateway
- 支持 `--dry-run` 预演

## 两种路由模式

### 1) 账户级绑定
该飞书账户的所有消息，都路由到指定 Agent。

适合：一个机器人只服务一个 Agent。

生成的 binding 类似：

```json
{
  "agentId": "recruiter",
  "match": {
    "channel": "feishu",
    "accountId": "bot-recruiter"
  }
}
```

### 2) 群聊级绑定
指定群聊的消息，路由到指定 Agent。

适合：同一个飞书环境里，不同群聊由不同 Agent 接管。

生成的 binding 类似：

```json
{
  "agentId": "recruiter",
  "match": {
    "channel": "feishu",
    "peer": {
      "kind": "group",
      "id": "oc_xxx"
    }
  }
}
```

注意：群聊级绑定优先级高于账户级绑定。

## 安装

```bash
clawhub install openclaw-feishu-bot-manager
```

## 使用示例

### 账户级绑定

```bash
openclaw skills run openclaw-feishu-bot-manager -- \
  --app-id cli_xxx \
  --app-secret yyy \
  --account-id bot-sales \
  --agent-id sales-agent \
  --routing-mode account
```

### 群聊级绑定

```bash
openclaw skills run openclaw-feishu-bot-manager -- \
  --app-id cli_xxx \
  --app-secret yyy \
  --account-id bot-ops \
  --agent-id ops-agent \
  --chat-id oc_xxx \
  --routing-mode group
```

### 先预演，不落盘

```bash
openclaw skills run openclaw-feishu-bot-manager -- \
  --app-id cli_xxx \
  --app-secret yyy \
  --agent-id recruiter \
  --routing-mode account \
  --dry-run
```

## 参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `--app-id` | 是 | 飞书 App ID，格式 `cli_xxx` |
| `--app-secret` | 是 | 飞书 App Secret |
| `--account-id` | 否 | 账户标识，默认自动生成 |
| `--bot-name` | 否 | 机器人名称，默认 `Feishu Bot` |
| `--dm-policy` | 否 | `open` / `pairing` / `allowlist` |
| `--agent-id` | 否 | 要绑定的 Agent ID |
| `--chat-id` | 否 | 群聊 ID，群聊绑定时必填 |
| `--routing-mode` | 否 | `account` 或 `group`，默认 `account` |
| `--dry-run` | 否 | 仅预览，不写入、不重启 |
| `--force` | 否 | 忽略冲突警告继续执行 |
| `--no-restart` | 否 | 写入配置后不自动重启 Gateway |

## 工作流程

1. 读取现有 OpenClaw 配置
2. 检查账户 ID / 群聊 / Agent 绑定冲突
3. 备份 `~/.openclaw/openclaw.json`
4. 写入新的飞书账户配置
5. 写入 binding
6. 校验生成后的配置是否合法
7. 设置 `session.dmScope=per-account-channel-peer`
8. 重启 Gateway（除非显式跳过）

## 安全设计

这个 skill 的重点不是“能改配置”，而是“别把配置改坏”。

因此它做了这些保护：
- 修改前自动备份
- 默认做冲突检测
- 写入前进行结构校验
- 支持 dry-run 先看结果
- 允许手动跳过重启，降低变更风险

## 适用场景

- 新增一个飞书企业自建应用机器人
- 同时管理多个飞书机器人账户
- 给不同业务线分配不同 Agent
- 把某个群单独绑定到特定 Agent
- 不想手改 OpenClaw 配置文件

## 不适用场景

它不是飞书应用创建器。

如果你还没有飞书 App ID / App Secret，需要先创建飞书企业自建应用，再用本 skill 接入 OpenClaw。

## 版本建议

强烈建议：
- 先用 `--dry-run`
- 确认 binding 目标无误
- 再正式写入并重启 Gateway

这是配置层操作，做错了会直接影响消息路由。

## License

MIT
