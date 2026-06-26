# Intent Router / 意图路由器

> **The Search Layer for Agent Capabilities**
> **Agent 能力的搜索层**

**Version / 版本**: 1.0.0
**Package / 包名**: openclaw-intent-router
**License / 许可**: MIT

---

## 🎯 English Description

### What is Intent Router?

Intent Router is an intelligent routing system that analyzes natural language intents and matches them to the most appropriate agent skills and capabilities.

**Think of it as a smart dispatcher** - it understands what users want to do and routes requests to the right skill handler with confidence scoring.

### Key Features

- **🎯 Intelligent Matching** - Automatically routes intents to best-fit skills
- **📊 Confidence Scoring** - Every match includes a 0-1 confidence score
- **🔧 Multiple Strategies** - Keyword, semantic, and hybrid matching
- **💡 Easy to Extend** - Simple skill registration interface
- **⚡ Fast & Lightweight** - Optimized for performance (< 500KB)
- **🔐 Type Safe** - Full TypeScript support
- **🛡️ Secure** - No external dependencies, runs entirely locally

### Quick Example

```typescript
import { IntentRouter } from 'openclaw-intent-router';

const router = new IntentRouter();

// Register a skill
router.registerSkill({
  name: 'weather-lookup',
  description: 'Get weather information',
  triggers: ['weather', 'temperature', 'forecast'],
  execute: async (params) => {
    return await getWeather(params.location);
  }
});

// Route an intent
const result = await router.route('What is the weather in Paris?');
// => { skill: 'weather-lookup', confidence: 0.95 }
```

### Use Cases

- 🤖 **Multi-Agent Systems** - Route to specialized sub-agents
- 💬 **Chatbots** - Determine intent handlers
- 🌐 **API Gateway** - Intelligent service routing
- 🗣️ **Voice Assistants** - Command to action mapping
- ⚙️ **Workflow Automation** - Natural language triggers

### Installation

```bash
npm install openclaw-intent-router
```

### Requirements

- **Node.js**: >= 18.0.0
- **npm**: >= 8.0.0
- **No external API keys required**
- **No database required**
- **Runs entirely locally**

---

## 🎯 中文描述

### 什么是意图路由器？

意图路由器是一个智能路由系统，能够分析自然语言意图并将其匹配到最合适的 Agent 技能和能力。

**可以把它看作是一个智能调度员** - 它理解用户想做什么，并通过置信度评分将请求路由到正确的技能处理器。

### 核心功能

- **🎯 智能匹配** - 自动将意图路由到最佳技能
- **📊 置信度评分** - 每个匹配都包含 0-1 的置信度分数
- **🔧 多种策略** - 关键词、语义和混合匹配
- **💡 易于扩展** - 简单的技能注册接口
- **⚡ 快速轻量** - 性能优化（< 500KB）
- **🔐 类型安全** - 完整的 TypeScript 支持
- **🛡️ 安全** - 无外部依赖，完全本地运行

### 快速示例

```typescript
import { IntentRouter } from 'openclaw-intent-router';

const router = new IntentRouter();

// 注册技能
router.registerSkill({
  name: 'weather-lookup',
  description: '获取天气信息',
  triggers: ['天气', '气温', '温度', '预报'],
  execute: async (params) => {
    return await getWeather(params.location);
  }
});

// 路由意图
const result = await router.route('巴黎的天气怎么样？');
// => { skill: 'weather-lookup', confidence: 0.95 }
```

### 使用场景

- 🤖 **多 Agent 系统** - 路由到专门的子 Agent
- 💬 **聊天机器人** - 确定意图处理器
- 🌐 **API 网关** - 智能服务路由
- 🗣️ **语音助手** - 命令到动作映射
- ⚙️ **工作流自动化** - 自然语言触发器

### 安装

```bash
npm install openclaw-intent-router
```

### 系统要求

- **Node.js**: >= 18.0.0
- **npm**: >= 8.0.0
- **无需外部 API 密钥**
- **无需数据库**
- **完全本地运行**

---

## 🔐 Security / 安全性

### What This Package Does / 功能说明

**English:**
- ✅ Analyzes text locally using pattern matching
- ✅ Routes to registered handlers
- ✅ Provides confidence scores
- ❌ No external API calls
- ❌ No data collection
- ❌ No credentials required

**中文：**
- ✅ 使用模式匹配本地分析文本
- ✅ 路由到注册的处理器
- ✅ 提供置信度分数
- ❌ 无外部 API 调用
- ❌ 无数据收集
- ❌ 无需凭证

### Verification / 验证

**English:**
Before installing, verify:
1. npm package: https://www.npmjs.com/package/openclaw-intent-router
2. GitHub repo: https://github.com/ZhenRobotics/openclaw-intent-router
3. Run `npm audit` after installation

**中文：**
安装前验证：
1. npm 包：https://www.npmjs.com/package/openclaw-intent-router
2. GitHub 仓库：https://github.com/ZhenRobotics/openclaw-intent-router
3. 安装后运行 `npm audit`

---

## 📊 Technical Details / 技术细节

### Architecture / 架构

```
User Intent → Intent Analyzer → Skill Matcher → Skill Execution
用户意图 → 意图分析器 → 技能匹配器 → 技能执行
```

### Performance / 性能

**English:**
- ⚡ Fast routing: < 5ms average
- 📦 Lightweight: < 500KB package size
- 🔄 Scalable: Handles 1000+ skills efficiently
- 💾 Low memory: < 50MB with 100 skills

**中文：**
- ⚡ 快速路由：平均 < 5ms
- 📦 轻量级：包大小 < 500KB
- 🔄 可扩展：高效处理 1000+ 个技能
- 💾 低内存：100 个技能 < 50MB

### Quality / 质量

**English:**
- ✅ 100% TypeScript
- ✅ 10/10 Tests Passing
- ✅ Zero Core Dependencies
- ✅ Full Type Definitions
- ✅ Open Source (MIT)

**中文：**
- ✅ 100% TypeScript
- ✅ 10/10 测试通过
- ✅ 核心零依赖
- ✅ 完整类型定义
- ✅ 开源（MIT）

---

## 📚 Documentation / 文档

### Links / 链接

**English:**
- **GitHub**: https://github.com/ZhenRobotics/openclaw-intent-router
- **npm**: https://www.npmjs.com/package/openclaw-intent-router
- **Quick Start**: [QUICKSTART.md](https://github.com/ZhenRobotics/openclaw-intent-router/blob/main/QUICKSTART.md)
- **Examples**: [examples/](https://github.com/ZhenRobotics/openclaw-intent-router/tree/main/examples)

**中文：**
- **GitHub**: https://github.com/ZhenRobotics/openclaw-intent-router
- **npm**: https://www.npmjs.com/package/openclaw-intent-router
- **快速开始**: [QUICKSTART.md](https://github.com/ZhenRobotics/openclaw-intent-router/blob/main/QUICKSTART.md)
- **示例**: [examples/](https://github.com/ZhenRobotics/openclaw-intent-router/tree/main/examples)

---

## 🚀 Quick Start / 快速开始

### Installation / 安装

```bash
npm install openclaw-intent-router
```

### Basic Usage / 基本使用

```typescript
import { IntentRouter } from 'openclaw-intent-router';

const router = new IntentRouter();

// Register skills / 注册技能
router.registerSkill({
  name: 'calculator',
  triggers: ['calculate', 'compute', 'math'],
  execute: async (params) => ({ result: 42 })
});

// Route intent / 路由意图
const result = await router.route('calculate 2 + 2');
console.log(result.primary.skill.name); // 'calculator'
```

### CLI Usage / CLI 使用

```bash
# Global install / 全局安装
npm install -g openclaw-intent-router

# Use CLI / 使用 CLI
intent-router route "your query here"
intent-router skills
```

---

## 📄 License / 许可证

MIT License

---

## 👥 Author / 作者

**justin** - OpenClaw Project

---

## 🤝 Support / 支持

**English:**
- **Issues**: https://github.com/ZhenRobotics/openclaw-intent-router/issues
- **Discussions**: https://github.com/ZhenRobotics/openclaw-intent-router/discussions

**中文：**
- **问题反馈**: https://github.com/ZhenRobotics/openclaw-intent-router/issues
- **讨论区**: https://github.com/ZhenRobotics/openclaw-intent-router/discussions

---

**Version**: 1.0.0
**Last Updated**: 2024-03-13

**Build smarter agents with Intent Router!**
**用意图路由器构建更智能的 Agent！**
