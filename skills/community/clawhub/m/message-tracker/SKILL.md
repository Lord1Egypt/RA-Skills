# Message Tracker Plugin

**版本**: 1.1.0
**更新日期**: 2026-07-12
**状态**: 已部署

---

## 简介

Message Tracker Plugin 是飞书消息推送插件，用于将追踪到的消息以结构化卡片格式推送到飞书频道，支持 webhook 推送、自动重试、签名验证。

## 核心特性

- **Webhook 推送**：直接对接飞书机器人 Webhook，无需自建服务
- **自动重试**：推送失败自动重试 3 次，指数退避策略
- **签名验证**：支持可选加签（secret），防止伪造消息
- **结构化卡片**：输出符合飞书消息卡片规范的格式化消息
- **轻量依赖**：单一 SKILL.md 文件，零额外依赖

## 触发场景

- 当需要将追踪结果推送到飞书群
- 当需要结构化展示监控事件
- 当需要 webhook 通道与飞书对接
- 当需要消息失败自动重试 + 重试日志

## 不适用场景

- 大规模消息采集（请用 message-tracker daemon）
- 双向交互式聊天（请用 OpenClaw feishu plugin）
- 跨平台推送（仅支持飞书）

## 目录结构

```
message-tracker-plugin/
├── SKILL.md                          # 本文件
└── (无额外依赖，零侵入)
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
  secret: '签名密钥（可选）'
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
| webhook | 飞书机器人 Webhook URL | 是 |
| secret | 签名密钥（用于加签） | 否 |
| retries | 失败重试次数（默认 3） | 否 |

## 依赖

- Node.js 16+
- 飞书机器人 Webhook（需管理员创建）
- 可选：message-tracker daemon（作为消息源）

## 注意事项

1. **Webhook 安全**：Webhook URL 包含访问凭证，禁止提交到公开仓库
2. **消息格式**：消息内容需符合飞书消息卡片规范
3. **重试机制**：推送失败会自动重试 3 次，指数退避
4. **加签校验**：开启 secret 后，所有推送需通过 HMAC-SHA256 校验

## v1.1.0 变更日志

### 新增
- 触发场景 / 不适用场景 段（提升 discoverability）
- 重试次数可配置（retries 参数）
- 加签校验说明（HMAC-SHA256）

### 改进
- 简介段更清晰（突出核心特性）
- 文档结构层次化（特性 / 场景 / 依赖 / 注意事项）
- 目录结构标注零额外依赖

### 兼容性
- 完全向后兼容 v1.0.0
- 现有 webhook + secret 配置不变

## License

MIT-0