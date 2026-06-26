---
name: openclaw-cn-installer
description: OpenClaw 中文安装配置助手。一键检测环境、配置国产 AI 模型（DeepSeek/智谱/阿里通义）。适合中国用户快速上手 OpenClaw。
version: 1.0.1
author: OpenClaw CN
tags:
  - openclaw
  - chinese
  - installer
  - setup
  - deepseek
  - zhipu
  - qwen
---

# OpenClaw 中文安装配置助手

专为中文用户设计的 OpenClaw 安装配置 Skill。配置国产 AI 模型，节省 99% API 费用。

## 功能

- 🔍 **环境检测** - 自动检测 Node.js、系统、网络环境
- 🤖 **国产模型配置** - 一键配置 DeepSeek、智谱 GLM、阿里通义千问
- ✅ **连接测试** - 测试 API 连接，验证配置正确

## 安装

```bash
npx clawhub@latest install openclaw-cn-installer
```

## 使用方法

### 1. 环境检测

```bash
node ~/.openclaw/skills/openclaw-cn-installer/check-env.js
```

检测内容：
- Node.js 版本（需要 18+）
- 操作系统兼容性
- 网络连接状态

### 2. 配置国产 AI 模型

```bash
# DeepSeek
node ~/.openclaw/skills/openclaw-cn-installer/setup-ai.js deepseek

# 智谱 GLM
node ~/.openclaw/skills/openclaw-cn-installer/setup-ai.js zhipu

# 阿里通义千问
node ~/.openclaw/skills/openclaw-cn-installer/setup-ai.js qwen
```

### 3. 测试连接

```bash
node ~/.openclaw/skills/openclaw-cn-installer/test-connection.js
```

输出示例：
```
✅ DeepSeek API: 连接成功
✅ 响应时间: 234ms
✅ 余额: ¥45.00
```

## 支持的 AI 模型

| 模型 | 提供商 | 特点 | 推荐场景 |
|------|--------|------|----------|
| DeepSeek V3 | DeepSeek | 超高性价比 ¥0.27/M tokens | 日常对话、代码生成 |
| GLM-4 | 智谱 AI | 中文能力强 | 中文内容创作 |
| Qwen 2.5 | 阿里云 | 多模态支持 | 图文混合任务 |

## 价格对比

| 模型 | 输入价格 | 输出价格 | 相比 GPT-4 |
|------|----------|----------|------------|
| DeepSeek V3 | ¥0.27/M | ¥1.08/M | **便宜 100x** |
| GLM-4 | ¥0.1/M | ¥0.1/M | 便宜 50x |
| Qwen 2.5 | ¥0.3/M | ¥0.6/M | 便宜 30x |
| GPT-4o | ¥35/M | ¥105/M | 基准 |

**省钱技巧**：用 DeepSeek 做日常任务，省 99% API 费用。

## 常见问题

### Q: 如何获取 DeepSeek API Key？
1. 访问 https://platform.deepseek.com
2. 注册账号（支持手机号）
3. 充值（最低 ¥10）
4. 创建 API Key

### Q: OpenClaw 配置文件在哪？
```
~/.openclaw/config.json       # 主配置
~/.openclaw/.env              # 环境变量（API Keys）
~/.openclaw/workspace/        # 工作目录
```

## 技术支持

- 📖 **文档**: https://docs.openclaw.ai
- 💬 **Discord**: https://discord.com/invite/clawd
- 📧 **安装服务**: ¥99 起

## 更新日志

### v1.0.1 (2026-03-20)
- 🐛 修复文档与实际功能不匹配的问题
- ✅ 移除未实现的功能说明

### v1.0.0 (2026-03-20)
- ✨ 首次发布
- ✅ 支持 DeepSeek/GLM/Qwen 配置
- ✅ 环境检测功能
- ✅ 连接测试功能

## License

MIT-0