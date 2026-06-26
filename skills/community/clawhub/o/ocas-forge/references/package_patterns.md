# Forge Package Patterns

## Shortcut
```
ocas-{name}/
  skill.json
  SKILL.md
```
SKILL.md: 20-120 lines. Quick actions, inputs, caveats.

## Workflow
```
ocas-{name}/
  skill.json
  SKILL.md
  references/
    schemas.md (if needed)
```
SKILL.md: 80-250 lines. Trigger, inputs, workflow, outputs, boundaries.

## System
```
ocas-{name}/
  skill.json
  SKILL.md
  references/
    schemas.md
    {domain_detail}.md
    journal.md
  scripts/ (if needed)
  assets/ (if needed)
```
SKILL.md: 150-300 lines. Trigger, purpose, decision model, execution loop, support file map, validation.
