# Skill Design Patterns

Use this file to choose structure before writing `SKILL.md`.

## 1. Tool Wrapper

Use when the skill's main job is to load domain rules or internal conventions on demand.

Choose it for:
- Framework conventions
- Internal APIs
- House style guides
- Domain-specific reference material

Typical shape:
- Lean `SKILL.md`
- Heavier `references/`
- Few or no `assets/`

Question to ask:
- "Will this skill mainly make the agent smarter about a domain?"

## 2. Generator

Use when the output must follow a stable template.

Choose it for:
- Document generation
- Standardized plans
- Commit messages
- Project scaffolds

Typical shape:
- `assets/` for templates
- `references/` for style rules
- `SKILL.md` that orchestrates variable collection and filling

Question to ask:
- "Is inconsistent output the current pain?"

## 3. Reviewer

Use when the skill should evaluate something against criteria rather than produce a fresh artifact.

Choose it for:
- Code review
- Security review
- Content QA
- Compliance checks

Typical shape:
- `references/` contains checklists
- `SKILL.md` defines scoring order and output structure

Question to ask:
- "Should the standards change independently from the review workflow?"

## 4. Inversion

Use when the agent must interview the user first and must not act early.

Choose it for:
- Project planning
- Requirements gathering
- Ambiguous build requests
- Any skill where missing context causes rework

Typical shape:
- Hard gate: do not build before questions are answered
- Ordered discovery stages
- Explicit confirmation step

Question to ask:
- "Would acting too early create the wrong solution?"

## 5. Pipeline

Use when the task must move through ordered stages with checkpoints.

Choose it for:
- Multi-step transformations
- Approval-sensitive workflows
- Tasks that combine generation, review, and packaging

Typical shape:
- Sequential phases
- Hard transitions
- Validation between stages

Question to ask:
- "Do we need explicit checkpoints to keep the agent from skipping steps?"

## Selection Guide

- Pick `tool-wrapper` when knowledge loading is the main value.
- Pick `generator` when output consistency is the main value.
- Pick `reviewer` when scoring or findings are the main value.
- Pick `inversion` when discovery quality is the main risk.
- Pick `pipeline` when process integrity is the main risk.

Combine patterns only when each one controls a different failure mode.

Recommended default for skill creation:
- `inversion` to gather requirements
- `generator` to scaffold files
- `reviewer` to validate the result
- `pipeline` to enforce sequence
