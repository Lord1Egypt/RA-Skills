---
name: huo15-openclaw-wechat-service
description: "OpenClaw 微信服务号（公众号）渠道插件 v2.3.5 hotfix —— **修 errcode 45002 content size out of limit**：truncateForWechatText 改字节截断（微信限 2048 字节不是字符，中文 1 字 = 3 字节），默认 1900 字节留余量；保护 <a href> 标签不截在内部避免 XML 错乱；中文 / emoji / 混合场景全覆盖。症状：v2.3.0~v2.3.4 粉丝只收 placeholder 不收 LLM 真回复——根因 LLM 输出 > 600 中文字超 2048 字节被微信拒。承袭 v2.3.x 全部能力。287 vitest 用例全过。"
version: 2.3.5
homepage: https://cnb.cool/huo15/ai/huo15-openclaw-wechat-service
metadata: { "openclaw": { "emoji": "💬", "kind": "channel-plugin", "channelId": "wechat-service", "requires": { "bins": [] } } }
---

# huo15-openclaw-wechat-service v2.1.0

OpenClaw 微信服务号（公众号）渠道插件。

## 这是什么

把微信公众号接进 OpenClaw Agent 体系，让公众号粉丝可以直接和 LLM agent 聊天 / 接收通知 / 触发业务流程，覆盖**消息收发、内容发布、网页授权、数据分析、智能识别、卡券**六大维度。

## 安装

```bash
# 通过 OpenClaw 安装（推荐）
/install @huo15/wechat-service

# 或 npm
npm install @huo15/wechat-service
```

随后在 OpenClaw 里 `/setup wechat-service` 跑向导。

## 核心特性

### 🚀 一粉一会话动态 Agent

模仿 `@huo15/wecom` 的动态 Agent 框架：

```yaml
channels:
  wechat-service:
    dynamicAgents:
      enabled: true
      dmCreateAgent: true        # 每个 openid 一个 agent
      adminUsers: [oABC123xyz]   # 管理员旁路走 main agent
```

每个粉丝的 openid 自动派生独立 agent（命名 `wechat-service-{accountId}-dm-{sanitized_openid}`），实现真正的一对一会话隔离。

### 🛠️ 12 个 Agent Tool / 60+ API

| Tool | 主要 action |
|------|-------------|
| `wechat_service_menu` | 自定义菜单（基础 + 个性化）|
| `wechat_service_message` | 客服消息 + 模板消息 + 公模板库 + 一次性订阅 + 长期订阅通知（25 个 actions）|
| `wechat_service_material` | 临时/永久素材 |
| `wechat_service_article` | 草稿箱 + freepublish 流水线 |
| `wechat_service_user` | 用户/标签/黑名单 |
| `wechat_service_qrcode` | 带参二维码 + short_key |
| `wechat_service_mass_send` | 按标签/openid/预览群发 |
| `wechat_service_jssdk` | wx.config 签名 |
| `wechat_service_oauth` | 网页授权 OAuth2.0 全流程 |
| `wechat_service_analytics` | datacube 17 项指标 |
| `wechat_service_intelligent` | OCR 7 类 + 图像处理 3 项 |
| `wechat_service_card` | 卡券精简（6 个 actions）|

### 🧠 多账号矩阵 + 知识库双写

- `accounts.<id>` 隔离 webhook 路径、access_token、agent 路由
- 每条对话自动同步本地 markdown（Karpathy 风格）+ Odoo `knowledge.article`

## 配置示例

完整 schema 见 npm 包根目录 [`README.md`](./README.md) 里的「配置 Schema」段落。

最小可用配置：

```yaml
channels:
  wechat-service:
    accounts:
      main:
        appId: wx1234567890abcdef
        appSecret: ${WECHAT_SERVICE_APP_SECRET}
        token: ${WECHAT_SERVICE_TOKEN}
        encodingAESKey: ${WECHAT_SERVICE_AES_KEY}
        encryptMode: safe
```

## 路线图（已收官）

```
v0.1.0  初始版本
v0.2.0  ✅ Phase 0  动态 Agent 框架
v0.3.0  ✅ Phase 1  通知能力补全
v0.4.0  ✅ Phase 2  OAuth + 数据统计
v1.0.0  ✅ Phase 3  智能开放 + 卡券（latest）
```

## 资源

- **npm**：https://www.npmjs.com/package/@huo15/wechat-service
- **源码**（cnb）：https://cnb.cool/huo15/ai/huo15-openclaw-wechat-service
- **微信公众平台官方文档**：https://developers.weixin.qq.com/doc/service/guide/
- **OpenClaw**：https://docs.openclaw.ai/zh-CN

## 维护

青岛火一五信息科技有限公司（辉火云）· postmaster@huo15.com · QQ 群 1093992108

ISC © jobzhao
