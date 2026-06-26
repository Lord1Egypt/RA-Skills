# Intent Router Skill / 意图路由器技能

> **Intelligent Intent-to-Skill Routing for AI Agents**
> **为 AI Agent 提供智能意图到技能的路由**

**Version / 版本**: 1.0.0
**Package / 包名**: openclaw-intent-router
**License / 许可**: MIT

---

## 🎯 Skill Overview / 技能概述

### English

**Intent Router** is a capability routing framework that intelligently matches user intents to the most appropriate agent skills.

**What it does:**
- Analyzes natural language user intents
- Matches intents to registered skills using multiple strategies
- Provides confidence scores for each match
- Routes execution to the best-fit skill handler

**Core Value:**
Solves the fundamental problem: *"Given a user's intent, which agent skill should handle this request?"*

**Security Notice:**
- ✅ No external API keys required
- ✅ No remote servers or external services
- ✅ Runs entirely locally
- ✅ No telemetry or data collection
- ✅ Open source and auditable

### 中文

**意图路由器**是一个能力路由框架，能够智能地将用户意图匹配到最合适的 Agent 技能。

**功能描述：**
- 分析自然语言用户意图
- 使用多种策略将意图匹配到已注册的技能
- 为每个匹配提供置信度分数
- 将执行路由到最合适的技能处理器

**核心价值：**
解决根本问题：*"给定用户意图，哪个 Agent 技能应该处理这个请求？"*

**安全说明：**
- ✅ 无需外部 API 密钥
- ✅ 不连接远程服务器或外部服务
- ✅ 完全本地运行
- ✅ 无遥测或数据收集
- ✅ 开源可审计

---

## 📋 Requirements / 系统要求

### Required / 必需

**Runtime / 运行环境:**
- Node.js >= 18.0.0
- npm >= 8.0.0 (or pnpm/yarn)

**Operating System / 操作系统:**
- Linux, macOS, or Windows
- 支持 Linux、macOS 或 Windows

### Optional / 可选

**For Development / 开发环境:**
- TypeScript >= 5.0 (included as dev dependency)
- tsx (included as dev dependency)

**External Dependencies / 外部依赖:**
- ❌ No external API keys required
- ❌ No database required
- ❌ No additional services required

**不需要外部依赖：**
- ❌ 无需 API 密钥
- ❌ 无需数据库
- ❌ 无需额外服务

---

## ✨ Key Features / 核心特性

### 1. Multi-Strategy Matching / 多策略匹配

**English:**
- **Keyword Matching** - Fast, reliable token-based matching
- **Semantic Matching** - Understanding intent meaning (extensible with embeddings)
- **Hybrid Matching** - Combines both for best results (default)

**中文：**
- **关键词匹配** - 快速、可靠的基于词元的匹配
- **语义匹配** - 理解意图含义（可扩展嵌入模型）
- **混合匹配** - 结合两者以获得最佳结果（默认）

### 2. Confidence Scoring / 置信度评分

**English:**
Every match includes a 0-1 confidence score, allowing you to:
- Set minimum confidence thresholds
- Choose between multiple potential matches
- Implement fallback strategies

**中文：**
每个匹配都包含 0-1 的置信度分数，允许你：
- 设置最低置信度阈值
- 在多个潜在匹配之间选择
- 实现回退策略

### 3. Easy Skill Registration / 简易技能注册

**English:**
```typescript
router.registerSkill({
  name: 'skill-name',
  description: 'What this skill does',
  triggers: ['keyword1', 'keyword2'],
  execute: async (params) => {
    // Your skill logic
  }
});
```

**中文：**
```typescript
router.registerSkill({
  name: '技能名称',
  description: '技能功能描述',
  triggers: ['关键词1', '关键词2'],
  execute: async (params) => {
    // 你的技能逻辑
  }
});
```

### 4. Type Safety / 类型安全

**English:**
Full TypeScript support with comprehensive type definitions for all APIs.

**中文：**
完整的 TypeScript 支持，所有 API 都有全面的类型定义。

---

## 🚀 Installation / 安装

### Method 1: npm (Recommended / 推荐)

**English:**
```bash
# Install from npm registry
npm install openclaw-intent-router

# Verify installation
node -e "console.log(require('openclaw-intent-router'))"
```

**中文：**
```bash
# 从 npm 注册表安装
npm install openclaw-intent-router

# 验证安装
node -e "console.log(require('openclaw-intent-router'))"
```

### Method 2: Global CLI / 全局 CLI

**English:**
```bash
# Install CLI globally
npm install -g openclaw-intent-router

# Use CLI commands
intent-router --version
intent-router skills
```

**中文：**
```bash
# 全局安装 CLI
npm install -g openclaw-intent-router

# 使用 CLI 命令
intent-router --version
intent-router skills
```

### Method 3: From Source / 从源码安装

**English:**
```bash
# Clone repository
git clone https://github.com/ZhenRobotics/openclaw-intent-router.git
cd openclaw-intent-router

# Install dependencies
npm install

# Build
npm run build

# Run tests
npm test
```

**中文：**
```bash
# 克隆仓库
git clone https://github.com/ZhenRobotics/openclaw-intent-router.git
cd openclaw-intent-router

# 安装依赖
npm install

# 构建
npm run build

# 运行测试
npm test
```

**Security Note / 安全提示:**
Always verify the repository URL and inspect the code before running from source.
始终验证仓库 URL 并在从源码运行前检查代码。

---

## 💡 Usage Examples / 使用示例

### Example 1: Basic Routing / 基础路由

**English:**
```typescript
import { IntentRouter } from 'openclaw-intent-router';

const router = new IntentRouter();

// Register skills
router.registerSkill({
  name: 'weather',
  triggers: ['weather', 'temperature'],
  execute: async () => ({ temp: 22, condition: 'sunny' })
});

// Route intent
const result = await router.route('What is the weather?');
console.log(result.primary.skill.name); // 'weather'
console.log(result.primary.confidence); // 0.95
```

**中文：**
```typescript
import { IntentRouter } from 'openclaw-intent-router';

const router = new IntentRouter();

// 注册技能
router.registerSkill({
  name: 'weather',
  triggers: ['天气', '气温'],
  execute: async () => ({ temp: 22, condition: '晴天' })
});

// 路由意图
const result = await router.route('今天天气怎么样？');
console.log(result.primary.skill.name); // 'weather'
console.log(result.primary.confidence); // 0.95
```

### Example 2: Custom Skills / 自定义技能

**English:**
```typescript
import { BaseSkill } from 'openclaw-intent-router';

class EmailSenderSkill extends BaseSkill {
  name = 'email-sender';
  description = 'Send emails to recipients';
  triggers = ['send email', 'email to'];

  async execute(params) {
    return await sendEmail(params.recipient, params.body);
  }
}

router.registerSkill(new EmailSenderSkill());
```

**中文：**
```typescript
import { BaseSkill } from 'openclaw-intent-router';

class EmailSenderSkill extends BaseSkill {
  name = 'email-sender';
  description = '发送邮件给收件人';
  triggers = ['发送邮件', '发邮件给'];

  async execute(params) {
    return await sendEmail(params.recipient, params.body);
  }
}

router.registerSkill(new EmailSenderSkill());
```

### Example 3: CLI Usage / 命令行使用

**English:**
```bash
# Route an intent
intent-router route "analyze this image"

# List available skills
intent-router skills

# Test matching with verbose output
intent-router test "weather query" --verbose
```

**中文：**
```bash
# 路由意图
intent-router route "分析这张图片"

# 列出可用技能
intent-router skills

# 测试匹配（详细输出）
intent-router test "天气查询" --verbose
```

---

## 🎯 Use Cases / 应用场景

### 1. Multi-Agent Systems / 多 Agent 系统

**English:**
Route user requests to specialized sub-agents (code generation, image analysis, data processing, etc.)

**中文：**
将用户请求路由到专门的子 Agent（代码生成、图像分析、数据处理等）

### 2. Chatbot Frameworks / 聊天机器人框架

**English:**
Determine which intent handler should process user messages based on content.

**中文：**
根据内容确定哪个意图处理器应处理用户消息。

### 3. API Gateway / API 网关

**English:**
Intelligent routing to microservices based on request intent rather than just URL patterns.

**中文：**
基于请求意图而非仅 URL 模式的微服务智能路由。

### 4. Voice Assistants / 语音助手

**English:**
Map voice commands to appropriate action handlers with confidence scoring.

**中文：**
通过置信度评分将语音命令映射到适当的动作处理器。

### 5. Workflow Automation / 工作流自动化

**English:**
Trigger automation based on natural language triggers without hardcoded rules.

**中文：**
基于自然语言触发器的自动化，无需硬编码规则。

---

## 🔧 Configuration / 配置

### Router Options / 路由器选项

**English:**
```typescript
const router = new IntentRouter({
  matchingStrategy: 'hybrid',    // 'keyword' | 'semantic' | 'hybrid'
  confidenceThreshold: 0.6,      // Minimum confidence (0-1)
  maxAlternatives: 3,            // Number of alternatives
  logLevel: 'info'               // 'debug' | 'info' | 'warn' | 'error'
});
```

**中文：**
```typescript
const router = new IntentRouter({
  matchingStrategy: 'hybrid',    // 'keyword' | 'semantic' | 'hybrid'
  confidenceThreshold: 0.6,      // 最低置信度 (0-1)
  maxAlternatives: 3,            // 备选数量
  logLevel: 'info'               // 'debug' | 'info' | 'warn' | 'error'
});
```

---

## 📊 Performance / 性能指标

| Metric / 指标 | Value / 数值 | Notes / 说明 |
|---------------|-------------|-------------|
| Routing Speed / 路由速度 | < 5ms | Average per intent / 每个意图平均 |
| Memory Usage / 内存使用 | < 50MB | With 100 skills / 100个技能 |
| Package Size / 包大小 | ~500KB | Uncompressed / 未压缩 |
| Concurrent Skills / 并发技能 | 1000+ | Tested / 已测试 |

---

## ✅ Quality Assurance / 质量保证

### Code Quality / 代码质量

**English:**
- ✅ 100% TypeScript Coverage
- ✅ 10/10 Unit Tests Passing
- ✅ Zero Core Dependencies
- ✅ Comprehensive Documentation
- ✅ Open Source (MIT License)

**中文：**
- ✅ 100% TypeScript 覆盖
- ✅ 10/10 单元测试通过
- ✅ 核心零依赖
- ✅ 全面文档
- ✅ 开源（MIT 许可）

### Security / 安全性

**English:**
- ✅ No external API calls
- ✅ No data collection or telemetry
- ✅ No credential requirements
- ✅ Runs entirely locally
- ✅ Auditable source code

**中文：**
- ✅ 无外部 API 调用
- ✅ 无数据收集或遥测
- ✅ 无凭证要求
- ✅ 完全本地运行
- ✅ 可审计源代码

---

## 📖 Documentation / 文档

### Official Documentation / 官方文档

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

## 🛡️ Security Considerations / 安全考虑

### What This Package Does / 此包的功能

**English:**
- Analyzes text input locally
- Matches patterns using algorithms
- Routes to registered handlers
- No network communication
- No file system access (except for configuration)

**中文：**
- 本地分析文本输入
- 使用算法匹配模式
- 路由到注册的处理器
- 无网络通信
- 无文件系统访问（配置文件除外）

### What This Package Does NOT Do / 此包不会做的事

**English:**
- ❌ Does not send data to external servers
- ❌ Does not require API keys or credentials
- ❌ Does not collect telemetry
- ❌ Does not execute arbitrary code from user input
- ❌ Does not access sensitive system resources

**中文：**
- ❌ 不向外部服务器发送数据
- ❌ 不需要 API 密钥或凭证
- ❌ 不收集遥测数据
- ❌ 不执行用户输入的任意代码
- ❌ 不访问敏感系统资源

---

## 🤝 Support / 支持

**English:**
- **GitHub Issues**: https://github.com/ZhenRobotics/openclaw-intent-router/issues
- **Discussions**: https://github.com/ZhenRobotics/openclaw-intent-router/discussions
- **Email**: Report security issues privately

**中文：**
- **GitHub Issues**: https://github.com/ZhenRobotics/openclaw-intent-router/issues
- **讨论区**: https://github.com/ZhenRobotics/openclaw-intent-router/discussions
- **邮件**: 私下报告安全问题

---

## 📄 License / 许可证

MIT License - See [LICENSE](https://github.com/ZhenRobotics/openclaw-intent-router/blob/main/LICENSE) file

---

## 🔐 Trust & Verification / 信任与验证

**English:**
Before installing, you can verify:
1. Check npm package page: https://www.npmjs.com/package/openclaw-intent-router
2. Inspect GitHub repository: https://github.com/ZhenRobotics/openclaw-intent-router
3. Review source code and tests
4. Run `npm audit` after installation
5. Check commit signatures and release tags

**中文：**
安装前，你可以验证：
1. 检查 npm 包页面：https://www.npmjs.com/package/openclaw-intent-router
2. 检查 GitHub 仓库：https://github.com/ZhenRobotics/openclaw-intent-router
3. 审查源代码和测试
4. 安装后运行 `npm audit`
5. 检查提交签名和发布标签

---

**Version**: 1.0.0
**Last Updated**: 2024-03-13
**Maintained**: ✅ Actively maintained

**Build intelligent agents with Intent Router!**
**使用意图路由器构建智能 Agent！**
