# Memory Lucia

[![npm version](https://img.shields.io/npm/v/memory-lucia.svg)](https://www.npmjs.com/package/memory-lucia)
[![GitHub](https://img.shields.io/badge/github-memory--lucia-blue.svg)](https://github.com/wen521/memory-lucia-)
[![License](https://img.shields.io/npm/l/memory-lucia.svg)](LICENSE)

Local SQLite-based memory system for OpenClaw agents. All data stored locally with no external dependencies.

## 📦 Installation

```bash
npm install memory-lucia
```

## 🚀 Quick Start

```javascript
const MemoryAPI = require('memory-lucia');

const api = new MemoryAPI('./memory.db');
await api.init();

// Track learning progress
await api.startLearning(msgId, convId, message);
await api.updateLearningProgress(learningId, { progress: 50 });

// Record a decision
await api.recordDecision(msgId, convId, {
  summary: 'Choose SQLite over PostgreSQL',
  context: 'For local deployment',
  expectedOutcome: 'Simpler setup'
});

// Get dashboard
const dashboard = await api.getDashboard();
console.log(dashboard);
```

## ✨ Features

- 🎯 **Priority Analysis** - Analyze and store message priorities
- 📚 **Learning Tracking** - Track learning progress and milestones
- 🎯 **Decision Recording** - Record decisions with outcomes and reviews
- 📈 **Skill Evolution** - Monitor skill usage and growth
- 💾 **Version Management** - Automatic backups with rollback
- 📊 **Dashboard** - Unified view of all memory data

## 📖 Core Modules

### 1. Priority Module
Analyze and store message priorities.

```javascript
const analysis = await api.analyzePriority(message);
await api.storePriority(msgId, convId, analysis);
const highPriority = await api.getHighPriority(10);
```

### 2. Learning Module
Track learning topics and progress.

```javascript
const learning = await api.startLearning(msgId, convId, message);
await api.addMilestone(learning.id, { title: 'Completed Chapter 1' });
const active = await api.getActiveLearning(5);
```

### 3. Decision Module
Record and review decisions.

```javascript
await api.recordDecision(msgId, convId, decisionData);
await api.updateDecisionOutcome(decisionId, { actualOutcome: 'Success' });
const pending = await api.getPendingDecisions();
```

### 4. Evolution Module
Monitor skill usage.

```javascript
await api.recordSkillUsage('skill-name', 'category', 'success');
const topSkills = await api.getTopSkills(10);
```

## 📚 Documentation

- [SKILL.md](SKILL.md) - Skill description and usage
- [API Reference](references/API.md) - Complete API documentation
- [Architecture](references/ARCHITECTURE.md) - System design

## 🗄️ Database

SQLite backend with tables:
- `memory_priorities` - Priority analysis
- `memory_learning` - Learning tracking
- `memory_decisions` - Decision records
- `memory_evolution` - Skill usage

## 🔗 Links

- **npm**: https://www.npmjs.com/package/memory-lucia
- **GitHub**: https://github.com/wen521/memory-lucia-
- **Issues**: https://github.com/wen521/memory-lucia-/issues

## 📋 Version

Current: 2.5.4

## 📄 License

MIT © Chief of Staff
