---
name: huo15-wecom
description: "火一五·企业微信（WeCom）OpenClaw 插件 v2.8.25 — 默认走 Bot WebSocket（响应快、配置简单），自带加密媒体解密 / Agent 主动发消息 / 微信客服三通道接入 / 多账号切换。v2.8.25 重点：GUIDANCE 优先级翻转回 MEDIA: 直发——v2.8.22 当时担心 stream 截断 + 86008 把链接设为优先，v2.8.23/v2.8.24 修了群聊主动推送通道 + UI 锁交互后 MEDIA: 路径稳定可靠，应用户偏好翻转：默认 MEDIA: 直发，仅大文件（> 企微上限）才走 enhance_share_file 链接。GUIDANCE 加决策表 + 用户偏好覆盖。继承 v2.8.24 placeholder timeout 解锁、v2.8.23 群聊主动推送、v2.8.20 MEDIA: parser。Use when: 接企业微信、给企微 Bot/自建应用接 OpenClaw、用微信客服收外部用户消息、需要图片/文件双向、跨账号切换。Do NOT use for 个人微信（不同协议）。"
version: 2.9.4
homepage: https://cnb.cool/huo15/ai/huo15-wecom-plugin
metadata: { "openclaw": { "emoji": "🦜", "requires": { "bins": [] } } }
---

# 火一五企业微信插件

`@huo15/wecom` 是 OpenClaw 的企业微信通道插件，fork 自 [yanhaidao/wecom](https://github.com/yanhaidao/wecom) 并持续合并上游。**默认 Bot WebSocket 模式**，配置简单、响应快；同时支持 Agent 自建应用主动推送和微信客服三方通道。

## 三条消息通道

| 通道 | 用途 | 配置入口 |
|---|---|---|
| **Bot WebSocket** | 默认推荐，企业微信"智能机器人"WS 协议，免公网回调 | `channels.wecom.accounts.<id>.bot.ws` |
| **Agent 自建应用** | 走企微官方 API（CorpId/AgentId/Secret），支持主动推送给指定用户/群 | `channels.wecom.accounts.<id>.agent` |
| **微信客服** | 接管"客服会话"，外部客户在微信/视频号里发给客服账号的消息 | `channels.wecom.accounts.<id>.kefu` |

三条通道可以**单独启用**或**组合启用**，多账号场景每个账号独立配置。

## 安装

```bash
# OpenClaw 内置安装（推荐）
openclaw plugins install @huo15/wecom

# 或者直接 npm
npm install @huo15/wecom
```

## 最小配置（Bot WS 模式）

```yaml
# ~/.openclaw/openclaw.json 中
channels:
  wecom:
    enabled: true
    accounts:
      default:
        bot:
          ws:
            botId: "你的智能机器人 ID"
            secret: "WS 密钥"
```

启动后，Bot 收到的消息会自动路由到默认 Agent，回复也通过 WS 直接送回 — 不需要部署任何回调 endpoint。

## 关键能力

- **加密媒体解密**：图片/文件/语音 AES-256-CBC 解密直接拿 buffer，可让 Agent 直接读取（OCR / ASR / 文档解析）
- **Markdown V2**：支持企微富文本（标题、表格、代码块、链接、引用），自动适配 chat 上下文
- **图片回复**：`![alt](url)` 自动抽离 + uploadMedia + replyMedia，COS/OSS 预签名 URL 失败时降级为占位文本（不让"链接已过期"漏到客户端）
- **多账号切换**：单实例支持多个企业、多个智能体并存，按 conversation 路由
- **流式回复**：placeholder + partial replyStream（最多 8 次中间更新）+ ack timeout watchdog 自动重连

## v2.8.8 关键修复（WS BOT 图片）

1. **Reply 通道纠错**：reply 上下文从 `sendMediaMessage`（主动推送）改用 `replyMedia`（被动回复，绑定 reqId）
2. **入向多图**：`mixed` 与 `quote.mixed` 类型从只取首张改为全部提取；首张挂 `ctx.MediaPath`，其余落盘 + info 日志
3. **Outbound fetch UA**：从裸 `fetch` 切到 plugin-sdk `fetchRemoteMedia`，显式带 desktop User-Agent，避免部分 Tencent COS / 阿里 OSS bucket 拒绝 Node 默认 UA
4. **解析可观测性**：媒体类型消息但无 attachments 时记 warn 日志（含 msgid + body keys），便于 SDK 字段漂移排查

详见 [changelog/v2.8.8.md](./changelog/v2.8.8.md)。

## 安全实践

- LLM 输出的 `touser` / `chatid` 经 `resolveWecomTarget` sanitizer，**拒绝 `@all` / `@everyone` / `*` 等广播字面量**（v2.8.1 SECURITY 修复）
- 跨企业上下游消息走 upstream-delivery 通道，不与本企业 Agent API 混用
- 微信客服 `corpSecret` 可与 Agent `corpSecret` 独立配置，权限隔离

## 不变的设计原则

- **Bot WS 优先**：能用 WS 就不用 Agent API（少配置、低延迟）
- **失败降级**：WS reply ack timeout 自动 fallback 到 Agent API（保留消息可达性），watchdog 连续 8 次后触发 WS 重连
- **不修改 OpenClaw 核心**：所有功能通过 channel plugin SDK 注册

## 仓库

- 主仓库：https://cnb.cool/huo15/ai/huo15-wecom-plugin
- 镜像：https://github.com/zhaobod1/huo15-wecom-plugin
- 上游 fork 源：https://github.com/yanhaidao/wecom（**仅 fetch，不 push**）

## License

ISC（继承自 yanhaidao/wecom 上游）。
