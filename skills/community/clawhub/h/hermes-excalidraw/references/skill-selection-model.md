# Skill Selection Model (Hermes & OpenClaw)

The user's model for how skill selection works in Hermes and OpenClaw.

## The 3-Layer Architecture

### Layer 1 — Skill Catalog Exposure
The code exposes the skill catalog to the model. Skills must be:
- **Not disabled** — `enabled: false` = invisible
- **Not filtered** — frontmatter rules must pass for the skill to appear in the model-visible list
- **Available** — correctly installed with valid frontmatter

If a skill never appears in the model-visible list, it effectively **does not exist**.

### Layer 2 — Prompt Injection
The system prompt tells the model to check skills first. This is not a deterministic router — it relies on the model to make a choice from the visible catalog.

### Layer 3 — Model Selection
The model chooses the best skill, or combination of skills. It is NOT deterministic:
- The model can pick no skill (wrong)
- The model can pick a suboptimal skill
- The model can combine skills

## High-Leverage Moves to Improve Selection

| Move | Why It Works |
|------|-------------|
| Clear, precise name | Model matches on name — vague names get missed |
| Task-matching description | Model uses description to evaluate fit |
| Language real users say | Description uses the vocabulary the user actually uses |
| Explicitly invoke when needed | `skill_view(name)` forces the skill into context |
| Preload related skills together | Composite tasks need multiple skills loaded simultaneously |

## Key Insight: Discoverability ≠ Content

Skill selection is mostly about **discoverability**, not content quality. A skill with excellent content but a vague name or mismatched description will never be selected. The name and description are the interface to the model's selection mechanism.

## Source

User-provided framework for designing skill catalogs and improving skill selection in Hermes Agent and OpenClaw.