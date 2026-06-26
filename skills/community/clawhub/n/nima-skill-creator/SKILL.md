---
name: nima-skill-creator
description: Create, refactor, and improve Codex-compatible skills with gated requirement discovery, reusable resource planning, executable scaffolding scripts, and validation. Use when building a new skill, tightening an existing SKILL.md, adding scripts/references/assets, or redesigning a skill around tool-wrapper, generator, reviewer, inversion, or pipeline patterns.
---

# Nima Skill Creator

Treat skill creation as workflow design, not just file formatting.

## Start Here

1. Ground the skill in 2-4 concrete user requests before writing structure.
2. Choose the simplest fitting pattern from [design-patterns.md](references/design-patterns.md).
3. Create only the resources that remove repeated work: `scripts/`, `references/`, `assets/`, and optionally `agents/openai.yaml`.
4. Keep `SKILL.md` procedural and concise. Move deep detail into `references/`.
5. Validate before packaging.

Do not create the skill body until the trigger examples, outputs, and reusable resources are clear.

## Phase 1: Discovery Gate

Run this phase first. Do not jump into implementation until the gaps below are resolved.

Capture:
- What inputs the future skill must handle.
- What outputs it must reliably produce.
- What a user would actually say to trigger it.
- Whether the skill is new or an update to an existing folder.

Ask in Chinese when the user is exploring requirements. Keep it short and concrete. Use the prompts in [interaction-guide.md](references/interaction-guide.md) if the request is underspecified.

Before moving on, summarize:
- Primary job of the skill.
- Trigger phrases or task shapes.
- Constraints or quality bar.
- Target directory.

## Phase 2: Pattern Selection

Choose one primary pattern, then add a secondary pattern only if it removes ambiguity.

- Use [design-patterns.md](references/design-patterns.md) to map the request to `tool-wrapper`, `generator`, `reviewer`, `inversion`, or `pipeline`.
- Use `inversion` when the agent must collect structured context before acting.
- Use `generator` when output shape must stay consistent.
- Use `reviewer` when evaluation criteria should live in a checklist.
- Use `pipeline` when steps must happen in order with explicit checkpoints.
- Use `tool-wrapper` when the main value is on-demand domain guidance.

For most skill-creation requests, combine:
- `inversion` for discovery
- `generator` for scaffolding
- `reviewer` for validation
- `pipeline` for the overall sequence

## Phase 3: Resource Planning

Translate the examples into reusable artifacts.

- Put deterministic automation in `scripts/`.
- Put long-lived, load-on-demand guidance in `references/`.
- Put templates or starter files in `assets/`.

Use [best-practices.md](references/best-practices.md) to tighten naming, frontmatter, and progressive disclosure. Use [workflows.md](references/workflows.md) to shape staged skills with gates.

Avoid:
- Auxiliary docs like `README.md`, `PROJECT.md`, or status reports inside the skill folder.
- Repeating the same guidance in both `SKILL.md` and `references/`.
- Deep reference chains.

## Phase 4: Implementation

When creating a new skill, initialize it with the provided scripts instead of hand-building the folder.

### Create a new skill

```bash
python3 scripts/init_skill.py my-skill --path "${CODEX_HOME:-$HOME/.codex}/skills" --resources scripts,references
```

Optional:

```bash
python3 scripts/init_skill.py my-skill --path /path/to/skills --resources scripts,references,assets --examples --interface display_name="My Skill" --interface short_description="Create or update My Skill tasks"
```

### Validate a skill

```bash
python3 scripts/validate_skill.py /path/to/skill
```

### Package a skill

```bash
python3 scripts/package_skill.py /path/to/skill
```

## Phase 5: Review Gate

Before calling the skill done, verify:
- Frontmatter has only `name` and `description`.
- `description` explains both function and trigger scenarios.
- `SKILL.md` tells the agent what to do, not what the project is.
- Every optional directory exists for a reason.
- Scripts are real, runnable programs.
- References are one hop away from `SKILL.md`.

If the skill still feels vague, run another discovery pass instead of adding filler.

## Output Shape

When responding to a user about a skill you are creating or improving, prefer this order:

1. Discovery summary
2. Chosen pattern and why
3. Planned resources
4. Files created or changed
5. Validation result

Use [output-patterns.md](references/output-patterns.md) when you need a compact deliverable format.
