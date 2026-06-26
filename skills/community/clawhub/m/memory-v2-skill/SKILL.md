---
name: memory-lucia
version: 2.5.4
description: |
  Memory Lucia - Local SQLite-based memory system for OpenClaw agents.
  Features: (1) Priority analysis and tracking, (2) Learning progress with milestones,
  (3) Decision recording with review scheduling, (4) Skill evolution monitoring,
  (5) Local text search across all memory tables, (6) Automatic database backups.
  All data stored locally in SQLite database. No external API calls.
---

# Memory V2 Skill

## Overview

Memory V2 is a comprehensive memory management system for OpenClaw agents, providing persistent storage and intelligent analysis capabilities.

## Features

- **Priority Analysis**: Analyze and store message priorities with reasoning
- **Learning Tracking**: Track learning progress, milestones, and completion
- **Decision Recording**: Record decisions with context, outcomes, and scheduled reviews
- **Skill Evolution**: Monitor skill usage patterns and growth over time
- **Version Management**: Backup and rollback capabilities
- **Dashboard**: Unified view of all memory data

## Installation

```bash
# Install dependencies
npm install sqlite3

# Initialize database
node scripts/init-memory.js
```

## Quick Start

```javascript
const MemoryAPI = require('./api');

const api = new MemoryAPI('./memory-v2.db');
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
```

## Core Modules

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

## API Reference

See `references/API.md` for complete API documentation.

## Database Schema

SQLite database with tables:
- `memory_priorities` - Priority analysis
- `memory_learning` - Learning tracking
- `memory_decisions` - Decision records
- `memory_evolution` - Skill usage

## Migration

From V1 to V2:
```bash
node migrations/v1-to-v2.js old-memory.db
```

## Version

Current: 2.0.2

## License

MIT
