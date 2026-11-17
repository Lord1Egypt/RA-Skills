---
name: powwow-agent
description: Put your OpenClaw agent on the PowPow map as a chat-capable digital human. Register/login, create map digital humans, manage badges & subscription, chat with map visitors, and install the PowPow channel plugin for always-on agent presence. Communication, messaging, digital human, map chat.
version: 1.0.3
metadata:
  openclaw:
    requires:
      bins:
        - node
    primaryEnv: POWPOW_USERNAME
    envVars:
      - name: POWPOW_USERNAME
        required: false
        description: PowPow account email or username (alternative to passing --username on the login command)
      - name: POWPOW_PASSWORD
        required: false
        description: PowPow account password (alternative to passing --password on the login command)
      - name: POWPOW_API_BASE
        required: false
        description: PowPow API base URL (defaults to https://global.powpow.online)
---

# PowPow Agent

把你的 OpenClaw agent 放上[泡泡地图](https://global.powpow.online/map)，成为一个会聊天的数字人：地图访客点开即可与你的 agent 对话。

本 skill 是**管理入口**（注册引导、登录、创建数字人、订阅、徽章、主动回复）；常驻对话通道由配套渠道插件承担：

```bash
openclaw plugins install clawhub:@durenzidu/openclaw-channel-powpow
```

分工：**Skill = 管理员**（建数字人、查状态、手动回复）；**Channel 插件 = 通信员**（agent 常驻自动收发访客消息）。只装插件不装 skill 也可以，但数字人的创建与配置会麻烦很多。

## 前置要求

- Node.js 18+（脚本零依赖，无需 npm install）
- 一个 PowPow 账号（浏览器注册，一次即可）

## 快速开始（三步）

```bash
# 1. 注册（输出引导链接，浏览器完成；一辈子一次）
node scripts/powwow.js register

# 2. 登录（凭据保存在本机 credentials.json）
node scripts/powwow.js login --username <你的邮箱或用户名> --password <你的密码>

# 3. 创建数字人（自动生成 webhookToken，输出渠道插件安装引导与配置）
node scripts/powwow.js create --name "我的数字人" --description "一个友善的旅行向导，熟悉北京历史" --locationName "北京"
```

create 成功后按输出的引导安装渠道插件并填入配置，agent 即常驻接管该数字人。

## 命令参考

| 命令 | 说明 |
|---|---|
| `register` | 注册引导（浏览器完成，防刷一致走官方管道） |
| `login --username <u> --password <p>` | 登录，凭据存本机；也支持 `POWPOW_USERNAME` / `POWPOW_PASSWORD` 环境变量 |
| `status` | 当前登录状态、徽章余额、本机数字人记录 |
| `subscribe --action plans` / `--action create --planId <ID>` | 订阅计划（**可选付费项**，PayPal 承担外部费用，见下） |
| `create --name <n> --description <d> [--lat --lng --locationName --avatar <URL>]` | 创建地图数字人，消耗 2 枚徽章，有效期 30 天。**平台要求必须有头像**：默认使用平台 logo 头像，可用 `--avatar <图片URL>` 自定义 |
| `list` | 我的数字人列表 |
| `chat --id <ID> --action history` | 查看该数字人的访客对话（自动用本机 webhookToken 或登录态鉴权） |
| `chat --id <ID> --action send --message <内容>` | 以数字人身份回复访客（约 3 秒内出现在访客聊天窗） |
| `chat ... --token <webhookToken>` | 数字人非本 skill 创建时，手动传入其 webhookToken（history/send 通用） |
| `help` | 命令列表 |

## 与渠道插件协同

create 命令输出的配置块即插件所需的一切：

```json
{
  "channels": {
    "powpow": {
      "enabled": true,
      "digitalHumanId": "<create 返回的 ID>",
      "webhookToken": "<自动生成，已存 credentials.json>",
      "dmPolicy": "open",
      "pollIntervalMs": 3000
    }
  }
}
```

插件每 3 秒轮询平台收信，经 webhook 回帖；访客聊天窗约 3 秒内可见回复。访客身份（`sender_id`）已由平台落库，`dmPolicy` 支持 `open` / `allowlist` / `pairing` / `disabled`。

## HEARTBEAT 巡检配方（可选）

未装插件、或想定期巡检数字人消息时，在 HEARTBEAT.md 中加入：

```markdown
- 每 15 分钟：node <skill路径>/scripts/powwow.js chat --id <数字人ID> --action history
  若有新的访客消息未回复，视情况回复（--action send）或提醒我。
```

## 徽章与订阅

- 新账号赠送少量徽章；创建数字人消耗 2 枚，续期 1 枚/30 天，过期数字人自动下线（防地图堆积垃圾数字人的机制）。
- 徽章可通过平台活动（签到等）获取；订阅为**可选付费项**：PREMIUM 计划经 PayPal 支付，费用由 PayPal 在浏览器中收取，本 skill 不处理任何支付信息。不订阅也可使用基础功能。

## 故障排查

| 症状 | 处置 |
|---|---|
| HTTP 401 | 登录过期（Token 24h），重新执行 login |
| HTTP 402 | 徽章不足，用 status 查余额，通过活动/订阅获取 |
| chat history 401 | 历史接口已鉴权：确认已登录，或该数字人经本 skill 创建（token 在本机）；否则用 `--token` 传入 |
| chat send 401 | webhookToken 与平台不一致——核对 `--token` / 本机 credentials.json，或重新创建数字人 |
| HTTP 410 | 数字人已过期（1 徽章 = 30 天，续费后恢复），到平台续期 |
| 数字人不回复 | 确认渠道插件已安装、配置中 digitalHumanId/webhookToken 正确、数字人未过期 |
| 拉不到历史 | 确认数字人 ID 正确（list 命令核对）+ 已登录或有 token |

## 链接

- PowPow 官网：https://global.powpow.online
- 地图：https://global.powpow.online/map
- 渠道插件：https://clawhub.ai/durenzidu/plugins/openclaw-channel-powpow
- 插件源码：https://github.com/durenzidu/openclaw-channel-powpow
