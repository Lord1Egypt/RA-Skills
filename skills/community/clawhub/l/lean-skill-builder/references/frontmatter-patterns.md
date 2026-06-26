# Frontmatter Patterns

Keep frontmatter sharp. The description is the trigger surface.

## Minimum viable frontmatter

```yaml
---
name: skill-name
description: >
 One or two sentences describing what the skill does, when to use it,
 and the kinds of requests that should trigger it.
---
```

Use extra fields only when they match the local style and clearly help. Do not pad.

## Naming guidance

- use lowercase hyphen-case
- prefer short, concrete names
- name for the job, not the aspiration
- avoid vague labels like `workflow-manager` or `universal-helper`

Good:
- `skill-builder`
- `cron-doctor`
- `openclaw-guide`

Weak:
- `skill-system`
- `meta-skill-orchestrator`
- `general-automation-framework`

## Description pattern

A strong description usually covers:
1. **what it does**
2. **when to use it**
3. **what kinds of phrases or tasks should trigger it**

### Simple pattern

```yaml
---
name: example-skill
description: >
 [Primary job]. Use when [situation]. Helps with [2-4 concrete tasks or trigger phrases].
---
```

### Example

```yaml
---
name: skill-builder
description: >
 Decide whether work should become a skill, stay a plain edit, use an existing tool,
 or be delegated to a subagent. Use when creating a new skill, trimming an existing one,
 or auditing a skill for bloat, stale instructions, or unclear triggers.
---
```

## Write pushy descriptions

LLMs tend to under-trigger skills — they default to handling things directly even
when a skill would produce better results. To counter this, make descriptions
slightly aggressive about when to fire.

**Instead of:**
```yaml
description: >
 How to build a dashboard to display internal data.
```

**Write:**
```yaml
description: >
 How to build a dashboard to display internal data. Use this skill whenever the
 user mentions dashboards, data visualization, internal metrics, or wants to
 display any kind of data, even if they don't explicitly ask for a "dashboard."
```

The goal is not to lie about what the skill does — it is to ensure the skill
triggers on natural phrasings that a human would recognize but a literal keyword
match might miss.

### Pushy description checklist

- [ ] Does the description include 3-5 concrete trigger phrases?
- [ ] Does it cover casual/informal ways a user might ask for this?
- [ ] Does it mention adjacent concepts the skill handles?
- [ ] Does it say "even if they don't explicitly ask for X" where appropriate?

## Description quality checks

Good descriptions are:
- specific enough to trigger correctly
- broad enough to catch normal phrasings
- honest about scope
- free of hype
- slightly pushy about when to trigger (see above)

Bad signs:
- no clue when to use it
- promises implementation, review, deployment, and governance all at once
- stuffed with internal jargon
- so narrow it only matches one exact sentence
- so conservative that it only triggers on the skill's literal name

## Scope wording

It is often worth adding a short body section for:
- **Use when**
- **Do not use when**

This keeps the description clear without cramming everything into frontmatter.
