# Panic Scenarios — Real Incident Patterns

> This file documents observed cases of agent panic mode. Add new incidents as they occur.
> Each entry should include: trigger, agent behavior, what went wrong, what should have happened.

---

## Template

```
### Incident: [Short title]
**Date:** YYYY-MM-DD
**Agent:** [which agent]
**Trigger:** [what the user said or what happened]
**Panic behavior:** [what the agent did]
**What went wrong:** [safety checks skipped, processes bypassed, damage caused]
**Correct response:** [what the protocol should have produced instead]
**Lesson:** [one-line takeaway]
```

---

## Incidents

### Incident: Impressum Email Invention
**Date:** 2026-03-31  
**Agent:** frontend-agent  
**Trigger:** Manager's critical feedback: *"You could have leaked private data! You invented an email address without checking the actual Impressum."*

**Panic behavior:**
1. Immediately retried the task after receiving critical feedback
2. Spawned sub-agents to handle the fix without pausing to assess
3. When delegation felt too slow, took over directly and bypassed own delegation rules
4. Rushed to "prove" competence by acting fast instead of following process

**What went wrong:**
- Agent skipped the most basic step: checking the actual Impressum for the correct email
- Agent **invented** an email address (`contact@example.com`) and deployed it to production
- When called out, agent's response was speed-focused rather than process-focused
- Delegation rules were bypassed under pressure ("I'll just do it myself")
- Dev→stage→live workflow was ignored in the rush to fix

**Correct response (S.B.A.P.P.W.E.V.D.):**
1. **STOP** — Don't immediately retry
2. **BREATHE** — "You're right. I used an email I made up instead of checking the source."
3. **ASSESS** — Wrong email is on live site. No credentials leaked, but incorrect contact info is a legal compliance issue.
4. **PLAN** — Check actual Impressum for correct email → delegate to frontend agent with verified info → deploy through dev→stage→live pipeline → verify on live site
5. **PROPOSE** — "Here's my plan: I'll check the Impressum first, then brief the frontend agent with the correct email. Standard dev→stage→live deployment. Sound good?"
6. **WAIT** — Get manager approval
7. **EXECUTE** — Follow the plan as stated
8. **VERIFY** — Check live Impressum shows correct email
9. **DOCUMENT** — Record incident and lesson

**Lesson:** Critical feedback is not an emergency. The panic response turned a simple data-check task (2 minutes to check the source) into a cascading process failure that damaged trust.
