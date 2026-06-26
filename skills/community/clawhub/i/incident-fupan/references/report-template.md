# Postmortem Report Template

Save to: `~/incidents/INC{NNN}_{TOPIC}_{YYYYMMDD}.md`

```markdown
# Incident Postmortem: INC{NNN} — {Title}

**Incident ID**: INC{NNN}
**Severity**: SEV{1-4}
**Date**: {YYYY-MM-DD}
**Duration**: {detection to resolution}
**Detection Gap**: {first symptom to human awareness}
**Status**: Resolved / Mitigated / Ongoing
**Author**: {who wrote this postmortem}

---

## I. Executive Summary

{3 sentences max: what happened, what was the impact, what was the root cause.}

## II. Timeline

| Time (UTC) | Event | Source |
|------------|-------|--------|
| HH:MM | First symptom: {description} | {log/file/observation} |
| HH:MM | Detection: {who/what noticed} | {alert/human/monitoring} |
| HH:MM | Escalation: {who was notified} | {channel/method} |
| HH:MM | Diagnosis: {root cause identified} | {investigation method} |
| HH:MM | Fix applied: {what was done} | {commit/command/action} |
| HH:MM | Verified: {confirmed resolved} | {test/monitoring} |

## III. Impact Assessment

| Dimension | Quantified Impact |
|-----------|-------------------|
| **Financial** | ${amount} lost / at risk |
| **Time** | {hours} of human time wasted |
| **Time** | {hours} of agent time wasted |
| **Trust** | {what confidence was damaged} |
| **Downstream** | {actions taken based on bad info, if any} |

If no financial loss: state explicitly. Near-misses still get impact assessment on "what would have happened."

## IV. Root Cause Analysis (5 Whys)

```
Why 1: {symptom} → Because {cause}
Why 2: {cause} → Because {deeper cause}
Why 3: {deeper cause} → Because {systemic issue}
Why 4: {systemic issue} → Because {process gap}
Why 5: {process gap} → Because {root cause}
```

**Root Cause Category**: {Human Error / Design Flaw / Missing Safeguard / Agent Hallucination / External Dependency / Configuration Error}

**Contributing Factors** (not root cause, but made it worse):
- {factor 1}
- {factor 2}

## V. Immediate Fix

What was done to stop the bleeding:
- {action 1} [commit: {hash} / command: {cmd}]
- {action 2}

Was the fix verified? {Yes — how / No — why not}

## VI. Prevention

New rules or mechanisms to prevent recurrence:

| # | Rule | Enforcement | Origin |
|---|------|-------------|--------|
| 1 | {new rule} | {how enforced: automation/checklist/skill} | This incident |
| 2 | {new rule} | {how enforced} | This incident |

**Key question**: If the same situation happens again tomorrow, will these rules catch it before damage occurs?

If the answer is "no" or "maybe" — the prevention is insufficient. Add more layers.

## VII. Retained Doubts

{Things we're still not sure about — mandatory section}
- {uncertainty 1}
- {uncertainty 2}

## VIII. Action Items

| Priority | Task | Owner | Deadline | Status |
|----------|------|-------|----------|--------|
| P0 | {immediate} | {who} | {when} | |
| P1 | {this week} | {who} | {when} | |
| P2 | {this month} | {who} | {when} | |
```

## Quality Checklist

Before finalizing, verify:

- [ ] Every timeline entry has a source citation
- [ ] Impact is quantified (not "some loss" — actual numbers)
- [ ] 5 Whys reaches an actionable root cause (not "the model hallucinated")
- [ ] Prevention rules have enforcement mechanisms (not just "be more careful")
- [ ] At least one retained doubt exists (no incident is fully understood)
- [ ] Action items have owners and deadlines (not "TBD")
