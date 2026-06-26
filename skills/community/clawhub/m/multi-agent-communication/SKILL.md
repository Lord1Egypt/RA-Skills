---
name: multi-agent-communication
description: Based on two core tools, sessions_spawn and sessions_send, to help users build, manage, and optimize distributed Agent systems, enabling task decomposition, parallel processing, and efficient coordination among Agents.
---

# Multi-Agent Communication

Core tools: `sessions_spawn` (launch child Agents) and `sessions_send` (send messages to existing Agents).

## Use Cases

- Launching child Agents for background tasks
- Multi-Agent collaboration and negotiation
- Configuring Agent permissions and concurrency limits
- Choosing the appropriate communication mode (run/session/send)
- Designing Agent team workflows

## Two Core Tools

### sessions_spawn — Create a new Agent instance

```
sessions_spawn({
  task: "Review PR #123",
  agent: "code-reviewer",     // Agent ID (not SOUL name)
  mode: "run",                // run=one-shot, session=persistent
  thread: false,              // Whether to bind to a message thread
  runTimeoutSeconds: 300      // Optional, timeout duration
})
```

**Essence: Fork a new process.** Creates an independent session and execution environment, automatically pushing results back to the parent Agent upon completion. In mode="run", the child Agent's execution process is not visible to the user by default.

### sessions_send — Send a message to an existing Agent

```
sessions_send({
  sessionKey: "agent:main:subagent:abc",
  label: "security",          // Use sessionKey or label
  message: "Check security",
  timeoutSeconds: 30          // Synchronous wait; 0=asynchronous delivery
})
```

**Essence: Inter-Process Communication (IPC).** Sends messages to an existing session, supporting multi-round A2A negotiation (up to 5 rounds of ping-pong).

## Core Decision: Which One to Choose?

| Scenario | Tool | Mode |
|----------|------|------|
| Background data processing, one-shot analysis | sessions_spawn | mode: "run" |
| Parallel task decomposition (multiple spawns) | sessions_spawn | mode: "run" |
| Multi-round code review (user-visible) | sessions_spawn | mode: "session", thread: true |
| Real-time collaborative Q&A between Agents | sessions_send | timeoutSeconds > 0 |
| Asynchronous delivery, no reply needed | sessions_send | timeoutSeconds: 0 |

**Quick Judgment:**
- Need to **create a new Agent** → sessions_spawn
- Need to communicate with an **existing Agent** → sessions_send

## Spawn Execution Flow (10 Stages)

```
User Request → Main Agent → sessions_spawn
  ↓
[1. Permission Check]  → Verify depth, concurrency, whitelist
  ↓
[2. Session Creation]  → Generate unique sessionKey
  ↓
[3. Thread Binding]    → (Optional) Bind to Discord/Slack thread
  ↓
[4. Attachment Handling] → Snapshot transfer (independent lifecycle)
  ↓
[5. System Prompt]     → Inject task context
  ↓
[6. Working Directory] → Inherit parent Agent or use target Agent config
  ↓
[7. Agent Launch]      → Via Gateway RPC
  ↓
[8. Runtime Registration] → Record in SubagentRegistry
  ↓
[9. Hook Trigger]      → Notify plugins
  ↓
[10. Result Return]    → Return childSessionKey
```

Results are automatically pushed back to the parent Agent via Sweeper (checks every 1-8 seconds), no manual polling required.

## Session Key Design

```
Main Agent:    agent:main:main
Child Agent:   agent:main:subagent:<uuid>
Grandchild:    agent:main:subagent:<uuid>:subagent:<uuid>
```

UUID ensures global uniqueness; the hierarchical structure facilitates routing and traceability.

## mode="run" vs. mode="session"

| Feature | run | session |
|---------|-----|---------|
| Lifecycle | One-shot, deleted upon completion | Persistent, awaits subsequent messages |
| Thread Binding | Not supported | Required (thread=true) |
| User Visibility | ❌ Completely invisible | ✅ Visible in thread |
| Applicable Scenarios | Background data processing | Multi-turn conversations, code reviews |

**⚠️ Note: mode="session" must also have thread=true set**, otherwise subsequent messages cannot be routed correctly.

## Three-Tier Security Protection

| Constraint | Default Value | Purpose |
|------------|---------------|---------|
| Max Recursion Depth | 1 | Prevent infinite recursion |
| Max Child Processes | 5/session | Prevent resource exhaustion |
| Whitelist Mechanism | Configurable | Cross-Agent permission control |

## A2A Multi-Round Negotiation (sessions_send)

```
Agent A ──"Format this code"──→ Agent B
         ←─"Which style do you prefer?"
Agent A ──"Use Prettier"─────→ Agent B
         ←─"Done"
Agent A ──REPLY_SKIP──────────→ Agent B
```

- Maximum 5 rounds (configurable)
- Either party replies with REPLY_SKIP_TOKEN to end
- Final result delivered to the user channel

## Key Design Decisions

- **Snapshots over References**: Attachments are copied to the child Agent; the child can still access them even after the parent deletes them.
- **Push over Polling**: Zero polling cost; a 30-second task saves approximately 15,000 tokens.
- **Cross-Agent Workspace Isolation**: Same-type child Agents inherit the parent directory; cross-type ones use the target Agent's configuration.

## Configuration Suggestions

See [references/config.md](references/config.md) for details.

## Design Patterns

See [references/patterns.md](references/patterns.md) for details.