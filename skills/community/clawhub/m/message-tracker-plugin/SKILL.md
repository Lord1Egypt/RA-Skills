# Message Tracker Plugin

**版本**: 1.0.0
**更新日期**: 2026-04-30
**状态**: 已部署

---

## 简介

message-tracker-plugin 是 message-tracker 的飞书插件模块，用于将追踪到的消息推送到飞书频道。

## 目录结构

```
message-tracker-plugin/
├── SKILL.md                          # 本文件
└── node_modules/                      # NPM依赖
```

## 功能说明

本插件作为 message-tracker 的扩展，负责：
- 将追踪消息推送到飞书
- 格式化消息内容
- 处理推送失败重试

## 使用方式

```javascript
const TrackerPlugin = require('message-tracker-plugin');

// 初始化插件
const plugin = new TrackerPlugin({
  webhook: '飞书Webhook地址',
  secret: '签名密钥'
});

// 发送消息
plugin.send({
  title: '消息标题',
  content: '消息内容',
  timestamp: Date.now()
});
```

## 配置说明

| 参数 | 说明 | 必填 |
|------|------|------|
| webhook | 飞书机器人Webhook URL | 是 |
| secret | 签名密钥（用于加签） | 否 |

## 依赖

- Node.js 16+
- 飞书机器人Webhook

## 注意事项

1. 确保Webhook地址有效
2. 消息格式需符合飞书消息卡片规范
3. 推送失败会自动重试3次