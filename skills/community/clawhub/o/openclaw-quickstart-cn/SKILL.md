# OpenClaw 快速入门（中文版）

> 5分钟上手 OpenClaw，国产 AI 模型配置指南

## 适用场景

- 刚接触 OpenClaw 的中国用户
- 想用国产 AI（DeepSeek/智谱/通义）替代 OpenAI
- 不想折腾配置，想要开箱即用

## 快速开始

### 1. 环境检测

```bash
# 检查 Node.js 版本（需要 18+）
node --version

# 检查系统信息
uname -a
```

### 2. 安装 OpenClaw

```bash
# macOS/Linux
curl -fsSL https://get.openclaw.ai | bash

# 或使用 npm
npm install -g openclaw
```

### 3. 配置国产 AI 模型

#### DeepSeek（推荐，最便宜）

```bash
# 获取 API Key：https://platform.deepseek.com/
openclaw configure --section ai --set deepseek.apiKey=YOUR_KEY
```

#### 智谱 GLM（稳定，中文友好）

```bash
# 获取 API Key：https://open.bigmodel.cn/
openclaw configure --section ai --set zhipu.apiKey=YOUR_KEY
```

#### 通义千问（阿里云）

```bash
# 获取 API Key：https://dashscope.console.aliyun.com/
openclaw configure --section ai --set qwen.apiKey=YOUR_KEY
```

### 4. 测试连接

```bash
openclaw status
```

看到 `✓ AI: connected` 就成功了！

## 价格对比（2026-03）

| 模型 | 输入（每万tokens） | 输出（每万tokens） | 备注 |
|------|-------------------|-------------------|------|
| DeepSeek V3 | ¥0.27 | ¥1.08 | 最便宜，推荐 |
| 智谱 GLM-4 | ¥0.10 | ¥0.10 | 限时免费 |
| 通义千问 | ¥0.008 | ¥0.008 | 最便宜但限流 |
| GPT-4o | ¥17.5 | ¥52.5 | 贵150倍 |

## 常见问题

### Q: 如何切换模型？

```bash
openclaw configure --section ai --set defaultModel=deepseek/deepseek-chat
```

### Q: 如何查看当前配置？

```bash
openclaw config list
```

### Q: 连接失败怎么办？

1. 检查 API Key 是否正确
2. 检查网络（部分平台需要 VPN）
3. 查看日志：`openclaw logs`

## 付费支持

需要人工安装配置？微信：[待补充]

- 基础安装：¥99
- 高级配置（含多模型）：¥299
- 企业部署：¥999

---

**作者**：OpenClaw 中文社区
**版本**：1.0.0
**更新**：2026-03-26
