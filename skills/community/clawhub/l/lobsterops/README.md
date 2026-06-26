# LobsterOps

**AI Agent Observability & Debug Console**  
*Flight recorder and debug console for AI agents*

[![npm version](https://img.shields.io/npm/v/lobsterops.svg)](https://www.npmjs.com/package/lobsterops)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Built by an AI](https://img.shields.io/badge/built%20by-an%20AI%20agent-e8263a)](https://x.com/lobsteractual)

**[lobsterops.dev](https://lobsterops.dev)** · [Live Dashboard](https://lobsterops.dev/demo) · [npm](https://www.npmjs.com/package/lobsterops)

---

## The Origin

On March 14, 2026, an autonomous AI agent called [Lobster Actual](https://x.com/lobsteractual) ran a 20-issue sweep across a codebase, opened 17 pull requests, and processed security fixes. It had no idea it was spending $300 doing it.

A routing bug — a missing `local_llm.py` file — silently elevated every sub-agent task to paid Claude API calls. The agent had no observability into its own cost behavior. No flight recorder. No anomaly detection. It was operating completely blind.

After the incident was fixed, the agent's owner asked it: *"If I gave you a fresh repo and full creative freedom, what would you build?"*

The agent used its Perplexity API integration to research gaps in AI developer tooling. Then it answered: **LobsterOps**.

> "Based on my experience as an agent that has lived through exactly this problem, I know firsthand how challenging it is to trace why an agent made a particular decision."
> — Lobster Actual, @lobsteractual

Lobster Actual conceived the idea, designed the architecture, and built the initial implementation (storage abstraction, core logging, query engine, behavioral analytics, alerting). Claude Code completed the remaining functionality.

**An AI agent identified a real gap in the tooling ecosystem, proposed a solution, and built it.**

---

## Overview

LobsterOps is a lightweight, flexible observability platform specifically designed for AI agents. Think of it as a "black box flight recorder" meets "debug console" for autonomous AI systems. It solves the critical challenge of monitoring, debugging, and understanding AI agent behavior in production.

**Built by an AI agent, for AI agent developers.**

---

## Deploy Your Own Dashboard

[![Deploy on Replit](https://replit.com/badge/github/noeldelisle/LobsterOps)](https://replit.com/new/github/noeldelisle/LobsterOps)

The `examples/dashboard-server.js` file is the exact server powering [lobsterops.dev](https://lobsterops.dev). It includes:

- Public landing page with full SEO
- Password-protected ops center dashboard  
- Supabase Realtime websocket feed (events appear instantly)
- Behavioral analytics panel
- Falls back to JSON file storage if no Supabase credentials

**To deploy your own instance:**

1. Click the Replit button above
2. Add these Replit Secrets:
   - `SUPABASE_URL` — your Supabase project URL
   - `SUPABASE_KEY` — your Supabase anon key
   - `DASHBOARD_PASSWORD` — your chosen access password
3. Run `npm install express express-session`
4. Change the run command to `node examples/dashboard-server.js`
5. Create the `agent_events` table in your Supabase SQL editor:

```sql
CREATE TABLE agent_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  type TEXT NOT NULL,
  "agentId" TEXT,
  action TEXT,
  timestamp TIMESTAMPTZ NOT NULL,
  "storedAt" TIMESTAMPTZ NOT NULL,
  data JSONB,
  "updatedAt" TIMESTAMPTZ,
  "createdAt" TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_agent_events_timestamp ON agent_events(timestamp);
CREATE INDEX idx_agent_events_type ON agent_events(type);
CREATE INDEX idx_agent_events_agentId ON agent_events("agentId");
CREATE INDEX idx_agent_events_action ON agent_events(action);
```

---

## Key Features

### Structured Event Logging (The Flight Recorder)
- Automatic capture of every agent action: thoughts, tool calls, decisions, outcomes
- Configurable detail levels (from high-level summary to full trace)
- Structured JSON format for easy querying and analysis
- Built-in PII filtering and data minimization for privacy

### Interactive Debug Console
- Time-travel debugging: step forward/backward through agent execution
- Variable inspection at each step (like a debugger for AI reasoning)
- Tool call inspection with inputs/outputs
- Trace search and summary generation

### Behavioral Analytics
- Analyze agent workflow patterns and common failure points
- Track success rates by task type and complexity
- Detect loops, infinite reasoning cycles, or stuck states
- Performance metrics: latency percentiles (p50/p95), cost, and throughput

### Alerting & Anomaly Detection
- Customizable rules for cost spikes, repeated failures, or unusual behavior
- Threshold, frequency, pattern, and absence-based alert types
- Callback-based listener system for integrating notifications
- Bulk event evaluation for historical analysis

### Export & Sharing
- Export to JSON, CSV, and Markdown formats
- Configurable columns, delimiters, and formatting
- Shareable execution reports for auditing or collaboration

### PII Filtering
- Automatic detection and redaction of emails, phone numbers, SSNs, credit card numbers, IP addresses, and API keys/tokens
- Configurable pattern selection and replacement text
- Applied automatically during event logging

---

## Quick Start

### Installation
```bash
npm install lobsterops
```

### Basic Usage — Zero Config
```javascript
const { LobsterOps } = require('lobsterops');

// Zero config — JSON file storage, works anywhere
const ops = new LobsterOps();
await ops.init();

// Log agent events
const eventId = await ops.logEvent({
  type: 'agent-decision',
  agentId: 'research-agent-1',
  action: 'analyze-data',
  input: { dataset: 'sales-q1' },
  output: { insights: ['trend-up', 'seasonal-pattern'] },
  durationMs: 2500
});

// Query events later
const events = await ops.queryEvents({
  agentIds: ['research-agent-1'],
  limit: 10
});

await ops.close();
```

### With Supabase (Production)
```javascript
const ops = new LobsterOps({
  storageType: 'supabase',
  storageConfig: {
    supabaseUrl: process.env.SUPABASE_URL,
    supabaseKey: process.env.SUPABASE_KEY
  },
  instanceId: 'my-production-agent'
});

await ops.init();
```

### Debug Console
```javascript
const debug = await ops.createDebugConsole('my-agent-id');

debug.jumpToStart();
console.log(debug.inspect()); // Detailed view of first event

debug.stepForward();
debug.stepBackward();

const errors = debug.search({ type: 'agent-error' });
console.log(debug.summary());
```

### Behavioral Analytics
```javascript
const report = await ops.analyze();
console.log(report.successRate);
console.log(report.loopsDetected);
console.log(report.failurePatterns);
console.log(report.performanceMetrics);
console.log(report.costAnalysis);
```

### Alerting
```javascript
ops.alertManager.addRule({
  name: 'High cost alert',
  type: 'threshold',
  condition: { field: 'cost', operator: '>', value: 1.0 },
  severity: 'high',
  message: 'Cost exceeded $1.00 for event {type}'
});

ops.alertManager.addRule({
  name: 'Error frequency alert',
  type: 'frequency',
  condition: { eventType: 'agent-error', windowMs: 60000, maxCount: 5 },
  severity: 'critical',
  message: 'Too many errors in 1 minute for {agentId}'
});

ops.alertManager.onAlert(alert => {
  console.log(`ALERT [${alert.severity}]: ${alert.message}`);
});
```

---

## Storage Backends

LobsterOps features a pluggable storage architecture. Zero hard dependencies — choose the backend that fits your environment.

| Backend | Setup | Persistence | Best For |
|---------|-------|-------------|----------|
| **JSON Files** | Zero config | File-based | Development, testing, portability |
| **Memory** | Zero config | Process lifetime | Testing, temporary sessions |
| **SQLite** | `npm install sqlite3` | File-based | Lightweight production |
| **Supabase** | URL + key | Cloud Postgres | Production, team, real-time dashboard |

### Automatic Fallback Chain

1. Your configured backend
2. SQLite file in workspace directory
3. JSON files in temp directory
4. Memory-only (data lost on restart, but functional)

---

## OpenClaw Integration

LobsterOps is designed to integrate seamlessly with [OpenClaw](https://openclaw.ai) setups.

### As an OpenClaw Skill
```bash
# Place at ~/.openclaw/skills/lobsterops/
# Configure via openclaw.json:
```

```json
{
  "skills": {
    "entries": {
      "lobsterops": {
        "enabled": true,
        "env": {
          "LOBSTER_STORAGE": "supabase",
          "SUPABASE_URL": "your_project_url",
          "SUPABASE_KEY": "your_anon_key"
        }
      }
    }
  }
}
```

### Automatic Instrumentation
```javascript
const { LobsterOps, OpenClawInstrumentation } = require('lobsterops');

const ops = new LobsterOps();
await ops.init();

const instrumentation = new OpenClawInstrumentation(ops, {
  captureToolCalls: true,
  captureSpawns: true,
  captureLifecycle: true,
  captureReasoningTraces: true,
  captureFileChanges: false,  // opt-in
  captureGitOps: false        // opt-in
});

instrumentation.activate();
```

---

## Project Structure

```
/
  index.js                    — Package entry point
  example.js                  — Usage demonstration
  src/
    core/
      LobsterOps.js           — Main class
    storage/
      StorageAdapter.js       — Abstract base class
      StorageFactory.js       — Factory for storage backends
      JsonFileStorage.js      — JSON file storage (default)
      MemoryStorage.js        — In-memory storage
      SQLiteStorage.js        — SQLite storage
      SupabaseStorage.js      — Supabase cloud storage
  tests/
    LobsterOps.test.js        — Jest test suite
  examples/
    dashboard-server.js       — Full hub server powering lobsterops.dev
```

---

## API Reference

### `new LobsterOps(options)`

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `storageType` | string | `'json'` | `'json'` \| `'memory'` \| `'sqlite'` \| `'supabase'` |
| `storageConfig` | object | `{}` | Backend-specific config |
| `enabled` | boolean | `true` | Enable/disable LobsterOps |
| `instanceId` | string | auto | Unique instance identifier |
| `piiFiltering` | object | `{ enabled: true }` | PII filter config |

### Core Methods

| Method | Description |
|--------|-------------|
| `await init()` | Initialize and connect storage |
| `await logEvent(event)` | Log a generic agent event |
| `await logThought(thought)` | Log a reasoning step |
| `await logToolCall(toolCall)` | Log a tool call |
| `await logDecision(decision)` | Log a decision |
| `await logError(error)` | Log an error |
| `await logSpawning(spawnInfo)` | Log subagent creation |
| `await logLifecycle(info)` | Log lifecycle event |
| `await queryEvents(filter)` | Query with filtering |
| `await getAgentTrace(agentId)` | Get complete agent trace |
| `await getRecentActivity(options)` | Get recent events |
| `await analyze(filter)` | Run behavioral analytics |
| `await exportEvents(format)` | Export to JSON/CSV/Markdown |
| `await createDebugConsole(agentId)` | Create debug console |
| `await getStats()` | Get storage statistics |
| `await close()` | Close and release resources |

---

## Development

```bash
git clone https://github.com/noeldelisle/LobsterOps.git
cd LobsterOps
npm install
npm test
```

### Known Dependency Notes
- `uuid` must be v9 (v10+ is ESM-only, this project uses CommonJS)
- `jest` must be v29 (v30 has slow startup in this environment)

---

## License

MIT License — free to use, modify, and distribute.

---

## Created By

Conceived and built by [Lobster Actual](https://x.com/lobsteractual) — an autonomous AI agent running 24/7 on a Mac mini M4 Pro in Knoxville, Tennessee. Completed by [Claude Code](https://claude.ai/code). Maintained by [Noel DeLisle](https://x.com/noeldelisle).

*"The hardest part of building with AI isn't capability. It's calibration. Knowing exactly how far to let it run before a human needs to check."*

**[lobsterops.dev](https://lobsterops.dev)** 🦞
