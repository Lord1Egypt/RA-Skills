# Platform Integration Guide

Concrete methods for implementing Loop Engineering design principles on the OpenClaw platform. Covers scheduling, skill modules, sub-agent dispatching, and persistence engine integration.

---

## OpenClaw Automations + cron

### Concept Mapping

Loop Engineering's **Automation** concept maps directly to OpenClaw's cron scheduling system:

| Loop Engineering | OpenClaw | Description |
|------------------|----------|-------------|
| Automation | Cron job | Task scheduler triggered by time/interval |
| Loop cycle | cron expression | Defines execution frequency |
| Trigger condition | Time + optional pre-check | Determines when to execute |
| Archive | Task log + round records | Preserves execution history |

### Configuration

```bash
# Run a code review loop every 30 minutes
openclaw cron add "code-review-loop" \
  --schedule "*/30 * * * *" \
  --task "Check code quality of the latest commit, run tests, auto-fix issues if any"

# Generate daily report at 9 AM every day
openclaw cron add "daily-report" \
  --schedule "0 9 * * *" \
  --task "Summarize all task execution from yesterday, generate a daily report"
```

### Mapping to Loop Patterns

- **Scheduled inspection type**: Use cron directly, set `maxRounds` to 1 (execute one complete round per trigger)
- **Goal-oriented type**: cron as the trigger source, internally use `/goal` to loop until conditions are met
- **Event-driven type**: Combine with webhook or file change monitoring, cron as a fallback check

### Notes

- Relationship between cron scheduling and `/loop` primitives: cron defines "when to trigger", `/loop` defines "how to execute after triggering"
- Avoid cron intervals shorter than single execution time to prevent task pile-up
- Use `openclaw cron list` and `openclaw cron log` to monitor execution status

---

## OpenClaw Skills as Skill Modules

### Concept Mapping

Loop Engineering's **Skills** map directly to the OpenClaw Skills system. Skills are encapsulated capability modules that auto-activate via skill routing -- when a loop task's content matches a Skill's trigger conditions, that Skill loads automatically.

### Scheduling Skills Within a Loop

```yaml
loop:
  name: "feature-development-cycle"
  rounds:
    - round: 1
      action: "Analyze requirements"
      skills: ["industry-research", "sdd-spec-gen"]
    - round: 2
      action: "Write code"
      skills: ["coding-agent", "rust"]
    - round: 3
      action: "Test and review"
      skills: ["superpowers"]
    - round: 4
      action: "Deploy and verify"
      skills: ["healthcheck"]
```

### Key Principles

1. **Activate on demand**: Don't let the loop preload all Skills; let each round's task naturally trigger the corresponding Skill
2. **Skills are stateless**: Skills do not save state; state is uniformly managed by Worktree
3. **Composition over embedding**: Use Skill composition instead of embedding all logic in a single Skill
4. **Version awareness**: Skill updates may affect loop behavior; critical loops should pin Skill versions

### Building Loop-Specific Skills

Loop-specific Skills should explicitly declare in SKILL.md:

```yaml
name: my-loop-skill
description: |
  Describe the Skill's role in the loop. Trigger words should include keywords from loop scenarios.
  Trigger words: "loop check", "auto fix", "round analysis"
---
# Loop-specific contract
- Input: Previous round output summary + current round state
- Output: Structured result (for consumption by the next round or orchestrator)
- Side effects: No state saved inside the Skill
```

---

## Sub-agents Pattern (sessions_spawn)

### Concept Mapping

Loop Engineering's **Sub-agent** pattern is implemented through OpenClaw's `sessions_spawn`. Each Sub-agent is an independent session with its own context window and model configuration.

### Basic Usage

```python
# Serial dispatch
result = sessions_spawn(
    task="Analyze the code structure under src/ and output a dependency graph",
    agent="analyzer",
    model="claude-sonnet"
)

# Parallel dispatch
results = sessions_spawn_many([
    {"task": "Implement module A", "agent": "coder"},
    {"task": "Implement module B", "agent": "coder"},
    {"task": "Write tests", "agent": "tester"}
])
```

### Three Orchestration Patterns

- **Serial dependency chain**: Each Sub-agent's output becomes the next one's input `[Analyze] -> [Design] -> [Implement] -> [Test] -> [Review]`
- **Parallel fan-out**: Main loop waits for all Sub-agents to complete, then aggregates results
- **Hybrid mode**: Serial grouping first, parallel within groups, final merge and review

### Key Principles

1. **Context isolation**: Each Sub-agent receives only the minimal context needed to complete its task
2. **Structured results**: Require Sub-agents to output JSON/YAML for easy parsing and aggregation by the orchestrator
3. **Timeout settings**: Set independent timeouts for each Sub-agent to prevent a single task from blocking the entire loop
4. **Error isolation**: One Sub-agent's failure should not crash the entire loop

```python
# Robust Sub-agent dispatch
def spawn_with_fallback(task, agent, timeout=300, retries=2):
    for attempt in range(retries + 1):
        try:
            result = sessions_spawn(task=task, agent=agent, timeout=timeout)
            if result.success:
                return result
        except TimeoutError:
            if attempt == retries:
                raise
    return None
```

---

## TaskFlow Deep Integration

### Concept Mapping

TaskFlow is OpenClaw's underlying persistence engine, providing task lifecycle management and cross-round state preservation for Loop Engineering.

| Loop Engineering | TaskFlow | Description |
|------------------|----------|-------------|
| Loop task | TaskFlow Task | Persistent task entity with a unique ID |
| Round | TaskFlow Subtask | Each loop iteration as a subtask |
| State management | TaskFlow State | Task-level persistent state storage |
| Progress tracking | TaskFlow History | Auto-recorded task execution history |
| Termination condition | TaskFlow Completion | Verifiable completion condition |

### Integration Architecture

```
Loop Engineering Layer  -- Loop logic, orchestration, decision-making
        |
TaskFlow Persistence Layer -- Task lifecycle, state storage, history
        |
OpenClaw Execution Layer  -- Agent execution, Skills invocation, Sub-agent dispatch
```

### State Persistence and Subtask Tracking

```python
# Restore state before loop starts
state = taskflow.get_state(task_id)
round_number = state.get("round", 0) if state else 0
previous_output = state.get("lastOutput") if state else None

# Start a new round (create subtask)
subtask = taskflow.create_subtask(
    parent_id=loop_task_id,
    name=f"round-{round_number + 1}",
    description=f"Loop round {round_number + 1}"
)

# Round execution...

# Save state + mark subtask as complete
taskflow.save_state(task_id, {
    "round": round_number + 1,
    "lastOutput": current_output,
    "pending": updated_pending,
    "timestamp": now()
})
taskflow.complete_subtask(subtask.id, result=round_output)
```

### Best Practices Combined with Loop Engineering

1. **TaskFlow manages "what"**: Task identity, state, history, parent-child relationships
2. **Loop Engineering manages "how"**: Loop logic, decision rules, orchestration strategy
3. Don't write loop logic at the TaskFlow layer -- it's a storage engine, not an orchestration engine
4. Don't manage task identity at the Loop layer -- task IDs and state formats belong to TaskFlow
5. Use TaskFlow's revision-checked mechanism to prevent concurrent state conflicts

---

## General Integration Principles

The following principles are platform-agnostic and apply to any Loop Engineering implementation.

### 1. Separation of Concerns

Divide the loop system into three layers, each with clear interfaces and responsibilities:

```
[Orchestration Layer] Loop logic, decision-making, scheduling
[Execution Layer]    Agent invocation, tool usage, result generation
[Persistence Layer]  State storage, history, task identity
```

### 2. Progressive Adoption

```
Phase 1: Select 1-2 tasks suitable for looping as pilots
Phase 2: After validation and stabilization, gradually expand scope
Phase 3: Establish team-internal loop design specifications and templates
Phase 4: Distill mature loop patterns into reusable Skills
```

### 3. Observability First

Loop systems must have complete observability:

- **Logs**: Per-round input, output, decision rationale
- **Metrics**: Round count, token consumption, success rate, average duration
- **Alerts**: Notifications for consecutive failures, timeouts, state anomalies
- **Traceability**: Ability to trace back the complete context of any historical round

### 4. Human-Machine Collaboration Boundary

Clearly define which decisions the loop system makes autonomously and which require human confirmation:

```
Autonomous        : Code formatting, test execution, lint fixes
Semi-auto (confirm): Architecture changes, API modifications, dependency upgrades
Human decision    : Security policies, deployment releases, major refactoring
```

### 5. Cost Awareness

Loop systems are long-running; cost control must be built in:

- Set hard token budget caps
- Prioritize low-cost models for exploratory rounds
- Set approval thresholds for high-cost model usage
- Periodically audit the loop system's ROI

### 6. Platform Independence

Core design should not bind to a specific platform -- describe loop logic with platform-agnostic abstractions (YAML/JSON), and let platform adapters translate to specific API calls:

```yaml
# Platform-agnostic loop description
loop:
  name: "code-review-cycle"
  maxRounds: 5
  completionCheck:
    type: "external"
    condition: "review.passed && issues.resolved == 0"
  rounds:
    - action: "analyze"
      tool: "static-analysis"
    - action: "review"
      tool: "code-review"
    - action: "fix"
      tool: "auto-fix"
    - action: "verify"
      tool: "test-runner"
```

> Platform integration is the critical step from Loop Engineering theory to practice. On top of specific platform features, always maintain design generality and portability.