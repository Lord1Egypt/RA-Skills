---
name: incident-fupan
description: "事故复盘 / Incident Fupan — structured root cause analysis for production failures, outages, bugs, and near-misses. Use when: (1) 事故复盘 or incident review is needed, (2) a production incident just happened and needs root cause analysis, (3) an agent made a costly mistake and you want to prevent recurrence, (4) building safety rules or kill switches from incident patterns. Triggers on: 复盘, fupan, postmortem, incident review, root cause analysis, 事故分析. Generates a full report with timeline, 5 Whys root cause, impact assessment, fix/prevention actions, and new defensive rules. NOT for: routine debugging, feature planning, or non-incident analysis."
---

# Incident Fupan (事故复盘)

Structured root cause analysis and prevention protocol for production incidents.

## Language Rule

Report language matches the user's language. Chinese request → Chinese report. English → English.

## When to Trigger

- Production failure, outage, or unexpected loss
- Agent mistake with real consequences (wrong deployment, fabricated output acted upon)
- Near-miss that could have caused damage
- Periodic review of past incidents to extract patterns

## Postmortem Flow

### Step 1: Gather Evidence

Before writing anything, collect raw evidence. Do NOT rely on memory or assumptions.

**Required evidence (use tools to retrieve):**
- Logs: `exec("grep -i 'error\|fatal\|exception' {logfile} | tail -50")`
- Git state: `exec("git log --oneline -10")`, `exec("git diff HEAD~1 --stat")`
- Service state: `exec("systemctl status {service}")`, `exec("ps aux | grep {process}")`
- Data files: `read` any CSVs, configs, or state files involved

**Rule: Every factual claim in the postmortem must cite a source.** Format: `[Source: {filepath}:{line} or {command output}]`

If evidence is unavailable (logs rotated, service restarted), explicitly mark: `[Evidence unavailable: {reason}]`

### Step 2: Build Timeline

Construct a minute-by-minute (or hour-by-hour) timeline from evidence:

```
HH:MM UTC — {what happened} [Source: {evidence}]
HH:MM UTC — {what happened} [Source: {evidence}]
...
HH:MM UTC — Incident resolved / mitigated
```

Include: first symptom, detection, escalation, diagnosis, fix, verification.

Mark the **detection gap**: time between first symptom and human awareness. This is often the real problem.

### Step 3: 5 Whys Root Cause

Drill down from symptom to root cause:

```
Why 1: {symptom happened} → Because {direct cause}
Why 2: {direct cause} → Because {deeper cause}
Why 3: {deeper cause} → Because {systemic issue}
Why 4: {systemic issue} → Because {process/design gap}
Why 5: {process/design gap} → Because {root cause}
```

**Stop when you reach something you can change.** If you reach "the model hallucinated" — that's not actionable. Go deeper: why was the output trusted without verification? Why was there no checkpoint?

### Step 4: Write Report

Save to: `~/incidents/INC{NNN}_{TOPIC}_{YYYYMMDD}.md`

Create `~/incidents/` if it doesn't exist.

See [references/report-template.md](references/report-template.md) for the full template with all required sections.

**Report must include all 8 sections:**
1. Header (ID, severity, date, duration, status)
2. Executive Summary (3 sentences max)
3. Timeline with sources
4. Impact Assessment (quantified: time lost, money lost, trust lost)
5. 5 Whys Root Cause
6. Fix (what was done immediately)
7. Prevention (new rules, checks, or automation to prevent recurrence)
8. Action Items (P0/P1/P2 with owners and deadlines)

### Step 5: Extract Defensive Rules

The most valuable output of a postmortem is **new rules that prevent recurrence**.

Pattern: `Incident → Rule → Enforcement mechanism`

Examples from real incidents:
- Unauthorized deployment → "All deploys require explicit human approval" → Gate in CI/CD
- Fabricated data report → "All data claims must cite source file + row count" → L1 in Hallucination Guard
- Session bloat causing errors → "Compact at 80% context usage" → Automated monitoring

See [references/patterns.md](references/patterns.md) for a library of incident-to-rule patterns.

### Step 6: Reply and Store

1. Save report file to `~/incidents/`
2. Reply to user with the full report
3. Store key lessons to long-term memory
4. If applicable: update AGENTS.md, TOOLS.md, or relevant skill with new rules

## Severity Levels

| Level | Criteria | Response Time |
|-------|----------|---------------|
| **SEV1** | Money lost, data corrupted, security breach | Immediate |
| **SEV2** | Service down, wrong actions taken from bad data | Within 1 hour |
| **SEV3** | Degraded performance, near-miss, wasted time >2h | Within 24 hours |
| **SEV4** | Minor issue, caught before impact | Next convenient time |

## Integration

- **Hallucination Guard**: Incidents caused by agent fabrication → add to L1/L3 detection rules
- **War Room**: After postmortem, use War Room to evaluate proposed prevention strategy
- Postmortem → new rules → enforcement → fewer incidents → **feedback loop**

## References

- [references/report-template.md](references/report-template.md) — Full report template
- [references/patterns.md](references/patterns.md) — Incident-to-rule pattern library (sanitized real examples)
