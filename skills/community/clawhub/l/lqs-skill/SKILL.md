---
name: lqs-skill
description: |
  LQS Skill — prompt/schema/template driven artifact generator for the LQS codebase.
  Manual-run only: users paste free-text requirement or exported document text; the Skill
  guides prompt-driven generation of RequirementDraft → Spec → RenderPlan → Preview Diff.
  This Skill does NOT execute code, run migrations, or fetch external documents automatically.
activation:
  - "lqs-skill"
  - "generate controller"
  - "generate model"
  - "render artifacts"
  - "preview diff"
version: "0.2.0"
author: "LQS Team"
entry_prompts:
  - .skill/prompts/01_parse_requirement.md
  - .skill/prompts/02_mine_patterns.md
  - .skill/prompts/03_build_templates.md
  - .skill/prompts/04_resolve_spec.md
  - .skill/prompts/05_render_artifacts.md
  - .skill/prompts/06_preview_diff.md
  - .skill/prompts/07_write_files.md
examples: .skill/examples/
notes: |
  Workflow is intentionally manual to preserve safety and cross-repo compatibility.
  Recommended usage: follow .skill/quickstart.md and .skill/implementation_runbook.md.
---

# LQS Skill (human-run) overview

This SKILL.md provides metadata and a short usage note for packaging the `.skill`
assets for skill platforms such as OpenClaw.

- Purpose: provide prompts, templates, schemas and examples to guide human-in-the-loop
  generation of boilerplate artifacts (controller/model/view/migration) for Admin module.
- Non-goal: no code execution, no remote fetching, no automatic migrations.

See also: .skill/quickstart.md, .skill/implementation_runbook.md, .skill/mvp_delivery_checklist.md
