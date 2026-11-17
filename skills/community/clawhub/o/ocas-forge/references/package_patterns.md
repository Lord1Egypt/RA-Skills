# Forge Package Patterns

## Shortcut
```
ocas-{name}/
  SKILL.md
```
SKILL.md: 20-120 lines. Quick actions, inputs, caveats.

## Workflow
```
ocas-{name}/
  SKILL.md
  references/
    schemas.md (if needed)
```
SKILL.md: 80-250 lines. Trigger, inputs, workflow, outputs, boundaries.

## System
```
ocas-{name}/
## System
```\nocas-{name}/\n  SKILL.md\n  references/\n    schemas.md\n    {domain_detail}.md\n    journal.md\n    config-default.json   — machine-readable default config (platforms, settings, credential file pointers)\n    plans/\n      {plan_id}.plan.md  (if skill has bundled workflow plans)\n  scripts/ (if needed)\n  assets/ (if needed)
```

SKILL.md: 150-300 lines. Trigger, purpose, decision model, execution loop, support file map, validation.

## references/config-default.json convention

When a skill has a `config.json`, store the machine-readable default as `references/config-default.json`. The SKILL.md storage-layout section should point to it instead of describing config values inline:

```
Default `config.json` structure: see `references/config-default.json`.
Credential file paths: see `references/credential-files.md`.
```

This keeps config structure out of SKILL.md (reducing scanner false positives) and gives agents a copyable template to bootstrap from.
## System Skill Required Sections (SKILL.md)
1. Responsibility boundary
2. Ontology types
3. Commands
4. [domain-specific workflow sections]
5. Optional skill cooperation
6. Journal outputs
7. Storage layout (point to `references/config-default.json` for config structure; list data file paths, not credential file paths)
8. OKRs
9. Initialization (point to `references/account-creation.md` for wallet/account setup steps)
10. Background tasks (omit if purely reactive)
11. Support file map (include all `references/` files the skill depends on)
12. Update command

## references/plans/ convention
Plans follow `spec-ocas-workflow-plans.md` format.
Filename must match plan_id: `{plan_id}.plan.md`.
Init command must copy plans to {agent_root}/commons/data/ocas-mentor/plans/ (skip existing).