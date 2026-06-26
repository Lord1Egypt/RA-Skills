# Model Routing Strategy

> **Optimize model selection for cost-effectiveness and task-appropriate performance**
> Priority: CRITICAL | Category: Infrastructure

## Overview

Model routing is the single most important decision affecting your OpenClaw deployment. Poor model selection can increase costs by 25x while providing no meaningful improvement in task completion.

## Core Principle

**Not all tasks need the most expensive model.** Match model capability to task complexity:

```
Simple/Repeated Tasks → Budget Models
Standard Operations   → Mid-Tier Models (Sonnet 4.6)
Complex Reasoning     → Premium Models (Opus 4.6)
Code Writing          → Specialized Models (Codex)
```

## Model Hierarchy

### Tier 1: Daily Operations (Primary)
**Model**: Claude Sonnet 4.6
**Cost**: $3 input / $15 output per million tokens
**Use for**:
- All standard agent operations
- Heartbeat checks
- Status monitoring
- Routine task execution
- Documentation reading
- File operations

**Why**: 72.5% OSWorld score (nearly equal to Opus 4.6's 72.7%), reliable tool calling, excellent personality for agent work.

### Tier 2: Heavy Lifting (Fallback)
**Model**: Claude Opus 4.6
**Cost**: $15 input / $75 output per million tokens
**Use for**:
- Complex multi-step reasoning
- Long-context analysis (1M token window)
- Critical decisions requiring highest accuracy
- Tasks where Sonnet failed

**Why**: Maximum capability when cost is secondary to correctness.

### Tier 3: Budget Operations (Cost-Optimized)
**Model**: Kimi K2.5 (via OpenRouter)
**Cost**: ~$0.60 input / $2 output per million tokens
**Use for**:
- High-volume, low-complexity tasks
- Status polling
- Simple file operations
- Background processing

**Why**: Reliable tool calling at 1/5th the price of Sonnet.

### Tier 4: Minimum Viable (Ultra-Budget)
**Model**: MiniMax M2.5
**Cost**: $0.30 input / $1.20 output per million tokens
**Use for**:
- Non-critical background tasks
- Simple data processing
- When budget is primary constraint

**Why**: 80.2% SWE-Bench, MIT licensed, cheapest reliable option.

## Routing Rules

### DEFAULT BEHAVIOR
1. Always start with **Sonnet 4.6** for unknown tasks
2. Only upgrade to Opus after Sonnet failure
3. Never use Opus for heartbeat or status checks
4. Use budget models for repeated/known-simple operations

### TASK TYPE ROUTING

```yaml
# Heartbeat & Monitoring
heartbeat:
  model: "kimi-k2.5"  # Cheap, reliable
  reasoning: "Status checks don't need reasoning"

# Documentation Reading
read_docs:
  model: "sonnet-4-6"  # Good comprehension
  reasoning: "Need understanding but not deep reasoning"

# Code Changes
code_changes:
  primary: "codex-gpt-5.3"  # Best for code
  fallback: "sonnet-4-6"
  reasoning: "Specialized code model"

# Complex Planning
complex_planning:
  primary: "sonnet-4-6"
  fallback: "opus-4-6"
  reasoning: "May need deep reasoning"

# Routine File Ops
file_ops:
  model: "minimax-m2.5"  # Cheapest reliable
  reasoning: "Simple operations"
```

### ESCALATION TRIGGERS

Upgrade to more expensive model when:
1. Task fails 2 times on current model
2. Task requires >50k token context
3. Task involves cross-system dependencies
4. User explicitly requests premium model

### DOWNGRADE TRIGGERS

Downgrade to cheaper model when:
1. Task is repeated/routine (after 3 successful runs)
2. Task is simple status check
3. Task involves simple file operations only
4. Budget constraints activated

## Configuration Template

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-sonnet-4-6",
        "fallbacks": [
          "anthropic/claude-opus-4-6",
          "openrouter/moonshotai/kimi-k2.5",
          "minimax/minimax-m2.5"
        ],
        "auto_escalation": true,
        "escalation_threshold": 2,
        "auto_downgrade": true,
        "downgrade_after": 3
      }
    }
  },
  "routing_rules": {
    "heartbeat": {
      "model": "openrouter/moonshotai/kimi-k2.5",
      "reason": "Cost optimization for repeated checks"
    },
    "documentation": {
      "model": "anthropic/claude-sonnet-4-6",
      "reason": "Balance of comprehension and cost"
    },
    "complex_reasoning": {
      "model": "anthropic/claude-opus-4-6",
      "reason": "Maximum capability"
    }
  }
}
```

## Runtime Model Switching

You can switch models mid-session:

```bash
# Switch to Opus for complex task
/model opus-4-6

# Switch back to Sonnet
/model sonnet-4-6

# Switch to budget model
/model kimi-k2.5
```

The routing configuration handles automatic fallbacks if rate limits are hit.

## Cost Monitoring

### Track Your Usage
```bash
# View token usage
openclaw stats tokens

# View cost breakdown
openclaw stats cost --by-model

# Set budget limits
openclaw config set budget.daily 10000000  # 10M tokens
openclaw config set budget.alert 8000000   # Alert at 8M
```

### Expected Costs Per Task Type

| Task Type | Tokens | Cost (Sonnet) | Cost (Opus) |
|-----------|--------|---------------|-------------|
| Heartbeat | ~500 | $0.01 | $0.04 |
| Read Doc | ~5,000 | $0.02 | $0.08 |
| Simple Change | ~10,000 | $0.05 | $0.20 |
| Complex Feature | ~50,000 | $0.20 | $1.00 |
| Full Session | ~100,000 | $0.40 | $2.00 |

## Decision Tree

```
New Task
    │
    ├─ Is it a heartbeat/status check?
    │   └─ YES → Use Kimi K2.5
    │
    ├─ Is it a repeated/routine task?
    │   └─ YES → Use MiniMax M2.5
    │
    ├─ Does it require code writing?
    │   └─ YES → Use Codex GPT-5.3
    │
    ├─ Is it complex/multi-step?
    │   └─ YES → Start with Sonnet 4.6
    │             └─ Fails? → Opus 4.6
    │
    └─ Default → Sonnet 4.6
```

## Common Mistakes

### ❌ DON'T
- Use Opus for heartbeat checks
- Use Opus for status polling
- Use premium models for known-simple tasks
- Never downgrade after task becomes routine
- Ignore rate limit handling

### ✅ DO
- Start every unknown task with Sonnet
- Use budget models for repeated operations
- Escalate only when necessary
- Downgrade when patterns emerge
- Monitor costs weekly

## Verification

After implementing this skill, verify:

```bash
# Check current model
openclaw config get model.primary

# Run test task
openclaw exec --task "simple status check" --dry-run

# Verify correct model selected
openclaw logs last --model-used
```

## Key Takeaway

**Sonnet 4.6 is 95% as capable as Opus 4.6 for agent work at 20% of the cost.** Use Opus only when Sonnet proves insufficient. Use budget models for anything repeated.

---

**Next Skills**: After implementing model routing, enable `execution-discipline.md` for proper task handling.
