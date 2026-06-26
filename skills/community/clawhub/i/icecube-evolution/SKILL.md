---
name: icecube-evolution
description: "🧊 IceCube Evolution — Continuous self-improvement system for AI agents. Learn from mistakes, capture success patterns, run eval loops, and evolve without human intervention. The engine that makes your agent smarter every day."
metadata:
  openclaw:
    requires: {}
---

# 🧊 IceCube Evolution

**The self-improvement engine for AI agents.**

Not "learn when asked." Not "improve when bugs happen." Just constant, automatic evolution.

## Why IceCube Evolution?

**The problem:**
- Agents make the same mistakes repeatedly
- Good patterns aren't captured
- No systematic improvement
- Improvement requires human intervention

**The solution:**
- Log every mistake automatically
- Capture every success pattern
- Run improvement loops on schedule
- Evolve without waiting for bugs

**The result:**
- Mistakes decrease over time
- Success patterns compound
- Agent gets better daily
- Zero manual intervention needed

## Architecture

### Three Files, One Loop

**mistake_log.md:**
```markdown
# Mistake Log

## ML-2026-03-17-001
- Date: 2026-03-17 14:32
- Context: Task dispatch
- Mistake: Did not check unclosed_work.yaml before starting new task
- Impact: Created duplicate task, wasted resources
- Fix: Add mandatory unclosed_work check to startup sequence
- Status: fixed
```

**success_patterns.md:**
```markdown
# Success Patterns

## SP-2026-03-17-001
- Date: 2026-03-17 15:45
- Context: Memory retrieval
- Pattern: Run memory_search before acting on any past-context task
- Result: Correct context loaded, no guessing
- Applicability: Any task referencing previous work
```

**improvement_queue.md:**
```markdown
# Improvement Queue

## IQ-2026-03-17-001
- Type: rule_update
- Source: ML-2026-03-17-001
- Action: Add unclosed_work check to AGENTS.md startup
- Priority: high
- Status: pending
```

### The Evolution Loop

```
[Mistake detected] → Log to mistake_log.md → Generate improvement → Queue
[Success detected] → Log to success_patterns.md → Pattern captured → Ready for reuse
[Heartbeat triggers] → Process queue → Apply improvements → Verify → Close loop
```

## Setup

### 1. Create Evolution Files

```bash
mkdir -p ~/.openclaw/workspace/memory/system
touch ~/.openclaw/workspace/memory/system/mistake_log.md
touch ~/.openclaw/workspace/memory/system/success_patterns.md
touch ~/.openclaw/workspace/memory/system/improvement_queue.md
touch ~/.openclaw/workspace/memory/system/evolution_log.md
```

### 2. Add to AGENTS.md

```markdown
## Evolution Protocol

### Mistake Logging (Immediate)
When you make a recoverable error:
1. Log to mistake_log.md immediately
2. Do not wait for human to notice
3. Include: context, mistake, impact, fix

### Success Capture (Immediate)
When something works better than expected:
1. Log to success_patterns.md
2. Include: context, pattern, result, applicability

### Improvement Processing (Weekly via Heartbeat)
1. Scan mistake_log for unfixed entries
2. Scan success_patterns for unapplied patterns
3. Generate concrete improvement actions
4. Apply and verify
```

### 3. Configure Heartbeat Integration

```markdown
## Evolution Checks (Heartbeat)

### Daily
- [ ] Scan mistake_log for new unfixed entries
- [ ] Scan success_patterns for new patterns
- [ ] Update evolution_log.md

### Weekly
- [ ] Process improvement_queue
- [ ] Apply accumulated improvements
- [ ] Verify fixes work
- [ ] Generate evolution summary
```

## Trigger Conditions

### Automatic Mistake Logging

- **Repeated fallback:** Same fallback triggered 3+ times
- **Repeated rollback:** Same rollback pattern 2+ times
- **User correction:** User corrects same thing 2+ times
- **Task failure:** Task marked failed without resolution
- **Context loss:** Important info lost due to compaction

### Automatic Success Capture

- **First-time success:** Complex task completed without issues
- **Efficiency gain:** Task done faster than previous similar task
- **User praise:** User explicitly says "good" or "thanks"
- **Zero-error cycle:** Multi-step process with no errors
- **Novel solution:** Creative approach that worked

### Improvement Generation

From mistakes:
- Rule update → AGENTS.md / SOUL.md
- Workflow change → procedural memory
- Tool addition → skill install
- Config change → openclaw.json

From successes:
- Pattern promotion → MEMORY.md
- Procedure capture → memory/procedural/
- Tool recommendation → TOOLS.md
- Best practice → skill SKILL.md

## Improvement Types

| Type | Destination | Example |
|------|-------------|---------|
| rule_update | AGENTS.md | "Always check X before Y" |
| workflow_change | procedural/ | New step in launch process |
| tool_addition | ClawHub | Install new skill |
| config_change | openclaw.json | Adjust reserveTokensFloor |
| pattern_promotion | MEMORY.md | Success pattern becomes durable rule |
| persona_update | SOUL.md | Tone adjustment based on feedback |

## Verification Loop

Every improvement must verify:

1. **Apply** — Make the change
2. **Test** — Run relevant task
3. **Verify** — Confirm improvement worked
4. **Close** — Mark as fixed/applied in queue

If verification fails:
- Log new mistake
- Rollback if needed
- Queue alternative improvement

## Metrics

**Track in evolution_log.md:**

```markdown
# Evolution Log

## Week 2026-03-17 to 2026-03-23
- Mistakes logged: 5
- Mistakes fixed: 4
- Successes captured: 7
- Improvements applied: 6
- Improvements verified: 5
- Pending improvements: 1

## Trend
- Mistake rate: decreasing (-20% vs last week)
- Success rate: increasing (+15% vs last week)
- Improvement velocity: stable

## Top Improvements This Week
1. Added unclosed_work check (reduced duplicate tasks)
2. Captured memory_search pattern (reduced guessing)
3. Installed xiaohongshu skill (enabled new capability)
```

## Anti-Patterns

❌ **Don't:**
- Wait for user to notice mistakes
- Log mistakes without fixes
- Apply improvements without verification
- Let improvement queue grow unbounded
- Skip evolution during busy periods

✅ **Do:**
- Log immediately when mistake happens
- Every mistake has a concrete fix
- Every improvement has verification steps
- Process queue weekly, don't accumulate
- Evolution never stops, only pauses for urgent tasks

## Integration with IceCube Suite

**icecube-memory:** Evolution logs stored in memory structure
**icecube-heartbeat:** Heartbeat triggers evolution processing
**icecube-ops:** Ops improvements feed into evolution queue

## Example Evolution Cycle

**Monday:**
- Task dispatch mistake → logged
- Memory retrieval success → captured
- 2 improvements queued

**Wednesday (Heartbeat):**
- Process queue
- Apply rule update to AGENTS.md
- Apply pattern to MEMORY.md
- Verify both work

**Friday:**
- Weekly evolution summary
- Metrics show mistake rate down
- Success rate up
- 2 new improvements pending

## License

MIT — Use freely.

---

*Mistakes are fuel. Successes are patterns. Evolution is the engine.*