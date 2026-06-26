# Suggestion Templates

Templates used by `generate_suggestions.py` to produce actionable output.
Each suggestion type has a specific format designed to be immediately usable.

---

## Cron Job Suggestion

When a time-correlated or high-frequency pattern is detected:

```markdown
## 🔄 Suggested Cron Job: [Title]

**Confidence:** X% | **Type:** cron

[Description of what was detected and why it's schedulable]

**Evidence:**
- YYYY-MM-DD: [Section name from memory]
- YYYY-MM-DD: [Section name from memory]
- YYYY-MM-DD: [Section name from memory]

**Suggested schedule:** [human-readable, e.g., "weekly on Monday at 10:00 AM ET"]

**Ready-to-approve cron definition:**
```json
{
  "name": "Auto: [Title]",
  "schedule": {"kind": "cron", "expr": "0 10 * * 1", "tz": "America/New_York"},
  "payload": {
    "kind": "agentTurn",
    "message": "[What the cron should do]"
  }
}
```

The cron definition follows OpenClaw's jobs.json format and can be
registered directly via `openclaw cron create`.
```

---

## Skill Suggestion

When a multi-step workflow repeats:

```markdown
## 🛠️ Suggested Skill: [Title]

**Confidence:** X% | **Type:** skill

[Description of the recurring workflow]

**Evidence:**
- YYYY-MM-DD: [Section name]
- YYYY-MM-DD: [Section name]

**Draft SKILL.md:**
```yaml
---
name: [skill-name]
description: "[One-line description with trigger words]"
---
```

# [Skill Name]

## Workflow
1. [Step extracted from pattern]
2. [Step]
3. [Step]

## When to Use
Trigger phrases: [keywords from cluster]
```

Draft skills are starting points — the agent should refine them
before creating the actual skill directory.
```

---

## Workflow Shortcut Suggestion

When a pattern doesn't need full automation but could use a saved prompt:

```markdown
## ⚡ Workflow Shortcut: [Title]

**Confidence:** X% | **Type:** workflow

[Description of the recurring pattern]

**Suggested saved prompt:** `[Composite prompt that chains the steps]`

**Key components:** keyword1, keyword2, keyword3
```

Workflow shortcuts are lighter than skills — just a suggested way
to invoke a common pattern in fewer words.
```

---

## Proactive Monitoring Suggestion

When something gets checked manually many times:

```markdown
## 👁️ Suggested Monitor: [Target]

**Confidence:** X% | **Type:** monitor

[Description of what keeps getting checked]

**Target:** [What to monitor]
**Frequency:** [How often]

**Ready-to-approve cron definition:**
```json
{
  "name": "Monitor: [Target]",
  "schedule": {"kind": "cron", "expr": "0 */6 * * *", "tz": "America/New_York"},
  "payload": {
    "kind": "agentTurn",
    "message": "Check on [target] — automated monitoring. Report any issues."
  }
}
```

Monitor suggestions include a cron definition but also flag that
the agent should only report on failures or notable changes —
not send "everything is fine" messages every 6 hours.
```

---

## Suggestion Lifecycle

Every suggestion tracks its state:

| State | Meaning | Re-surface? |
|-------|---------|-------------|
| `pending` | Just generated, not yet shown to user | Yes (next report) |
| `suggested` | Shown to user, awaiting response | No (wait for response) |
| `accepted` | User approved, should be implemented | Track implementation |
| `rejected` | User declined | Only at 0.80+ confidence |
| `snoozed` | User wants to defer | After 30 days or confidence +0.20 |

### State Transitions

```
pending → suggested → accepted → (tracked)
                    → rejected → (dormant, high bar to resurface)
                    → snoozed  → pending (after cooldown)
```

The agent manages transitions by calling state.py functions:
- `update_suggestion(state, id, "accepted")`
- `update_suggestion(state, id, "rejected", reason="not useful right now")`
- `update_suggestion(state, id, "snoozed")`
