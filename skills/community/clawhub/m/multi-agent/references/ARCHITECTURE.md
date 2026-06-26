# Multi-Agent Architecture

This document describes the architecture and design patterns of the OpenClaw Multi-Agent skill, based on Claude Code's Coordinator Mode.

## Core Design Principles

### 1. Asymmetric Tool Partitioning

The most important design decision is the **separation of tools** between Coordinator and Workers:

- **Coordinator**: Can only spawn, communicate with, and stop workers
- **Worker**: Has full tool access (file read/write, bash, web search, etc.)

This creates a clean separation of concerns:
- Coordinator focuses on orchestration and synthesis
- Workers focus on execution

### 2. Four-Phase Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  PHASE 1: RESEARCH                                           │
│  ├── Spawn N parallel workers (researchers)                  │
│  ├── Each worker explores different aspect of codebase       │
│  └── Workers report findings via XML notifications           │
├─────────────────────────────────────────────────────────────┤
│  PHASE 2: SYNTHESIS                                          │
│  ├── Coordinator reads ALL findings (no lazy delegation)     │
│  ├── Coordinator understands the problem deeply              │
│  └── Coordinator creates implementation specification        │
├─────────────────────────────────────────────────────────────┤
│  PHASE 3: IMPLEMENTATION                                     │
│  ├── Spawn M implementation workers                          │
│  ├── Each worker handles specific files/modules              │
│  └── Workers execute changes per specification               │
├─────────────────────────────────────────────────────────────┤
│  PHASE 4: VERIFICATION                                       │
│  ├── Spawn verification workers                              │
│  ├── Test that changes work correctly                        │
│  └── Report results to Coordinator                           │
└─────────────────────────────────────────────────────────────┘
```

### 3. XML Communication Protocol

Workers communicate with Coordinator via structured XML messages:

```xml
<task-notification>
  <task-id>worker-abc123</task-id>
  <status>completed</status>
  <summary>Found 15 relevant files</summary>
  <result>Detailed findings...</result>
  <usage>
    <total-tokens>2048</total-tokens>
    <tool-uses>5</tool-uses>
    <duration-ms>15000</duration-ms>
  </usage>
</task-notification>
```

Why XML?
- Self-describing and extensible
- LLM-friendly (Claude is tuned for XML structures)
- Easy to parse and validate

### 4. Scratchpad File System

Multi-agent coordination requires shared knowledge storage:

```
.openclaw/scratchpad/
├── worker-researcher-abc123.json    # Worker spec
├── worker-implementer-def456.json   # Worker spec
├── findings-researcher-abc123.json  # Research findings
├── implementation-spec.md           # Synthesized spec
├── todos-worker-abc123.json         # TODO lists
└── notification-*.xml               # Task notifications
```

Benefits of filesystem-based sharing:
- Persistent across agent restarts
- Random access (not sequential like messages)
- Can store large documents
- Natural deduplication (overwrite)

### 5. Continue vs Spawn Decision Matrix

Coordinator must decide whether to:
- **Continue** an existing worker (send more instructions)
- **Spawn** a fresh worker (start from clean slate)

| Situation | Decision | Rationale |
|-----------|----------|-----------|
| Research explored exactly the files that need editing | Continue | Worker has relevant files in context |
| Research was broad but implementation is narrow | Spawn fresh | Avoid dragging exploration noise |
| Correcting a failure or extending recent work | Continue | Worker has error context |
| Verifying code a different worker wrote | Spawn fresh | Verifier should see code with fresh eyes |
| First attempt used wrong approach entirely | Spawn fresh | Wrong-approach context pollutes retry |
| Completely unrelated task | Spawn fresh | No useful context to reuse |

## Integration with OpenClaw

### Using Existing Tools

The Multi-Agent skill leverages OpenClaw's existing infrastructure:

| OpenClaw Tool | Usage in Multi-Agent |
|---------------|---------------------|
| `sessions_spawn` | Spawn worker agents |
| `sessions_send` | Send messages to workers |
| `sessions_list` | List active workers |
| `sessions_history` | Get worker results |
| `cron` | Schedule periodic tasks |
| `message` | Notify user of completion |

### Future: Agent Teams

Beyond Coordinator Mode, we can implement **Agent Teams**:

```
Team Lead (Coordinator)
    │
    ├── Shared Task List (DAG with dependencies)
    ├── Mailbox (peer-to-peer messaging)
    │
    └── Teammates (named, persistent workers)
        ├── Backend Agent
        ├── Frontend Agent
        └── Test Agent
```

Features:
- Named teammates with colors
- File locking for task claiming
- Plan approval workflow
- Task dependencies and auto-unblocking

## Implementation Phases

### Phase 1: Basic Coordinator (Current)
- ✅ Four-phase workflow
- ✅ XML protocol
- ✅ Scratchpad filesystem
- ✅ Simulated worker execution

### Phase 2: Real Worker Spawning
- Integrate with `sessions_spawn`
- Real async worker execution
- Proper session management

### Phase 3: Agent Teams
- Named teammates
- Task dependencies
- Peer-to-peer messaging
- File locking

### Phase 4: Advanced Features
- Automatic context compaction
- Worker result caching
- Parallelism optimization
- Cost tracking

## Usage Examples

### Example 1: Code Refactoring

```python
# User request: "Refactor auth module to use OAuth2"

coordinator = Coordinator()

# Phase 1: Research
workers = await coordinator.phase_research(
    "Refactor auth module to use OAuth2",
    num_workers=3
)
# → 3 researchers explore:
#   - Current auth implementation
#   - OAuth2 libraries available
#   - Files that need changes

# Phase 2: Synthesis  
spec = await coordinator.phase_synthesis(workers)
# → Coordinator creates spec with:
#   - Exact files to modify
#   - OAuth2 library to use
#   - Migration steps

# Phase 3: Implementation
impl_workers = await coordinator.phase_implementation(spec)
# → 2 implementers make changes in parallel

# Phase 4: Verification
verif_workers = await coordinator.phase_verification(impl_workers)
# → Verifiers run tests, check for regressions
```

### Example 2: Parallel Bug Investigation

```python
# User request: "API is slow, find the bottleneck"

coordinator = Coordinator()

# Spawn workers to investigate different hypotheses in parallel
hypotheses = [
    "Database query performance issue",
    "Network latency spikes",
    "Cache invalidation problem"
]

workers = []
for hypothesis in hypotheses:
    worker = coordinator.spawn_worker(
        task=f"Test hypothesis: {hypothesis}",
        role="researcher"
    )
    workers.append(worker)

# Wait for all to complete, then synthesize findings
```

## Security Considerations

1. **Permission Inheritance**: Workers inherit Coordinator's permission settings
2. **Sandboxing**: Workers can be run in isolated sessions
3. **Audit Trail**: All actions logged to scratchpad
4. **Kill Switch**: Coordinator can stop misbehaving workers immediately

## References

- [Claude Code Coordinator Mode Analysis](https://zread.ai/instructkr/claude-code/19-coordinator-mode)
- [Agent Teams Documentation](https://code.claude.com/docs/en/agent-teams)
- [Multi-Agent Workflow Patterns](https://addyosmani.com/blog/code-agent-orchestra/)
