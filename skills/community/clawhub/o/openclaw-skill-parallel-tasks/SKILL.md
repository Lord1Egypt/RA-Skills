---
name: parallel-tasks
description: Execute multiple tasks in parallel with timeout protection, error isolation, and real-time progress feedback. Use when user says "run these in parallel", "parallel execution", "concurrent tasks", or wants multiple independent tasks done simultaneously with proper error handling and timeout control.
---

# Parallel Tasks Skill

Execute multiple tasks **in parallel** with enterprise-grade reliability: timeout protection, error isolation, and real-time progress feedback.

## When to Use

Use this skill when:
- User says "run these in parallel" or "do these simultaneously"
- Multiple independent tasks need to be executed at once
- User wants faster results by running tasks concurrently
- Tasks are slow and user wants to avoid waiting sequentially

## Core Concept

**Serial vs Parallel**:

```
SERIAL (slow):
Task 1 → Task 2 → Task 3  (5min + 5min + 5min = 15min)

PARALLEL (fast):
Task 1 ─┬─> (5min total, not 15min)
Task 2 ─┼─>
Task 3 ─┘
```

## Usage

### Basic Parallel Execution

```
/parallel
- Task 1: Search for docs
- Task 2: Search for code
- Task 3: Search for examples
```

### Named Tasks with Custom Timeout

```
/parallel timeout=300
- [search-docs] Search for relevant documentation
- [search-code] Find similar implementations
- [analyze] Analyze the results
```

### CLI Usage (scripts/executor.ts)

```bash
# Simple usage
node scripts/executor.ts "Research AI trends" "Research market analysis"

# Named tasks with custom timeout
node scripts/executor.ts --timeout 600 \
  --task "[research] Research AI trends" \
  --task "[implement] Build the feature"

# Read from file (one task per line)
node scripts/executor.ts --tasks-file my-tasks.txt --max-concurrent 3

# Named task formats (all equivalent):
# - [name] description
# - - description (auto-named as task-1, task-2, ...)
# - 1. description
```

## Implementation

### Core Execution Pattern

The executor uses a **semaphore pattern** with configurable concurrency:

```typescript
// 1. Parse tasks from input
const tasks = parseTaskInput(input)

// 2. Execute tasks with concurrency control
const results: TaskResult[] = []
const executing: Promise<void>[] = []

for (const task of tasks) {
  // Wait if at max concurrency
  if (executing.length >= maxConcurrent) {
    await Promise.race(executing)
  }

  const promise = runTask(task).then(result => {
    results.push(result)
    // Remove from executing list
    const idx = executing.indexOf(promise)
    if (idx > -1) executing.splice(idx, 1)
  })

  executing.push(promise)
}

await Promise.all(executing)
```

### Task Execution via hermes cli

```typescript
async function executeTaskViaSpawn(
  task: Task,
  timeoutSeconds: number
): Promise<TaskResult> {
  const taskId = `parallel-${Date.now()}-${randomId()}`

  return new Promise((resolve) => {
    const proc = spawn('hermes', [
      'cli', '--',
      'sessions_spawn',
      '--task', `"${task.description}"`,
      '--label', `"${task.name}"`,
      '--timeout', String(timeoutSeconds),
      '--session-id', taskId
    ], { stdio: ['ignore', 'pipe', 'pipe'] })

    // Timeout handling
    const timeoutId = setTimeout(() => {
      proc.kill('SIGTERM')
      resolve({
        name: task.name,
        status: 'timeout',
        duration: Date.now() - startTime,
        error: `Exceeded ${timeoutSeconds}s timeout`
      })
    }, timeoutSeconds * 1000)

    proc.on('close', (code, signal) => {
      clearTimeout(timeoutId)
      if (signal === 'SIGTERM') {
        resolve({ name: task.name, status: 'timeout', ... })
      } else if (code === 0) {
        resolve({ name: task.name, status: 'fulfilled', ... })
      } else {
        resolve({ name: task.name, status: 'rejected', ... })
      }
    })
  })
}
```

### Timeout Protection

| Option | Default | Description |
|--------|---------|-------------|
| `timeout` | 300 | Default timeout per task (seconds) |
| Per-task timeout | - | Override global timeout for specific tasks |

**Behavior**: Task auto-terminates after timeout, other tasks continue.

### Error Isolation

Each task runs in **complete isolation**:

| Problem | Serial | Parallel (This Skill) |
|---------|--------|----------------------|
| One task fails | All others stop | Only failed task affected |
| One task hangs | Blocks entire flow | Others continue normally |
| One task times out | May cascade | Contained, others finish |

### Concurrency Control

| Option | Default | Description |
|--------|---------|-------------|
| `maxConcurrent` | 5 | Maximum tasks running simultaneously |

**Pattern**: Semaphore-style - starts N tasks, when one completes, starts next.

### Progress Feedback

Real-time terminal output with colored status:

```
🚀 Starting 3 tasks in parallel (max 5 concurrent)...

🔄 [task-1] Starting (timeout: 300s)...
🔄 [task-2] Starting (timeout: 300s)...
🔄 [task-3] Starting (timeout: 300s)...
✅ [1/3] [task-1] Complete (23.5s)
✅ [2/3] [task-2] Complete (45.2s)
⏱️  [3/3] [task-3] Timeout after 300s
```

## Task Input Formats

### 1. Named Tasks (Recommended)

```
[research] Research AI trends and write report
[implement] Build the feature
[test] Write comprehensive tests
```

### 2. Bullet List

```
- Search for API documentation
- Find relevant code examples
- Check for existing implementations
```

### 3. Numbered List

```
1. Research authentication patterns
2. Design database schema
3. Implement API endpoints
```

### 4. Plain Text (auto-named)

```
Research AI trends
Build the feature
Write tests
```
→ Auto-named: task-1, task-2, task-3

## Output Format

### Success Case

```
✅ Parallel Execution Complete
   3 tasks: 2 succeeded, 1 failed (45.2s total)

┌─────────────────────┬────────────┬────────────┐
│ Task                │ Status     │ Duration   │
├─────────────────────┼────────────┼────────────┤
│ research            │ ✅ fulfilled│ 23.5s      │
│ implement           │ ✅ fulfilled│ 45.2s      │
│ test                │ ⏱️ timeout  │ 300.0s    │
└─────────────────────┴────────────┴────────────┘

❌ Failed Tasks:
   • test: Exceeded 300s timeout
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All tasks succeeded |
| 1 | Some tasks failed or timed out |

## Options

### CLI Options

| Option | Default | Description |
|--------|---------|-------------|
| `--timeout, -to` | 300 | Timeout per task (seconds) |
| `--max-concurrent, -m` | 5 | Max concurrent tasks |
| `--stop-on-error` | false | Stop all if one fails |
| `--no-progress` | false | Suppress progress output |
| `--tasks-file, -f` | - | Read tasks from file |
| `--parse` | - | Parse stdin to JSON |

### Per-Task Options (in task description)

```
[name] description (timeout=600)
```

## Error Handling

### Error Types

| Status | Cause | Behavior |
|--------|-------|----------|
| `fulfilled` | Task succeeded | Returns result value |
| `timeout` | Exceeded timeout | Task terminated, others continue |
| `rejected` | Process error | Error captured, others continue |
| `cancelled` | User cancelled | All running tasks terminate |
| `no_reply` | No output | Reported as warning |

## Best Practices

1. **Independent tasks first**: Tasks should not depend on each other
2. **Set reasonable timeouts**: Don't set 5min if task should take 30s
3. **Use named tasks**: Easier to debug when something fails
4. **Keep tasks focused**: One clear goal per task
5. **Mind concurrency**: Don't set maxConcurrent higher than system can handle

## Examples

### Example 1: Research Multiple Topics

```bash
node scripts/executor.ts \
  "Research Claude Code best practices" \
  "Find OpenClaw skill examples" \
  "Search for agent design patterns"
```

### Example 2: Named Tasks from File

```bash
# tasks.txt:
# [research] Research AI trends
# [implement] Build the feature
# [test] Write tests

node scripts/executor.ts --tasks-file tasks.txt --timeout 600
```

### Example 3: Parallel Implementation

```bash
node scripts/executor.ts --timeout 600 \
  --task "[backend] Implement user authentication API" \
  --task "[frontend] Build login form component" \
  --task "[database] Create users table migration"
```

### Example 4: Web Scraping

```bash
node scripts/executor.ts \
  --task "[store1] Fetch product data from store1.com" \
  --task "[store2] Fetch product data from store2.com" \
  --task "[store3] Fetch product data from store3.com"
```

## Anti-Patterns

❌ **Don't use for dependent tasks**:
```bash
# WRONG - second task depends on first!
node scripts/executor.ts \
  "Create user account" \
  "Send welcome email"
```
Use sequential execution instead.

❌ **Don't use for very fast tasks**:
```bash
# WRONG - spawning overhead not worth it
node scripts/executor.ts "Read file A" "Read file B" "Read file C"
```
The overhead of spawning parallel sessions isn't worth it for sub-second tasks.

## Related Skills

- `subagents` - Background agent spawning
- `batch-operations` - Bulk file operations
- `workflow-orchestrator` - Complex multi-step workflows
