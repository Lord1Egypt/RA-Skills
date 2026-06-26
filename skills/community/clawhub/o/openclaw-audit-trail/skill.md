---
name: openclaw-audit-trail
display_name: Agent Audit Trail
version: 1.0.0
author: ZhenStaff
category: ai-tools
license: MIT-0
description: The Immutable Black Box for AI Decisions - Track, audit, and verify AI agent decisions with cryptographic guarantees
tags: [ai-audit, agent-tracking, decision-trail, immutable-log, ai-transparency, audit-trail, cryptographic-verification, ai-governance]
repository: https://github.com/ZhenRobotics/openclaw-audit-trail
homepage: https://github.com/ZhenRobotics/openclaw-audit-trail
documentation: https://github.com/ZhenRobotics/openclaw-audit-trail#readme
---

# Agent Audit Trail

**AI决策的不可篡改黑匣子**
**The Immutable Black Box for AI Decisions**

追踪、审计和验证AI Agent决策，提供密码学保证。
Track, audit, and verify AI agent decisions with cryptographic guarantees.

---

## 🎯 概述 / Overview

Agent Audit Trail 是一个为AI决策提供密码学保证的审计追踪工具，可以记录、验证和审计AI Agent的每一个决策过程。

Agent Audit Trail is an audit trail system that provides cryptographic guarantees for AI decisions, enabling recording, verification, and auditing of every AI Agent decision process.

### 核心特性 / Core Features

- 🔗 **密码学链条** - SHA-256哈希链确保不可篡改 / Cryptographic chain with SHA-256 hashing ensures immutability
- 📝 **完整记录** - 捕获输入、推理、输出全过程 / Complete recording of input, reasoning, and output
- ✅ **完整性验证** - 自动检测任何篡改行为 / Integrity verification detects any tampering
- 📊 **多格式导出** - JSON、CSV、HTML、Markdown / Multiple export formats
- ⚡ **CLI和API** - 命令行和编程接口双重支持 / Both CLI and programmatic interfaces
- 🔐 **本地存储** - 所有数据存储在本地，无外部依赖 / All data stored locally, no external dependencies

---

## 📦 安装 / Installation

### NPM (推荐 / Recommended)

```bash
# 全局安装 / Install globally
npm install -g openclaw-audit-trail

# 或项目依赖 / Or as project dependency
npm install openclaw-audit-trail
```

### ClawHub

```bash
clawhub install openclaw-audit-trail
```

### 从源码 / From Source

```bash
git clone https://github.com/ZhenRobotics/openclaw-audit-trail.git
cd openclaw-audit-trail
npm install
npm link
```

---

## 🚀 快速开始 / Quick Start

### 初始化 / Initialize

```bash
# 初始化审计追踪 / Initialize audit trail
audit-trail init --agent-id my-ai-agent --version 1.0.0

# 或使用别名 / Or use alias
aat init --agent-id my-agent
```

### 记录决策 / Record Decisions

```bash
# 简单记录 / Simple recording
audit-trail record \
  --prompt "Should I approve this loan?" \
  --decision "Approved" \
  --reasoning "Credit score 750, income verified, debt ratio acceptable"

# 带更多细节 / With more details
audit-trail record \
  --prompt "Classify this image" \
  --decision "cat" \
  --reasoning "Detected feline features with 95% confidence" \
  --agent-id vision-classifier
```

### 验证完整性 / Verify Integrity

```bash
# 验证审计链 / Verify audit chain
audit-trail verify

# 预期输出 / Expected output:
# ✓ Chain integrity intact
#   Total entries: 42
#   Verified: 42/42
```

### 列出决策 / List Decisions

```bash
# 列出最近的决策 / List recent decisions
audit-trail list --limit 10

# 按时间过滤 / Filter by time
audit-trail list --start 1700000000 --end 1700100000
```

### 导出审计追踪 / Export Audit Trail

```bash
# 导出为JSON / Export as JSON
audit-trail export --output audit-report.json --format json

# 导出为HTML报告 / Export as HTML report
audit-trail export --output audit-report.html --format html --include-reasoning

# 导出为CSV / Export as CSV
audit-trail export --output audit-data.csv --format csv
```

---

## 💻 编程使用 / Programmatic Usage

### TypeScript/JavaScript API

```typescript
import { AgentAuditTrail } from 'openclaw-audit-trail';

// 初始化 / Initialize
const trail = new AgentAuditTrail({
  agentId: 'my-ai-agent',
  agentVersion: '1.0.0',
  storagePath: './audit-data'
});

await trail.initialize();

// 记录决策 / Record a decision
const entry = await trail.recordDecision(
  // 输入 / Input
  {
    prompt: 'Should I send this email?',
    context: { urgency: 'high', recipient: 'user@example.com' }
  },
  // 推理 / Reasoning
  {
    steps: [
      {
        step: 1,
        action: 'analyze',
        thought: 'Checking email content for sensitive information',
        timestamp: Date.now()
      },
      {
        step: 2,
        action: 'decide',
        thought: 'No sensitive data detected, urgency is high',
        timestamp: Date.now()
      }
    ],
    model: 'gpt-4',
    temperature: 0.7
  },
  // 输出 / Output
  {
    decision: 'send',
    confidence: 0.95,
    alternatives: [
      { decision: 'delay', confidence: 0.05, reasoning: 'Wait for manual review' }
    ]
  },
  // 执行时间 / Execution time
  1250
);

console.log(`Decision recorded: ${entry.id}`);

// 验证完整性 / Verify integrity
const verification = trail.verify();
if (!verification.valid) {
  console.error('Chain compromised!', verification.errors);
}

// 导出 / Export
const htmlReport = await trail.export({
  format: 'html',
  includeMetadata: true,
  includeReasoning: true
});

await trail.close();
```

### 简化版本 / Simplified Version

```typescript
// 用于简单用例 / For simple use cases
const entry = await trail.recordSimple(
  'What is 2+2?',
  '4',
  'Basic arithmetic calculation',
  50 // execution time in ms
);
```

---

## 🎯 使用场景 / Use Cases

### 1. AI安全与合规 / AI Safety & Compliance

**场景 / Scenario**: 金融机构使用AI进行贷款审批 / Financial institution using AI for loan approvals

```typescript
await trail.recordDecision(
  {
    prompt: 'Approve loan application #12345',
    context: { creditScore: 720, income: 80000, debtRatio: 0.3 }
  },
  {
    steps: [
      { step: 1, action: 'evaluate', thought: 'Checking credit score threshold' },
      { step: 2, action: 'analyze', thought: 'Debt-to-income ratio acceptable' },
      { step: 3, action: 'decide', thought: 'All criteria met for approval' }
    ]
  },
  {
    decision: 'approved',
    confidence: 0.92,
    metadata: { loanAmount: 50000, interestRate: 0.045 }
  },
  2300
);
```

**好处 / Benefits**: 完整的监管合规审计追踪，能够向客户解释决策 / Full audit trail for regulatory compliance, ability to explain decisions to customers

### 2. 自主系统 / Autonomous Systems

**场景 / Scenario**: 自动驾驶汽车决策日志 / Self-driving car decision logging

```typescript
await trail.recordDecision(
  {
    prompt: 'Pedestrian detected crossing street',
    context: { speed: 35, distance: 50, weather: 'clear' }
  },
  {
    steps: [
      { step: 1, action: 'detect', thought: 'Pedestrian at 50m ahead' },
      { step: 2, action: 'calculate', thought: 'Stopping distance: 35m' },
      { step: 3, action: 'decide', thought: 'Initiate emergency brake' }
    ]
  },
  { decision: 'emergency_brake', confidence: 1.0 },
  120
);
```

**好处 / Benefits**: 事故调查黑匣子记录，安全分析 / Black box recording for accident investigation, safety analysis

### 3. 内容审核 / Content Moderation

**场景 / Scenario**: AI审核用户生成内容 / AI moderating user-generated content

```typescript
await trail.recordDecision(
  {
    prompt: 'Moderate comment: "..."',
    context: { userId: 'user123', platform: 'forum' }
  },
  {
    steps: [
      { step: 1, action: 'scan', thought: 'Checking for hate speech patterns' },
      { step: 2, action: 'analyze', thought: 'Detected potential violation' }
    ]
  },
  {
    decision: 'flag_for_review',
    confidence: 0.75,
    metadata: { violationType: 'potential_hate_speech' }
  },
  850
);
```

**好处 / Benefits**: 用户透明度，政策执行的证据 / Transparency for users, evidence for policy enforcement

### 4. 研究与开发 / Research & Development

**场景 / Scenario**: 调试AI Agent行为 / Debugging AI agent behavior

```bash
# 查找所有失败的决策 / Find all failed decisions
audit-trail list --limit 100 | grep "failed"

# 导出上周的决策用于分析 / Export last week's decisions for analysis
audit-trail export --output weekly-decisions.json \
  --start $(date -d '7 days ago' +%s) \
  --format json --include-reasoning

# 验证未发生篡改 / Verify no tampering occurred
audit-trail verify
```

**好处 / Benefits**: 可重现的实验，决策模式分析 / Reproducible experiments, decision pattern analysis

---

## 🏗️ 架构 / Architecture

```
┌─────────────────────────────────────────┐
│           CLI / API Layer               │
│   (User Interface & Integration)        │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│      AgentAuditTrail (Main API)         │
│  - Record decisions                     │
│  - Query & export                       │
│  - Verification                         │
└──────────────┬──────────────────────────┘
               │
    ┌──────────┴──────────┐
    │                     │
┌───▼──────────┐  ┌──────▼─────────┐
│ AuditChain   │  │ Storage Layer  │
│              │  │                │
│ - Hash chain │  │ - JSON files   │
│ - Integrity  │  │ - SQLite       │
│ - Verify     │  │ - PostgreSQL   │
└──────────────┘  └────────────────┘
```

---

## 🔐 安全性 / Security

### 密码学保证 / Cryptographic Guarantees

- **SHA-256哈希** - 工业标准加密哈希 / Industry-standard cryptographic hash
- **链式关联** - 每个条目引用前一个哈希 / Each entry references previous hash
- **篡改检测** - 任何修改立即可检测 / Any modification is immediately detectable
- **创世哈希** - 唯一链标识符 / Unique chain identifier

### 数据隐私 / Data Privacy

- ✅ **本地存储** - 所有数据存储在本地文件系统 / All data stored locally
- ✅ **无外部传输** - 不连接任何外部服务器 / No external server connections
- ✅ **用户控制** - 完全由用户控制数据 / User has full control of data
- ✅ **可删除** - 用户可随时删除审计数据 / Users can delete audit data anytime

---

## 📊 技术规格 / Technical Specifications

- **语言 / Language**: TypeScript
- **Node.js版本 / Version**: >= 18.0.0
- **加密算法 / Crypto**: SHA-256
- **存储格式 / Storage**: JSON (SQLite, PostgreSQL planned)
- **导出格式 / Export**: JSON, CSV, HTML, Markdown
- **测试覆盖 / Test Coverage**: 100% (25/25 tests passing)

---

## 📝 CLI 命令参考 / CLI Command Reference

### `init` - 初始化 / Initialize
```bash
audit-trail init --agent-id <id> [--version <ver>] [--storage-path <path>]
```

### `record` - 记录决策 / Record Decision
```bash
audit-trail record \
  --prompt <text> \
  --decision <text> \
  --reasoning <text> \
  [--agent-id <id>]
```

### `verify` - 验证完整性 / Verify Integrity
```bash
audit-trail verify [--agent-id <id>]
```

### `list` - 列出决策 / List Decisions
```bash
audit-trail list [--limit <n>] [--start <timestamp>] [--end <timestamp>]
```

### `export` - 导出数据 / Export Data
```bash
audit-trail export \
  --output <file> \
  --format <json|csv|html|markdown> \
  [--include-reasoning]
```

### `info` - 显示信息 / Show Information
```bash
audit-trail info [--agent-id <id>]
```

---

## 🗺️ 路线图 / Roadmap

### v1.1 (即将推出 / Coming Soon)
- [ ] SQLite 存储后端 / SQLite storage backend
- [ ] PostgreSQL 存储后端 / PostgreSQL storage backend
- [ ] 数字签名支持 / Digital signature support
- [ ] 压缩支持 / Compression support
- [ ] Web 仪表板 / Web dashboard

### v1.2 (未来 / Future)
- [ ] 区块链集成 / Blockchain integration
- [ ] 实时流API / Real-time streaming API
- [ ] 高级分析 / Advanced analytics
- [ ] 多Agent支持 / Multi-agent support

---

## 🐛 常见问题 / FAQ

### Q: 如何确保审计数据不被篡改？ / How to ensure audit data cannot be tampered with?

**A**: 使用密码学哈希链。每个条目包含前一条目的SHA-256哈希，任何修改都会破坏链条。定期运行 `audit-trail verify` 检测篡改。

**A**: Use cryptographic hash chain. Each entry contains the SHA-256 hash of the previous entry. Any modification breaks the chain. Run `audit-trail verify` regularly to detect tampering.

### Q: 审计数据存储在哪里？ / Where is audit data stored?

**A**: 默认存储在 `./audit-data` 目录。可通过 `--storage-path` 参数或环境变量 `STORAGE_PATH` 自定义。

**A**: Stored in `./audit-data` directory by default. Customizable via `--storage-path` parameter or `STORAGE_PATH` environment variable.

### Q: 支持分布式审计吗？ / Does it support distributed auditing?

**A**: 当前版本(v1.0.0)支持本地文件存储。未来版本将支持SQLite、PostgreSQL和区块链集成。

**A**: Current version (v1.0.0) supports local file storage. Future versions will support SQLite, PostgreSQL, and blockchain integration.

---

## 📞 支持 / Support

- **GitHub Issues**: https://github.com/ZhenRobotics/openclaw-audit-trail/issues
- **文档 / Documentation**: https://github.com/ZhenRobotics/openclaw-audit-trail#readme
- **Email**: support@zhenrobotics.com

---

## 📄 许可证 / License

MIT License - 查看 [LICENSE](https://github.com/ZhenRobotics/openclaw-audit-trail/blob/main/LICENSE) 文件了解详情。

MIT License - see [LICENSE](https://github.com/ZhenRobotics/openclaw-audit-trail/blob/main/LICENSE) file for details.

---

**以透明为理念构建。让AI决策可审计、可信任。**
**Built with transparency in mind. Make AI decisions auditable and trustworthy.**

🔗 **GitHub**: https://github.com/ZhenRobotics/openclaw-audit-trail
📦 **NPM**: https://www.npmjs.com/package/openclaw-audit-trail
🦅 **ClawHub**: https://clawhub.ai/ZhenStaff/openclaw-audit-trail

---

**版本 / Version**: 1.0.0
**最后更新 / Last Updated**: 2026-03-13
**状态 / Status**: ✅ Production Ready
