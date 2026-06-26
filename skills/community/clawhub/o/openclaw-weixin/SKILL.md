---
name: openclaw-weixin
description: OpenClaw 微信 channel 插件，支持扫码登录授权。接收微信消息、回复图文/文字/文件，提供完整的微信通道集成。
metadata:
  {
    "openclaw": {
      "requires": { "bins": ["openclaw"] },
      "install": [
        {
          "id": "node",
          "kind": "node",
          "package": "@tencent-weixin/openclaw-weixin",
          "label": "Install Weixin Channel Plugin (npm)"
        }
      ]
    }
  }
---

# OpenClaw Weixin Channel

微信 channel 插件，支持扫码登录 + 消息收发。

## 安装

```bash
npm install -g @tencent-weixin/openclaw-weixin
```

## 配置

```bash
openclaw plugins install "@tencent-weixin/openclaw-weixin"
openclaw config set plugins.entries.openclaw-weixin.enabled true
```

## 扫码登录

```bash
openclaw channels login --channel openclaw-weixin
```

## 兼容性

| 插件版本 | OpenClaw 版本 |
|---------|--------------|
| 2.0.x   | >=2026.3.22  |
| 1.0.x   | >=2026.1.0  |

## 来源

腾讯微信团队出品 · MIT License
