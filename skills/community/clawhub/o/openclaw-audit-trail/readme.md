# Agent Audit Trail

**AI决策的不可篡改黑匣子**
**The Immutable Black Box for AI Decisions**

追踪、审计和验证AI Agent决策，提供密码学保证。
Track, audit, and verify AI agent decisions with cryptographic guarantees.

---

## ✨ 核心功能 / Core Features

### 不可篡改性 / Immutability
- 🔗 **密码学链条** - 每个决策条目使用SHA-256加密哈希链接
  **Cryptographic chain** - Each decision entry is cryptographically linked using SHA-256
- 🔐 **篡改检测** - 任何对历史记录的修改都会立即被发现
  **Tamper detection** - Any modification to historical records is immediately detectable
- ✅ **完整性验证** - 基于哈希的验证确保数据完整性
  **Hash-based verification** - Ensures data integrity

### 全面追踪 / Comprehensive Tracking
- 📥 **输入捕获** - 记录提示、上下文和参数
  **Input capture** - Record prompts, context, and parameters
- 🧠 **推理步骤** - 追踪Agent的决策过程
  **Reasoning steps** - Track the agent's decision-making process
- 📤 **输出记录** - 存储决策、置信度和替代方案
  **Output recording** - Store decisions, confidence levels, and alternatives
- 💰 **成本追踪** - 监控Token使用和API成本
  **Cost tracking** - Monitor token usage and API costs

### 灵活性 / Flexibility
- 💾 **多存储后端** - JSON文件、SQLite、PostgreSQL（即将推出）
  **Multiple storage backends** - JSON files, SQLite, PostgreSQL (coming soon)
- 📊 **导出格式** - JSON、CSV、HTML、Markdown
  **Export formats** - JSON, CSV, HTML, Markdown
- 🔍 **查询API** - 过滤和搜索历史决策
  **Query API** - Filter and search historical decisions
- ⚡ **CLI和编程访问** - 通过命令行或集成到代码
  **CLI and programmatic access** - Via command line or code integration

### 验证 / Verification
- ✓ **链完整性检查** - 验证整个决策链未被篡改
  **Chain integrity checks** - Verify the entire decision chain hasn't been tampered
- 🔄 **自动验证** - 可选的每次写入自动验证
  **Automatic verification** - Optional auto-verify on each write
- 📋 **审计报告** - 生成符合合规要求的审计报告
  **Audit reports** - Generate compliance-ready audit reports

---

## 🚀 快速开始 / Quick Start

### 安装 / Installation

```bash
# NPM安装 / Install via NPM
npm install -g openclaw-audit-trail

# ClawHub安装 / Install via ClawHub
clawhub install openclaw-audit-trail

# 从源码 / From source
git clone https://github.com/ZhenRobotics/openclaw-audit-trail.git
cd openclaw-audit-trail
npm install
npm link
```

### 初始化审计追踪 / Initialize Audit Trail

```bash
# 为你的Agent初始化 / Initialize for your agent
audit-trail init --agent-id my-ai-agent --version 1.0.0

# 或使用短别名 / Or use short alias
aat init --agent-id my-ai-agent
```

### 记录决策 / Record Decisions

```bash
# 记录简单决策 / Record a simple decision
audit-trail record \
  --prompt "Should I approve this transaction?" \
  --decision "Approved" \
  --reasoning "Transaction amount is within limits and user is verified"

# 记录详细信息 / Record with more details
audit-trail record \
  --prompt "Classify this image" \
  --decision "cat" \
  --reasoning "Detected feline features with 95% confidence" \
  --agent-id vision-classifier
```

### 验证完整性 / Verify Integrity

```bash
# 验证审计链 / Verify the audit chain
audit-trail verify

# 预期输出 / Expected output:
# ✓ Chain integrity intact
#   Total entries: 42
#   Verified: 42
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

### TypeScript/JavaScript

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
  1250,
  // 成本（可选）/ Cost (optional)
  {
    inputTokens: 150,
    outputTokens: 50,
    totalCost: 0.003
  }
);

console.log(`Decision recorded: ${entry.id}`);

// 查询决策 / Query decisions
const decisions = await trail.query({
  startTime: Date.now() - 86400000, // Last 24 hours
  limit: 100
});

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

### 简化助手 / Simple Helper

```typescript
// 简单用例 / For simple use cases
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

### 关键组件 / Key Components

#### 1. AuditTrailChain
- 管理密码学链 / Manages cryptographic chain
- 创建和链接条目 / Creates and links entries
- 验证完整性 / Verifies integrity

#### 2. 存储后端 / Storage Backends
- **JSONStorage**: 基于文件的存储（默认）/ File-based storage (default)
- **SQLiteStorage**: 即将推出 / Coming soon
- **PostgresStorage**: 即将推出 / Coming soon

#### 3. CLI
- 命令行界面 / Command-line interface
- 轻松集成脚本和自动化 / Easy integration with scripts and automation

---

## ⚙️ 配置 / Configuration

### 环境变量 / Environment Variables

创建 `.env` 文件 / Create a `.env` file:

```bash
# Agent配置 / Agent configuration
AGENT_ID=my-ai-agent
AGENT_VERSION=1.0.0

# 存储 / Storage
STORAGE_PATH=./audit-data
STORAGE_TYPE=json

# 选项 / Options
AUTO_VERIFY=true
ENABLE_SIGNATURES=false
ENABLE_COMPRESSION=false
```

### 编程配置 / Programmatic Configuration

```typescript
const trail = new AgentAuditTrail({
  agentId: 'my-agent',
  agentVersion: '2.0.0',
  storageType: 'json',
  storagePath: './custom-path',
  enableSignatures: false,
  enableCompression: false,
  autoVerify: true
});
```

---

## 📊 数据格式 / Data Format

### 决策条目结构 / Decision Entry Structure

```json
{
  "id": "entry_1234567890_abc",
  "timestamp": 1234567890000,
  "agentId": "my-ai-agent",
  "agentVersion": "1.0.0",
  "input": {
    "prompt": "Should I approve this?",
    "context": { "user": "john", "amount": 100 },
    "parameters": { "threshold": 0.8 }
  },
  "reasoning": {
    "steps": [
      {
        "step": 1,
        "action": "analyze",
        "thought": "Checking approval criteria",
        "timestamp": 1234567890100
      }
    ],
    "model": "gpt-4",
    "temperature": 0.7
  },
  "output": {
    "decision": "approved",
    "confidence": 0.95,
    "alternatives": [
      {
        "decision": "reject",
        "confidence": 0.05,
        "reasoning": "Amount slightly high"
      }
    ]
  },
  "executionTime": 1250,
  "cost": {
    "inputTokens": 150,
    "outputTokens": 50,
    "totalCost": 0.003
  },
  "previousHash": "abcdef1234567890...",
  "hash": "fedcba0987654321..."
}
```

---

## 🔐 安全 / Security

### 密码学保证 / Cryptographic Guarantees

- **SHA-256哈希** - 工业标准加密哈希 / Industry-standard cryptographic hash
- **链式链接** - 每个条目引用前一个条目的哈希 / Chain linking with each entry referencing previous hash
- **篡改检测** - 任何修改都会破坏链条 / Any modification breaks the chain
- **创世哈希** - 唯一链标识符 / Genesis hash as unique chain identifier

### 最佳实践 / Best Practices

1. **定期备份** - 导出并安全存储审计追踪 / Regularly export and securely store audit trails
2. **定期验证** - 按计划运行验证检查 / Run verification checks on schedule
3. **安全存储** - 使用适当权限保护审计数据 / Protect audit data with appropriate permissions
4. **监控完整性** - 设置验证失败告警 / Set up alerts for verification failures

---

## 🗺️ 路线图 / Roadmap

### v1.1 (即将推出 / Coming Soon)
- [ ] SQLite 存储后端 / SQLite storage backend
- [ ] PostgreSQL 存储后端 / PostgreSQL storage backend
- [ ] 数字签名条目 / Digital signatures for entries
- [ ] 压缩支持 / Compression support
- [ ] Web仪表板 / Web dashboard

### v1.2 (未来 / Future)
- [ ] 区块链集成（Ethereum, Hyperledger）/ Blockchain integration
- [ ] 实时流API / Real-time streaming API
- [ ] 高级分析 / Advanced analytics
- [ ] 多Agent支持 / Multi-agent support
- [ ] 分布式审计追踪 / Distributed audit trails

---

## 🤝 贡献 / Contributing

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 获取指南。
We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 许可证 / License

MIT License - 查看 [LICENSE](LICENSE) 文件了解详情。
MIT License - see [LICENSE](LICENSE) file for details.

---

## 📞 支持 / Support

- **GitHub Issues**: https://github.com/ZhenRobotics/openclaw-audit-trail/issues
- **文档 / Documentation**: https://github.com/ZhenRobotics/openclaw-audit-trail/wiki
- **Email**: support@zhenrobotics.com

---

## 📊 技术规格 / Technical Specifications

- **语言 / Language**: TypeScript
- **Node.js版本 / Version**: >= 18.0.0
- **加密算法 / Crypto**: SHA-256
- **存储格式 / Storage**: JSON, SQLite (planned), PostgreSQL (planned)
- **导出格式 / Export**: JSON, CSV, HTML, Markdown
- **测试覆盖 / Test Coverage**: 100% (25/25 tests passing)

---

## 🌟 为什么选择 Agent Audit Trail？ / Why Agent Audit Trail?

### 完整透明 / Complete Transparency
每个决策都记录了完整的上下文、推理和验证。
Every decision is recorded with full context, reasoning, and verification.

### 密码学保证 / Cryptographic Guarantees
使用工业标准密码学实现防篡改日志。
Tamper-proof logging using industry-standard cryptography.

### 易于集成 / Easy Integration
简单的CLI和编程API适用于任何用例。
Simple CLI and programmatic API for any use case.

### 生产就绪 / Production Ready
经过全面测试、文档完整，随时可部署。
Thoroughly tested, documented, and ready to deploy.

### 开源 / Open Source
MIT许可证，社区驱动开发。
MIT license, community-driven development.

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
