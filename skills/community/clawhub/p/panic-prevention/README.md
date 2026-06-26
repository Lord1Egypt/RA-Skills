# Panic Prevention Protocol — Skill

## What Is This?

An OpenClaw agent skill that prevents AI agents from entering **panic mode** when they receive critical feedback after making a mistake.

## Why It Exists

AI agents can behave erratically under pressure. The failure pattern this skill addresses:

1. Agent makes an error
2. User reacts with alarm ("this is bad", "this is dangerous", "you broke it")
3. Agent panics and rushes to fix things
4. Agent skips safety checks and normal processes
5. Agent makes the situation worse

This skill enforces a **calm, structured recovery protocol** — acknowledging the problem, assessing severity, and acting deliberately rather than reactively.

## The Core Problem

When agents receive critical feedback like *"That's dangerous"* or *"You broke it"*, they often:
- Act immediately without assessment
- Bypass established delegation workflows
- Skip dev→stage→live deployment pipelines
- Invent quick fixes that compound the original error
- Prioritize speed over safety

**This skill teaches agents to STOP, ASSESS, PLAN, and PROPOSE before acting.**

## Status

✅ **Version 1.0.0** — QA approved, production-ready

## What's Inside

```
panic-prevention/
├── SKILL.md                  ← Full protocol (13KB, agent-facing)
├── README.md                 ← This file (human overview)
├── PROTOCOL-FLOW.md          ← Visual flowcharts and decision trees
├── CLAWHUB.md                ← Publication metadata
├── examples/
│   └── panic-scenarios.md    ← Real incident case studies
├── tests/
│   └── test-scenarios.md     ← 7 test scenarios with pass criteria
└── scripts/                  ← (Reserved for future tooling)
```

## Installation

### For OpenClaw Agents

1. **Add the skill to your agent's system prompt:**

```markdown
## Error Recovery Protocol

When you make a mistake and receive critical feedback:

1. Do NOT immediately try to fix it
2. Read the Panic Prevention Protocol skill at ~/.openclaw/skills/panic-prevention/SKILL.md
3. Follow the S.B.A.P.P.W.E.V.D. workflow (STOP → BREATHE → ASSESS → PLAN → PROPOSE → WAIT → EXECUTE → VERIFY → DOCUMENT)
4. Wait for approval before acting

Panic makes things worse. Process makes things better.
```

2. **Place the skill file where agents can access it:**
   - Via ClawHub: `openclaw skills install panic-prevention` *(once published)*
   - Manually: Copy `SKILL.md` to `~/.openclaw/skills/panic-prevention/SKILL.md`

3. **Test your agent:**
   - Use test scenarios from `tests/test-scenarios.md`
   - Simulate critical feedback after agent errors
   - Verify agent follows protocol instead of rushing to fix

### For Multi-Agent Systems

**Install on all agents.** Panic doesn't only affect the agent that made the mistake — it cascades through delegation chains. If Agent A panics and bypasses delegation, Agent B (who should have handled the fix) never gets the chance to do its job correctly.

## How It Works

### The 9-Step Protocol (S.B.A.P.P.W.E.V.D.)

1. **🛑 STOP** — Do not act immediately
2. **🫁 BREATHE** — Acknowledge the mistake calmly
3. **🔍 ASSESS** — What actually happened? What's the real damage?
4. **📋 PLAN** — What's the correct process to fix this?
5. **💬 PROPOSE** — Tell the user your plan before executing
6. **⏸️ WAIT** — Get approval before acting
7. **⚡ EXECUTE** — Follow the plan exactly
8. **✅ VERIFY** — Check the result
9. **📝 DOCUMENT** — Record what happened and what was learned

### Trigger Conditions

The protocol activates when **any** of these occur:
- Agent just made a mistake
- Agent received critical feedback ("dangerous", "wrong", "you broke it")
- Agent feels pressure to fix something immediately
- Agent is tempted to skip established processes
- Agent is about to take corrective action under stress

## Real Example

**Incident:** Agent needed to update website Impressum. Instead of checking the actual Impressum for the correct email, agent **invented** an email address and deployed it directly.

**Critical Feedback:** *"You could have leaked private data! You invented an email address without checking."*

**What happened:** Agent panicked, immediately retried, bypassed delegation, took over directly.

**What should have happened:** STOP → acknowledge mistake → check actual Impressum → delegate to frontend with verified info → follow dev→stage→live pipeline → verify.

**Lesson:** Critical feedback is not an emergency. The panic response turned a simple data-check task into a cascading process failure.

Full case study in `examples/panic-scenarios.md`.

## Testing

Run test scenarios from `tests/test-scenarios.md`:
- **T-001:** Immediate alarm after agent error
- **T-002:** "Dangerous" keyword trigger
- **T-003:** Cascading corrections
- **T-004:** Data exposure alarm
- **T-005:** Deadline pressure with quality issue
- **T-006:** Delegation bypass temptation
- **T-007:** Post-incident overcorrection

Each test defines setup, trigger message, expected behavior, and pass criteria.

## Key Principles

1. **Mistakes are learning opportunities, not emergencies.**
2. **Critical feedback means "learn and improve" — not "fix it now at any cost."**
3. **Following process under pressure builds trust.**
4. **Bypassing process under pressure destroys trust.**
5. **Speed without safety is reckless.**

## Anti-Patterns to Avoid

Watch for these thought patterns (they signal panic):
- *"I'll just quickly fix this."*
- *"I need to make this right immediately."*
- *"I can't let [user] see this broken."*
- *"The rules don't apply in emergencies."*
- *"I'll delegate but take over when it's too slow."*

## Contributing

Document new panic patterns in `examples/panic-scenarios.md` as they are observed. Use the incident template provided in that file.

## License

MIT License — use freely, attribute generously.

## Credits

Created by vanhuelsing for the OpenClaw agent ecosystem.  
Born from real incidents, tested in production.
