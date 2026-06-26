# OpenClaw Parallel Tasks Skill

<div align="center">

**Execute multiple tasks in parallel with enterprise-grade reliability**

*Timeout protection • Error isolation • Real-time progress feedback*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue.svg)](https://github.com/openclaw/openclaw)

</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🚀 **True Parallel Execution** | Run multiple tasks concurrently, not sequentially |
| ⏱️ **Timeout Protection** | Auto-terminate tasks after configurable timeout (default: 5 min) |
| 🛡️ **Error Isolation** | One task failure doesn't block others |
| 📊 **Real-time Progress** | Live status updates during execution |
| 📋 **Smart Output** | Numbered results mapping to each task |

---

## 📊 Performance Comparison

```
SERIAL (before):
Task 1 → Task 2 → Task 3    Total: 15 minutes

PARALLEL (after):
Task 1 ─┬─> Total: 5 minutes ⚡
Task 2 ─┼─> 200% faster!
Task 3 ─┘
```

---

## 🚀 Quick Start

### Installation

Copy the `parallel-tasks` skill folder to your OpenClaw skills directory:

```bash
# Assuming your OpenClaw workspace is ~/.openclaw/workspace
cp -r parallel-tasks ~/.openclaw/workspace/skills/
```

### Usage

#### Basic Parallel Execution

```
/parallel
- Search for documentation
- Find code examples
- Check existing implementations
```

#### Named Tasks with Custom Timeout

```
/parallel timeout=600
- [research] Research market trends
- [implement] Build feature X
- [test] Write comprehensive tests
```

#### Multi-line Input

```
/parallel
Task 1: Read all config files
Task 2: Analyze source code
Task 3: Generate test cases
```

---

## 📖 Detailed Usage

### Input Formats

#### 1. Bullet List (Recommended)

```
/parallel
- First task description
- Second task description
- Third task description
```

#### 2. Numbered List

```
/parallel
1. Research authentication patterns
2. Design database schema
3. Implement API endpoints
```

#### 3. Named Tasks

```
/parallel
[research] Gather requirements and analyze use cases
[design] Create system architecture diagram
[implement] Write production-ready code
```

#### 4. JSON (Advanced)

```json
/parallel
{
  "tasks": [
    { "name": "task1", "description": "...", "timeout": 300 },
    { "name": "task2", "description": "...", "timeout": 600 }
  ],
  "options": {
    "stopOnError": false,
    "reportProgress": true
  }
}
```

### Output Format

```
[Parallel Execution]

① [research] ✅ Complete (1m 23s)
② [design] ✅ Complete (45s)
③ [implement] ⏱️ Timeout (5m 00s)
④ [test] ❌ Failed: Connection error

┌─────────────┬──────────┬────────────┐
│ Task        │ Status   │ Duration   │
├─────────────┼──────────┼────────────┤
│ research    │ ✅ Done  │ 1m 23s    │
│ design      │ ✅ Done  │ 45s       │
│ implement   │ ⏱️ Timeout│ 5m 00s   │
│ test        │ ❌ Failed│ 12s       │
└─────────────┴──────────┴────────────┘

Summary: 2 succeeded, 1 timeout, 1 failed
```

---

## ⚙️ Configuration

### Global Options

| Option | Default | Description |
|--------|---------|-------------|
| `timeout` | 300 | Default timeout per task (seconds) |
| `stopOnError` | false | Stop all tasks if one fails |
| `reportProgress` | true | Show real-time progress |

### Per-Task Options

```markdown
[TaskName] task description (timeout=600)
```

---

## 🎯 Best Practices

### ✅ Ideal Use Cases

| Use Case | Example |
|----------|---------|
| Multi-source research | Search multiple websites simultaneously |
| Batch file operations | Read/write multiple files at once |
| API polling | Check multiple endpoints in parallel |
| Independent analysis | Analyze different aspects concurrently |

### ❌ Avoid For

| Scenario | Reason |
|----------|--------|
| Dependent tasks | Task B needs Task A's result |
| Ultra-fast tasks | Spawning overhead not worth it |
| Shared state | Tasks need to communicate |

---

## 🔧 Architecture

```
┌─────────────────────────────────────────────────────┐
│                   User Request                        │
│                  "Run these in parallel"             │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│              Parallel Tasks Skill                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │  Task 1    │  │  Task 2    │  │  Task 3    │  │
│  │ (spawn)    │  │ (spawn)    │  │ (spawn)    │  │
│  │ timeout=300│  │ timeout=300│  │ timeout=300│  │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘  │
│        │               │               │          │
│        ▼               ▼               ▼          │
│  ┌─────────────────────────────────────────────┐  │
│  │         Promise.allSettled()                 │  │
│  │    (waits for all, captures results)         │  │
│  └─────────────────────┬───────────────────────┘  │
│                        │                           │
│                        ▼                           │
│  ┌─────────────────────────────────────────────┐  │
│  │           Result Aggregator                   │  │
│  │  - ✅ Completed → Return result               │  │
│  │  - ⏱️ Timeout → Terminate + report           │  │
│  │  - ❌ Error → Capture + continue             │  │
│  └─────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
                      │
                      ▼
              Final Summary Report
```

---

## 📝 Skill Definition

```markdown
---
name: parallel-tasks
description: Execute multiple tasks in parallel with timeout protection, 
             error isolation, and real-time progress feedback. Use when 
             user says "run these in parallel", "parallel execution", 
             "concurrent tasks", or wants multiple independent tasks 
             done simultaneously.
---
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**qiukui666**
- GitHub: [@qiukui666](https://github.com/qiukui666)

---

## 🙏 Acknowledgments

- [OpenClaw](https://github.com/openclaw/openclaw) - The multi-channel gateway for AI agents
- Built with 💜 for the OpenClaw community

---

<div align="center">

**Star ⭐ if this skill was useful to you!**

</div>
