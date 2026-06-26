# lee-cli Skill for Claude Code

> 🤖 个人AI助手CLI工具集 - 天气笑话、新闻日报、工作总结、AI学习、智能待办

## ✨ 功能特性

### 🌤️ 天气冷笑话
结合实时天气生成创意笑话，让你的一天从微笑开始

### 📰 新闻日报
聚合今日科技、财经、国际热点，快速了解大事

### 📝 工作总结
自动分析 Claude Code 活动记录，生成每日工作总结

### 🎓 AI学习资源
推荐高质量 AI 学习资料（LLM、Agent、MCP、Prompt Engineering）

### ✅ 智能待办
结合日历和工作情况，生成智能化待办清单

## 🚀 快速开始

### 前置要求

1. 安装 lee-cli 命令行工具
2. 配置 `ANTHROPIC_API_KEY` 环境变量

### 安装

```bash
# 通过 Claude Code 安装
/skills install lee-cli
```

## 📖 使用方法

### 在对话中自然调用

- "讲个笑话"
- "今天有什么新闻？"
- "总结下我今天的工作"
- "推荐一些 AI 学习资源"
- "明天我要做什么？"

### 命令行直接使用

```bash
# 天气笑话
lee-cli joke

# 新闻日报
lee-cli news --categories 科技,财经,国际

# 工作总结
lee-cli summary

# 学习资源
lee-cli learn --topic llm

# 智能待办
lee-cli todo --days 3

# 一键全功能
lee-cli all
```

## 🎯 使用场景

- ☀️ **早晨开始工作** - 天气笑话 + 新闻日报 + 待办清单
- 🌆 **下班前回顾** - 工作总结 + 明日待办
- 📚 **学习时段** - AI 学习资源推荐
- 🎪 **娱乐时刻** - 天气冷笑话调节心情

## 🛠️ 技术栈

- Node.js + Commander.js - CLI 框架
- Anthropic Claude API - AI 生成能力
- Chalk + Boxen - 终端美化
- Ora - 加载动画

## 📦 相关链接

- [lee-cli GitHub 仓库](https://github.com/yourusername/lee-cli)
- [完整文档](./SKILL.md)

## 👨‍💻 作者

李池明

## 📄 License

MIT

---

Made with ❤️ by Claude Code
