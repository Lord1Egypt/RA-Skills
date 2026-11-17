<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-UXD
generatedVersion: "{version}"
source: "{upstream-doc-path}"
generatedOn: "{ISO-date}"
ownership: hybrid
---

# Voice & Tone Guidelines

## Brand Voice (Constant Across Contexts)

| Dimension | Our Position | What This Sounds Like |
|-----------|:------------:|----------------------|
| Formal ← → Casual | {1-5 position} | {example sentence} |
| Serious ← → Playful | {1-5 position} | {example sentence} |
| Technical ← → Simple | {1-5 position} | {example sentence} |
| Authoritative ← → Friendly | {1-5 position} | {example sentence} |

### Voice Principles

1. **{Principle 1}** — {what it means in practice}
2. **{Principle 2}** — {what it means}
3. **{Principle 3}** — {what it means}

---

## Tone Shifts by Context

| Context | Tone Adjustment | Why | Example |
|---------|----------------|-----|---------|
| **Success** | Warm, brief, encouraging | User accomplished their goal — celebrate briefly, suggest next | "{Confirmation}. {Next step suggestion}." |
| **Error** | Empathetic, helpful, specific | User is frustrated — don't blame, help fix | "We couldn't {action}. {Specific cause}. {How to fix}." |
| **Empty state** | Encouraging, guiding | User sees nothing — orient and motivate | "{What belongs here}. {One action to start}." |
| **Loading** | Calm, informative | User is waiting — set expectation | "{What's happening}..." |
| **Onboarding** | Welcoming, minimal | User is new — don't overwhelm | "{What this is}. {One thing to try first}." |
| **Destructive** | Serious, clear, specific | User is about to lose something — be unambiguous | "{Consequence statement}. This can't be undone. [{Verb}] [Cancel]" |
| **Confirmation** | Clear, consequence-focused | User must decide — present facts without bias | "{What will happen if you proceed}. [{Action verb}] [Cancel]" |
| **Help/tooltip** | Concise, task-focused | User needs quick guidance — one sentence max | "{What this does or means}" |
| **Placeholder** | Instructive, example-driven | User needs to know what to enter | "{Format hint or example}" |

---

## Microcopy Patterns

### Buttons & CTAs

| Pattern | Structure | Good Example | Bad Example |
|---------|-----------|-------------|------------|
| Primary action | {Verb} + {Object} | "Create Report" | "Submit" / "OK" |
| Secondary action | {Verb} + {Object} | "Save as Draft" | "Save" (ambiguous) |
| Cancel | "Cancel" or "{Alternative action}" | "Keep Editing" | "No" / "Go Back" |
| Destructive | {Destructive verb} + {Object} | "Delete Account" | "Remove" / "Yes" |

### Error Messages

| Structure | Component | Example |
|-----------|-----------|---------|
| {What went wrong} | Headline | "Email format isn't valid" |
| + {How to fix it} | Helper text | "Try name@company.com" |
| + {Why it matters} (optional) | Context (complex only) | "We need this to send your receipt" |

**Rules:**
- Never blame the user ("You entered an invalid email" ❌)
- Be specific ("Something went wrong" ❌ → "We couldn't save your changes because the server isn't responding" ✅)
- Always offer a path forward

### Empty States

| Structure | Example |
|-----------|---------|
| {What would be here} | "No projects yet" |
| + {Why it matters / what it enables} (optional) | "Projects help you organize your work" |
| + {One CTA to populate} | "[Create your first project]" |

### Confirmation Dialogs

```
{Title: Action about to happen}

{Body: Consequence — what will change, what can't be undone}

[{Action verb — matches what they clicked}]  [Cancel]
```

### Notifications / Toasts

| Type | Structure | Duration |
|------|-----------|----------|
| Success | "{What happened}" | 3-5s auto-dismiss |
| Error | "{What failed}. {Recovery.}" | Persistent until dismissed |
| Warning | "{What to be aware of}" | 5-8s or persistent |
| Info | "{What changed / FYI}" | 3-5s auto-dismiss |

---

## Terminology Governance

### Preferred Terms

| Use This | NOT This | Rationale |
|----------|----------|-----------|
| {preferred term} | {alternatives to avoid} | {clarity / consistency / audience} |
| {term} | {avoided} | {reason} |
| {term} | {avoided} | {reason} |

### Term Usage Rules

1. Use the same word for the same concept everywhere (don't alternate "delete" / "remove" / "trash")
2. Match the user's language (from persona research), not internal/engineering terms
3. Abbreviations: spell out on first use, then abbreviate if the user knows the abbreviation
4. Avoid jargon unless the audience is domain-expert (confirmed in personas)

---

## Writing Checklist

Before any UI text ships, verify:

- [ ] Scannability: Can the user get the point in <3 seconds?
- [ ] Actionability: Does the user know what to DO next?
- [ ] Specificity: Does it say exactly what happened / will happen?
- [ ] Tone match: Does it match the context tone shift above?
- [ ] Terminology: Does it use only the preferred terms?
- [ ] Length: Is it the shortest it can be without losing meaning?
- [ ] Accessibility: Will it make sense read aloud by a screen reader?

---

## Cross-References

| Artifact | Connection |
|----------|-----------|
| Personas | Terminology matches persona language level |
| Design System | Voice & tone is Section 6 of the design system |
| Component Library | Each component spec includes content constraints |
| Accessibility Baseline | Screen reader announcements follow these patterns |
