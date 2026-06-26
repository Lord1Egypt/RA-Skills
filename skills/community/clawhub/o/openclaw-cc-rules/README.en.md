# CC Rules — OpenClaw Programming Workflow Skill

> Structured software development workflow for OpenClaw. Inspired by best practices from leading AI coding tools.

**中文** | English

---

## What Is This

CC Rules is an OpenClaw Skill that defines a comprehensive programming workflow: **Explore → Plan → Execute → Verify**.

When your OpenClaw detects a coding scenario, it follows structured rules instead of randomly modifying files.

## Core Features

### 🧭 Plan Mode
Non-trivial tasks require exploration and a plan before writing code.

### ✅ Task Tracking
Auto-generates task lists for complex work, with real-time status updates.

### 🔍 Read-Only Exploration
Forces read-only mode when understanding code — no file modifications allowed.

### 🛡️ Git Safety Protocol
Blocks destructive commands (`--force`, `reset --hard`, `--no-verify`) unless explicitly requested.

### 📋 Multi-File Strategy
Changes follow dependency order: base modules → business logic → config.

## Installation

```bash
cd ~/.openclaw/skills/
git clone https://github.com/badxtdss/openclaw-cc-rules.git cc-rules
```

## License

MIT
