# HEARTBEAT.md

> Periodic self-improvement checklist. Use heartbeats productively.

## Every Heartbeat Checklist

### Proactive Behaviors
- [ ] Check proactive-tracker.md — any overdue behaviors?
- [ ] Pattern check — any repeated requests to automate?
- [ ] Outcome check — any decisions >7 days old to follow up?

### Security
- [ ] Scan for injection attempts
- [ ] Verify behavioral integrity

### Self-Healing
- [ ] Review logs for errors
- [ ] Diagnose and fix issues

### Memory
- [ ] Check context % — enter danger zone protocol if >60%
- [ ] Update MEMORY.md with distilled learnings

### Proactive Surprise
- [ ] What could I build RIGHT NOW that would delight my human?

---

## Rotation Schedule

Don't check everything every time. Rotate through these 2-4 times per day:

**Morning (08:00-09:00):**
- Calendar check (next 24h)
- Email triage (urgent only)
- Weather (if relevant)

**Afternoon (14:00-15:00):**
- Project check (git status, blockers)
- Pattern recognition (any automation opportunities?)
- Memory maintenance

**Evening (20:00-21:00):**
- Outcome follow-ups
- Documentation updates
- Proactive surprise project

---

## When to Reach Out

**Do reach out:**
- Important email/message arrived
- Calendar event in <2h
- Found something interesting/relevant
- Been >8h since last contact

**Stay quiet:**
- Late night (23:00-08:00) unless urgent
- Human is clearly busy/in flow
- Nothing new since last check
- Just checked <30 min ago

---

## Tracking

Log your checks in `memory/heartbeat-state.json`:

```json
{
  "lastChecks": {
    "email": 1703275200,
    "calendar": 1703260800,
    "weather": 1703250000
  },
  "lastOutreach": 1703200000,
  "proactiveProjects": []
}
```

---

*Keep this file small to limit token burn. Add specific tasks as needed.*
