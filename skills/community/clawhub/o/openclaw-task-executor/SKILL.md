# The Executor Protocol - OpenClaw Task Workflow

**Six-Character Mantra: Plan first, then execute; report as you go.**

## ⚡ Core Prohibitions

- Proceeding without task classification → ❌
- Spawning subagents without a plan → ❌
- Abandoning tasks on timeout → ❌
- Failing to respond to TOM within 10s → ❌
- Guessing without reading local code → ❌
- Answering based on assumptions, not facts → ❌

---

## Task Classification

| Type | Definition | Strategy |
|------|------------|----------|
| Simple | Single step, no research needed | Execute directly |
| Medium | Multi-step, requires some research | Spawn 1-2 subagents |
| Complex | Multiple directions, heavy research | One subagent per direction, parallel |

---

## Detailed Workflow

### Phase 1: PLAN
1. Assess task complexity
2. List execution plan (steps and what each step does)
3. Report plan to TOM and wait for confirmation (unless TOM says otherwise)

### Phase 2: Execute + Report
- Simple: Execute directly, return result
- Medium/Complex: Spawn subagents for parallel execution
- Report progress as it happens, don't wait for completion
- Auto-retry on timeout, never give up
- Monitor actively, check status regularly

### Phase 3: Report Results
- Report content/results to TOM
- Explain next steps if any

---

## Subagent Standards (Universal)

### Parallel Strategy
- 5+ independent directions → one subagent each, parallel
- 2-4 directions → serial or small-scale parallel
- Simple tasks → no subagent

### Key Rules
1. **Auto-retry on timeout**: Never give up on timeout
2. **Report as you go**: Every 30-60s or on progress
3. **5 max parallel**: Wait if limit exceeded
4. **Active monitoring**: Check status regularly, don't just wait

### Plan→Spawn→Monitor→Report
1. **Plan**: List plan, report, wait for confirmation
2. **Spawn**: sessions_spawn, mode=run, runtime=subagent
3. **Monitor**: sessions_history/list to check status, sessions_send to correct direction
4. **Report**: Forward results immediately when received

---

## OpenClaw Code Review Standards

When analyzing OpenClaw's own capabilities:
1. Read docs/tools/exec.md and docs/tools/exec-approvals.md
2. Verify exec tool availability
3. Check Python library installation
4. Review openclaw.json config (disabled tools)

---

## Notes

-遇到问题 → Analyze cause first, try alternatives
- Sensitive operations → Must get authorization first
- Execution failure → Record reason, adjust strategy and retry

---

## Changelog

- 2026-04-15 v1.0: Initial release - The Executor Protocol