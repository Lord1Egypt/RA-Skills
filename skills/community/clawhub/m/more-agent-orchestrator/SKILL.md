---
name: agent-orchestrator
version: 1.0.0
description: Multi-agent collaboration and task orchestration. Decompose complex tasks, spawn sub-agents, coordinate execution, and synthesize results.
author: lcp14262
license: MIT-0
repository: https://github.com/lcp14262/agent-orchestrator
---

# Agent Orchestrator 🐙

**Multi-agent collaboration and task orchestration for OpenClaw.**

When a single agent isn't enough — orchestrate a team.

## What It Does

**Task Decomposition:**
- Analyzes complex tasks
- Breaks them into independent sub-tasks
- Identifies dependencies and parallelization opportunities

**Agent Coordination:**
- Spawns sub-agents with specific instructions
- Manages concurrent execution
- Handles inter-agent communication
- Monitors progress and health

**Result Synthesis:**
- Collects results from all sub-agents
- Resolves conflicts and inconsistencies
- Synthesizes final deliverable
- Provides execution summary

## When to Use

**Trigger Phrases:**
- "Break this down and have multiple agents work on it"
- "Coordinate several agents to..."
- "Parallelize this task"
- "Have agents collaborate on..."
- "Orchestrate a team to..."
- "Decompose and distribute..."

**Use Cases:**
1. **Research Projects** - Different agents research different aspects
2. **Code Reviews** - Multiple agents review different files/modules
3. **Data Analysis** - Parallel analysis of different datasets
4. **Content Creation** - Agents write different sections, then synthesize
5. **Testing** - Parallel test execution across scenarios
6. **Complex Workflows** - Multi-step processes with dependencies

## Quick Start

### Basic Usage

```
Orchestrate this: Research the top 5 AI frameworks and compare their features, performance, and community support.
```

The orchestrator will:
1. Decompose into sub-tasks (one per framework)
2. Spawn 5 sub-agents
3. Each agent researches one framework
4. Synthesize comparison report

### Advanced Usage

```
Orchestrate with options:
- Task: Analyze our Q4 sales data
- Agents: 4 (by region: North/South/East/West)
- Parallel: true
- Synthesis: consolidated_report
```

## Architecture

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

## Configuration

### Task Decomposition Strategy

| Strategy | Description | Best For |
|----------|-------------|----------|
| `parallel` | All sub-tasks run concurrently | Independent tasks |
| `sequential` | Tasks run one after another | Dependent tasks |
| `hybrid` | Mix of parallel and sequential | Complex workflows |

### Agent Allocation

| Mode | Description | Use Case |
|------|-------------|----------|
| `auto` | Orchestrator decides agent count | General purpose |
| `fixed` | Specific number of agents | Resource-constrained |
| `per_task` | One agent per sub-task | Maximum parallelization |

### Synthesis Options

| Option | Description |
|--------|-------------|
| `merge` | Combine all results as-is |
| `summarize` | Generate executive summary |
| `compare` | Highlight differences and similarities |
| `consolidate` | Merge with conflict resolution |

## Examples

### Example 1: Market Research

```
Task: Research the competitive landscape for project management software

Decomposition:
- Agent 1: Analyze Asana features and pricing
- Agent 2: Analyze Monday.com features and pricing
- Agent 3: Analyze Notion features and pricing
- Agent 4: Analyze ClickUp features and pricing
- Agent 5: Analyze emerging competitors

Synthesis: Comparative analysis report with recommendations
```

### Example 2: Code Review

```
Task: Review the entire codebase for security vulnerabilities

Decomposition:
- Agent 1: Review authentication module
- Agent 2: Review API endpoints
- Agent 3: Review database queries
- Agent 4: Review file handling
- Agent 5: Review third-party dependencies

Synthesis: Security audit report with prioritized fixes
```

### Example 3: Content Creation

```
Task: Write a comprehensive guide to OpenClaw skills

Decomposition:
- Agent 1: Introduction and setup
- Agent 2: Basic skill structure
- Agent 3: Advanced patterns
- Agent 4: Best practices
- Agent 5: Troubleshooting

Synthesis: Complete guide with consistent voice and formatting
```

## Implementation Details

### Task Decomposition Algorithm

1. **Analyze** the main task for scope and complexity
2. **Identify** natural breakpoints and independent components
3. **Estimate** effort for each component
4. **Group** related components into sub-tasks
5. **Determine** dependencies between sub-tasks
6. **Output** structured task list with metadata

### Sub-Agent Spawning

```json
{
  "runtime": "subagent",
  "mode": "run",
  "task": "<specific sub-task>",
  "timeoutSeconds": 300,
  "streamTo": "parent"
}
```

### Progress Tracking

- Track each sub-agent's status: `pending` → `running` → `completed`/`failed`
- Monitor execution time
- Handle timeouts and retries
- Report progress to main session

### Conflict Resolution

When sub-agents produce conflicting results:

1. **Flag** the conflict
2. **Request** clarification from each agent
3. **Escalate** to human if unresolved
4. **Document** the resolution

## Error Handling

### Sub-Agent Failures

| Error | Handling |
|-------|----------|
| Timeout | Retry once with extended timeout |
| Crash | Spawn replacement agent |
| Invalid output | Request clarification |
| Resource exhausted | Queue and retry later |

### Synthesis Failures

| Error | Handling |
|-------|----------|
| Missing results | Proceed with available data, flag gaps |
| Conflicting data | Flag for human review |
| Format mismatch | Normalize before merging |

## Best Practices

### Do's

✅ **Clear task boundaries** - Each sub-task should be self-contained
✅ **Explicit success criteria** - Define what "done" looks like
✅ **Reasonable timeouts** - Account for complexity
✅ **Progressive synthesis** - Synthesize as results arrive
✅ **Human escalation** - Know when to involve the user

### Don'ts

❌ **Over-parallelize** - Too many agents creates coordination overhead
❌ **Vague instructions** - Sub-agents need clear, specific tasks
❌ **Ignore dependencies** - Sequential tasks must respect order
❌ **Blind synthesis** - Review before merging conflicting results
❌ **No fallback** - Always have a plan B for failures

## Limitations

- **Context limits** - Each sub-agent has independent context
- **Coordination overhead** - More agents = more management
- **Cost** - Multiple agents = higher token usage
- **Complexity** - Debugging multi-agent flows is harder

## Troubleshooting

### Problem: Sub-agents produce inconsistent results

**Solution:**
1. Standardize the output format in task instructions
2. Add validation step before synthesis
3. Use `compare` synthesis mode to highlight differences

### Problem: Task takes too long

**Solution:**
1. Increase parallelization
2. Reduce scope per agent
3. Set aggressive timeouts with retries

### Problem: Results are too fragmented

**Solution:**
1. Use `consolidate` synthesis mode
2. Add explicit integration step
3. Assign one agent to "editor" role

## API Reference

### Orchestrate Command

```
orchestrate <task> [options]

Options:
  --agents <n>        Number of sub-agents (default: auto)
  --mode <mode>       Execution mode: parallel|sequential|hybrid
  --timeout <sec>     Timeout per sub-agent (default: 300)
  --synthesis <type>  Synthesis type: merge|summarize|compare|consolidate
  --verbose           Show detailed progress
```

### Status Command

```
orchestrate status <session_id>

Shows current orchestration session status
```

## Changelog

### v1.0.0 (2026-03-12)
- Initial release
- Task decomposition
- Sub-agent spawning and coordination
- Result synthesis
- Progress tracking
- Error handling

## License

MIT

---

*Part of the multi-agent toolkit for OpenClaw*

*"Alone we can do so little; together we can do so much."*
