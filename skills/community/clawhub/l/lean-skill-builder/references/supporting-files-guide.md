# Supporting Files Guide

The skill folder should stay small. Every file should earn its keep.

## Progressive disclosure model

Skills load in three tiers. Understanding the token economics helps you decide
where content belongs.

| Tier | What loads | When | Budget |
|------|-----------|------|--------|
| **1. Metadata** | `name` + `description` from frontmatter | Always in context for every conversation | ~100 words |
| **2. SKILL.md body** | Everything in `SKILL.md` below frontmatter | When the skill triggers | <500 lines ideal |
| **3. Bundled resources** | `references/`, `scripts/`, `assets/` | On demand, when SKILL.md tells the model to read them | Unlimited |

**Design implication:** Put only what the model needs on *every* trigger in SKILL.md.
Push optional detail, variant-specific guidance, and long reference material into
Tier 3 files. This keeps token cost low for the common case.

## Build in this order

When a new skill is justified, add files in this order and stop as soon as the skill is usable:

1. `SKILL.md`
2. `references/` with 1-3 files only if they reduce context load or hold optional detail
3. `assets/` only if the skill needs bundled templates, icons, fonts, or sample files
4. `scripts/` only if exact repeatable execution is clearly better than prose

If step 1 is enough, stop.

---

## `SKILL.md`

Put these here:
- frontmatter (`name`, `description`)
- scope and non-scope
- default workflow
- concise rules of thumb
- explicit links to supporting files
- the minimum build or audit instructions that should be visible whenever the skill triggers

Keep in `SKILL.md` only what the agent should likely see whenever the skill triggers.

### Move content out of `SKILL.md` when:
- it is detailed reference material
- it is only needed in some cases
- it is long examples, schemas, checklists, or variant-specific guidance
- it makes the core workflow harder to scan

---

## `references/`

Put these here:
- decision trees
- checklists
- examples and patterns
- schemas or domain notes
- variant-specific instructions
- build aids such as outline patterns or optional content maps

Use `references/` when the material is useful context but not mandatory on every trigger.

Good fits:
- audit checklist
- naming/frontmatter patterns
- folder placement rules
- API or domain reference notes
- example trigger phrasing

Bad fits:
- duplicate copies of SKILL.md guidance
- placeholder docs with no concrete use
- README/changelog/process notes for humans
- references created only because "most skills have a references folder"

### Count discipline

Default target: **0-2 reference files**.
Go to **3** only when each file has a distinct job.
If you need more than that to explain the skill, the scope is probably too wide.

---

## `assets/`

Put static resources here that the skill uses in its output — not instructions.

Good fits:
- document templates (e.g., a .docx or .html starter)
- icons, fonts, or images used in generated output
- sample/example files the skill processes

Bad fits:
- reference documentation (belongs in `references/`)
- scripts (belongs in `scripts/`)
- anything that only exists to pad the folder

Most skills do not need an `assets/` folder. Add it only when the skill produces
output that depends on bundled files.

---

## `scripts/`

Put code here only when code is genuinely the better form.

Good fits:
- deterministic transformations
- repeatable helpers that would otherwise be rewritten often
- fragile sequences where exact execution matters

Do **not** add a script when:
- a few lines of instructions are enough
- the script exists only to justify the skill
- nobody is likely to run it more than once
- the environment assumptions are unclear and untested

Rule of thumb: if the main value is judgment, keep it as guidance; if the main value is exact repeatable execution, consider a script.

### Script stub rule

If a script is justified during build, a stub is enough at first. Do not scaffold a mini-project around it.

---

## Minimal folder patterns

### Smallest valid skill

```text
skill-name/
└── SKILL.md
```

### Skill with optional detail

```text
skill-name/
├── SKILL.md
└── references/
 └── checklist.md
```

### Skill with two focused references

```text
skill-name/
├── SKILL.md
└── references/
 ├── patterns.md
 └── audit-checklist.md
```

### Skill with bundled assets

```text
skill-name/
├── SKILL.md
├── references/
│ └── patterns.md
└── assets/
 └── template.html
```

### Skill with deterministic helper

```text
skill-name/
├── SKILL.md
├── references/
│ └── patterns.md
└── scripts/
 └── helper.py
```

Start with the smallest pattern that works.

---

## Build output checklist

When asked to build a skill skeleton, produce:
- recommendation
- minimal folder tree
- draft frontmatter
- `SKILL.md` outline or draft
- justified references/scripts/assets only if needed
- optional publish metadata suggestions only if useful

Do **not** produce:
- repo scaffolding
- dashboards or registries
- packaging automation by default
- filler docs created for appearance
