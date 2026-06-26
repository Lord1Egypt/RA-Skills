# Agent Orchestrator 🐙

**Multi-agent collaboration and task orchestration for OpenClaw.**

When a single agent isn't enough — orchestrate a team.

## Installation

```bash
clawhub install agent-orchestrator
```

## Quick Start

### Basic Usage

```
Orchestrate this: Research the top 5 AI frameworks and compare their features
```

The orchestrator will:
1. Decompose into sub-tasks (one per framework)
2. Spawn 5 sub-agents
3. Each agent researches one framework
4. Synthesize comparison report

### Command Line

```bash
node scripts/orchestrate.js "Your complex task" --mode parallel --synthesis consolidate
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--agents <n>` | auto | Number of sub-agents |
| `--mode <mode>` | parallel | Execution mode: parallel\|sequential\|hybrid |
| `--timeout <sec>` | 300 | Timeout per sub-agent |
| `--synthesis <type>` | consolidate | Synthesis type: merge\|summarize\|compare\|consolidate |
| `--verbose` | false | Show detailed progress |

## Use Cases

1. **Research Projects** - Different agents research different aspects
2. **Code Reviews** - Multiple agents review different files/modules
3. **Data Analysis** - Parallel analysis of different datasets
4. **Content Creation** - Agents write different sections, then synthesize
5. **Testing** - Parallel test execution across scenarios

## How It Works

```
┌─────────────────┐
│   Orchestrator  │
│     (Main)      │
└────────┬────────┘
         │
    ┌────┴────┬────────────┐
    │         │            │
┌───▼───┐ ┌──▼────┐  ┌────▼────┐
│Agent 1│ │Agent 2│  │Agent 3  │
│ Task A│ │ Task B│  │ Task C  │
└───┬───┘ └───┬───┘  └────┬────┘
    │         │            │
    └─────────┴────────────┘
              │
         ┌────▼────┐
         │Synthesis│
         │ Result  │
         └─────────┘
```

## License

MIT
