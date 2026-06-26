# Multi-Agent Orchestration

## Agent Collaboration Patterns

### Sequential Chain
Agent A → Agent B → Agent C (each depends on previous output)
```
Research Agent → Writer Agent → Editor Agent → Publisher Agent
```

### Parallel Fan-Out
Split task across multiple agents, merge results
```
Coordinator → [Agent A, Agent B, Agent C] → Merger
```

### Debate / Adversarial
Two agents argue different perspectives, third decides
```
Pro Agent ↔ Con Agent → Judge Agent
```

### Hierarchical
Manager agent delegates to specialist agents
```
Manager → [Specialist A, Specialist B, Specialist C]
```

### Review Loop
Agent produces → Reviewer critiques → Agent revises (max N iterations)
```
Worker → Reviewer → (approve | revise → Worker)
```

## Orchestration Tools
- **sessions_spawn** — Create isolated agent sessions
- **sessions_send** — Send messages to running agents
- **sessions_list** — Monitor active sessions
- **subagents** — List, steer, kill spawned agents
- **sessions_yield** — Wait for agent completion

## Spawning Best Practices
```python
# One-shot task
sessions_spawn(
    task="Analyze this data and produce a summary",
    mode="run",
    model="appropriate-model"
)

# Persistent session for ongoing work
sessions_spawn(
    task="Monitor and respond to GitHub PR reviews",
    mode="session",
    thread=True
)
```

## Coordination Patterns

### Task Distribution
1. Break work into independent units
2. Spawn agents for each unit
3. Collect results via sessions_list
4. Merge outputs into final result

### Error Recovery
- If agent fails, retry with different approach
- If agent loops, kill and spawn replacement
- Fallback to manual execution

### Resource Management
- Limit concurrent agents (token budget)
- Use cheaper models for simple tasks
- Use thinking models for complex reasoning
- Clean up completed sessions

## Use Cases
- Code review: parallel analysis by security, performance, style agents
- Research: multiple agents search different sources
- Content: research → draft → edit → format pipeline
- Data: parallel ETL agents for different data sources
