# 多 Agent 支持说明

## 概述

li-feishu-audio 技能已支持多 Agent 模式，可以根据不同的 Agent 自动使用对应的飞书账户凭证。

## 配置方式

### openclaw.json 配置

```json
{
  "bindings": [
    {"agentId": "coder", "match": {"channel": "feishu", "accountId": "coder"}},
    {"agentId": "writer", "match": {"channel": "feishu", "accountId": "writer"}}
  ],
  "channels": {
    "feishu": {
      "defaultAccount": "coder",
      "accounts": {
        "coder": {
          "name": "编程助手",
          "appId": "cli_a94ed64eb1f89bc0",
          "appSecret": "xxx"
        },
        "writer": {
          "name": "写作助手",
          "appId": "cli_a94980d5d9381bda",
          "appSecret": "xxx"
        }
      }
    }
  }
}
```

### 凭证读取优先级

| 优先级 | 来源 | 说明 |
|--------|------|------|
| 1 | 参数指定 | `feishu-tts.sh audio.mp3 user_id coder` |
| 2 | 环境变量 | `OPENCLAW_ACCOUNT_ID=coder` |
| 3 | 默认账户 | `openclaw.json` 中的 `defaultAccount` |

### 运行时自动识别

OpenClaw 会在运行时注入 `OPENCLAW_ACCOUNT_ID` 环境变量，技能会自动读取对应账户的凭证。

## 验证多账户配置

```bash
# 运行健康检查
./scripts/healthcheck.sh

# 输出示例：
# [PASS] 飞书账户 [coder]: cli_a94ed64eb1f89bc0
# [PASS] 飞书账户 [writer]: cli_a94980d5d9381bda
```

## 手动指定账户

```bash
# 发送语音到 coder 账户
./scripts/feishu-tts.sh output.mp3 ou_xxx coder

# 发送语音到 writer 账户
./scripts/feishu-tts.sh output.mp3 ou_xxx writer
```

## 工作流程

```
用户发送语音消息
    ↓
OpenClaw 识别 agent (通过 bindings)
    ↓
注入 OPENCLAW_ACCOUNT_ID 环境变量
    ↓
技能读取对应账户凭证
    ↓
使用正确的飞书应用发送回复
```