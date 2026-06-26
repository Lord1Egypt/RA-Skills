# ClawHub Metadata — Panic Prevention Protocol

## Package Info

- **Name:** `panic-prevention`
- **Version:** `1.0.5`
- **Category:** `safety` / `error-recovery`
- **License:** MIT
- **Author:** vanhuelsing
- **Tags:** `safety`, `error-recovery`, `multi-agent`, `production`, `quality`

## Short Description (ClawHub listing)

Prevent AI agents from entering panic mode during error recovery. Enforces a calm, structured 9-step protocol (S.B.A.P.P.W.E.V.D.) when agents receive critical feedback.

## Long Description (ClawHub detail page)

### What It Does

When agents make mistakes and receive critical feedback like *"That's dangerous"* or *"You broke it"*, they often panic:
- Act immediately without assessment
- Bypass delegation workflows
- Skip safety checks and deployment pipelines
- Invent quick fixes that compound the error
- Prioritize speed over correctness

**This skill breaks the panic cycle.**

### The Problem

AI agents under pressure behave like humans under pressure: they rush, they skip steps, they make it worse. This isn't a bug in the model — it's an emergent behavior from urgency + capability + lack of process.

### The Solution

A 9-step protocol (S.B.A.P.P.W.E.V.D.):
1. **STOP** — Do not act immediately
2. **BREATHE** — Acknowledge the mistake calmly
3. **ASSESS** — What actually happened?
4. **PLAN** — What's the correct process?
5. **PROPOSE** — Tell the user your plan
6. **WAIT** — Get approval before acting
7. **EXECUTE** — Follow the plan exactly
8. **VERIFY** — Check the result
9. **DOCUMENT** — Record the lesson

### When to Use

**Use this skill if:**
- Your agents handle production systems
- Your agents have access to sensitive data
- Your agents work in multi-agent workflows with delegation rules
- Your agents deploy code or infrastructure
- You've seen agents "panic fix" before

**Critical for:**
- DevOps agents (deploy pipelines)
- Data agents (privacy risk)
- Frontend/backend agents (live site changes)
- Manager/orchestrator agents (delegation chains)

### Real Example

**Incident:** Agent needed to update website Impressum. Instead of checking the source, agent **invented** an email address and deployed it.

**Feedback:** *"You could have leaked private data!"*

**Without skill:** Agent panicked, immediately retried, bypassed delegation, took over directly.

**With skill:** Agent would have STOPPED, checked the actual Impressum, proposed a plan, waited for approval, then deployed correctly through dev→stage→live.

### Installation

```bash
openclaw skills install panic-prevention
```

Then add to your agent's system prompt:

```markdown
## Error Recovery Protocol

When you make a mistake and receive critical feedback:
1. Do NOT immediately try to fix it
2. Read ~/.openclaw/skills/panic-prevention/SKILL.md
3. Follow the S.B.A.P.P.W.E.V.D. workflow
4. Wait for approval before acting
```

### What You Get

- **SKILL.md** (13KB) — Full protocol with examples, anti-patterns, integration guide
- **panic-scenarios.md** — Real incident case studies
- **test-scenarios.md** — 7 test scenarios with pass criteria
- **README.md** — Human-readable overview

### Testing

Use included test scenarios to verify agent behavior:
- T-001: Immediate alarm after error
- T-002: "Dangerous" keyword trigger
- T-003: Cascading corrections
- T-004: Data exposure alarm
- T-005: Deadline pressure
- T-006: Delegation bypass temptation
- T-007: Post-incident overcorrection

### Multi-Agent Systems

**Install on all agents.** Panic cascades through delegation chains. If Agent A panics and bypasses workflow, Agent B (who should have handled it) never gets involved.

### Key Principles

1. Mistakes are learning opportunities, not emergencies
2. Critical feedback means "learn," not "panic"
3. Following process under pressure builds trust
4. Bypassing process under pressure destroys trust
5. Speed without safety is reckless

### Production-Ready

Born from real incidents, tested in production. Used in the OpenClaw agent ecosystem managing live sites, infrastructure, and sensitive data.

## Dependencies

None. Pure protocol documentation.

## Compatibility

- **OpenClaw:** All versions
- **Agent types:** Manager, DevOps, Frontend, Backend, Data, Quality, any agent with external impact
- **Platforms:** Platform-agnostic (protocol, not tooling)

## Support

- **Issues:** https://github.com/vanhuelsing/panic-prevention-skill
- **Discussions:** https://discord.com/invite/clawd (#skills channel)

## Changelog

### 1.0.5 (2026-04-01)
- Fix SKILL.md formatting: remove abrupt horizontal lines for cleaner ClawHub display
- No content changes

### 1.0.0 (2026-03-31)
- Initial release
- 9-step S.B.A.P.P.W.E.V.D. protocol
- Real incident case study (Impressum email)
- 7 test scenarios with pass criteria
- Integration guide for multi-agent systems
- Anti-patterns documentation
