# Multi-Thread Dialogue

English | [中文](./SKILL.md)

Multi-thread dialogue architecture: main agent handles foreground, sub-agents process tasks in background with status handling, two-stage review, and monitoring.

## Features

### 1. Smart Task Routing
- **Simple tasks** (≤3 tool calls): handled in foreground
- **Long tasks** (>3 tool calls): spawn sub-agent
- **Context bloat** (>3000 tokens): spawn sub-agent
- **Independent tasks**: parallel execution (up to 5)

### 2. Model Selection
- **Mechanical** (1-2 files, clear spec): mini/fast model
- **Standard** (multi-file integration): inherit parent model
- **Judgment** (architecture/review): strongest model

### 3. Status Handling
| Status | Meaning | Action |
|--------|---------|--------|
| `DONE` | Task complete | Show result or enter review |
| `DONE_WITH_CONCERNS` | Done with doubts | Read concerns then decide |
| `NEEDS_CONTEXT` | Need more info | Provide info, re-dispatch |
| `BLOCKED` | Cannot complete | Assess cause and handle |

### 4. Quality Assurance (Optional)
Two-stage review:
```
[Implementer] → [Spec Review] → [Code Quality Review] → [Show Result]
```

### 5. Interaction
- **Task numbering**: incrementing IDs (1, 2, 3...)
- **Interrupt**: say "stop" or "interrupt" to kill recent task
- **Targeted reply**: "task X..." to reply to specific task

### 6. Monitoring
- 30-minute timeout reminder
- 1-day timeout auto-delete
- User replies by task number

## Installation

### 1. Install Skill

```bash
npx skills add multi-thread-dialogue
# or globally
npx skills add multi-thread-dialogue -g

### 2. Configure AGENTS.md

Add the following to your `AGENTS.md`:

```markdown
## 🧵 Multi-Thread Dialogue Mode

### Trigger Rules
| Condition | Threshold | Behavior |
|-----------|-----------|----------|
| Simple task | ≤3 tool calls | Foreground |
| Long task | >3 tool calls | Spawn sub-agent |
| Context bloat | >3000 tokens | Spawn sub-agent |
| Independent | Multi-step | Parallel (max 5) |

### Model Selection
| Complexity | Model | Example |
|------------|-------|---------|
| Mechanical | mini/fast | Simple refactor |
| Standard | Inherit parent | Feature implementation |
| Judgment | Strongest | Architecture/review |

### Status Handling
- DONE: Show result or enter review
- DONE_WITH_CONCERNS: Read concerns then decide
- NEEDS_CONTEXT: Provide info, re-dispatch
- BLOCKED: Assess cause and handle

### Interaction
- Task number: Each sub-agent gets incrementing ID
- Interrupt: "stop" or "interrupt" kills recent task
- Target reply: "task X..." for specific task

### Monitoring
- 30-minute wait reminder
- 1-day timeout auto-delete
```

### 3. Create Task State File

```bash
mkdir -p memory
echo '{"nextTaskId": 1, "tasks": []}' > memory/multi-thread-tasks.json
```

## Usage

### Prompt Template for Spawning Sub-agents

```markdown
[TASK CONTEXT]
You are working on [specific task] in [project/domain].

[OBJECTIVES]
1. [Specific objective 1]
2. [Specific objective 2]

[CONSTRAINTS]
- Focus on: [specific scope]
- Prioritize: [important items]
- Skip: [unnecessary items]

[OUTPUT FORMAT]
Return: [specific format]

[COMPLETION CRITERIA]
Complete when: [specific criteria]
```

### Status Markers

When sub-agent completes, mark status clearly:
- `DONE` - Task complete
- `DONE_WITH_CONCERNS: [concerns]` - Done but has doubts
- `NEEDS_CONTEXT: [missing info]` - Need more info
- `BLOCKED: [reason]` - Cannot complete

### Check Status

```
You: task list / what's running
→ Show all active sub-agents
```

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| Short task threshold | ≤3 tool calls | Task complexity判断 |
| Stuck threshold | 30 minutes | Wait time before reminder |
| Timeout delete | 1 day | Auto-delete after timeout |
| Max parallel | 5 | Max concurrent sub-agents |

## File Structure

```
multi-thread-dialogue/
├── SKILL.md
├── _meta.json
├── skill.yaml
├── README.md
└── docs/
    └── multi-thread-dialogue-plan.md  # Full plan document
```

## Related Skills

- `skill-creator`: Skill creation tool
- `subagent-creator`: Subagent creator (tech-leads-club)
- `codex-subagent`: Codex subagent (am-will)
- `superpowers`: Subagent-driven development (obra)
