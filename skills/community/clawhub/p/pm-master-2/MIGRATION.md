# PM Master v1.3.6 → v2.0.0 Migration Guide

## Overview

v2.0.0 is an **architectural refactor** whose goal is to move from a "reference-manual-style SKILL" to an "enforcement-manual-style SKILL".
Most scripts and templates remain unchanged; the main changes are in the SKILL.md structure, the Sub-Agent protocol, and the newly added execution-driven scripts.

---

## Change List

### 1. SKILL.md Refactor (core change)

| Aspect | v1.3.6 | v2.0.0 |
|--------|--------|--------|
| Lines | ~201 lines | ~90 lines |
| Structure | Orchestration + reference material mixed | Pure enforcement instructions |
| Rule phrasing | "Suggested / recommended / as needed" | "Must / prohibited / else blocked" |
| Workflow | 6-step suggestive process | 6-step mandatory process + checkpoint |

**Migration action**: Replace SKILL.md with the v2 version; back up the old version as SKILL.v1.md.

### 2. New Files

| File | Purpose |
|------|---------|
| `scripts/execution_driver.py` | Execution-phase driver script, bridging the planning → execution gap |
| `scripts/subagent_check.py` | Sub-agent output validator |
| `references/subagent-protocol.md` | Sub-agent communication protocol (JSON Schema) |

### 3. Modified Files

| File | Change |
|------|--------|
| `config.yaml` | Added execution/quality_gate/stage_gates/operational_control config blocks |
| `references/project-schema.md` | Added _checkpoint field definition; schema_version upgraded to 2 |

### 4. Unchanged Files

The following files can be copied directly from v1.3.6 and used without modification:
- All scripts under `scripts/` (except the 2 newly added)
- All templates under `templates/`
- All `references/methodology-*.md`
- All `references/phases/*.md`
- `references/agents.md`, `references/expert-roles.md`, `references/activity-expert-map.md`
- `references/lifecycle.md`, `references/orchestration.md`
- `references/hybrid_playbook.md`, `references/program-management.md`
- `references/risk-matrix.md`, `references/metrics.md`, `references/templates-index.md`
- `examples/sample_project.yaml`

### 5. Deletable Files

| File | Reason |
|------|--------|
| `references/usage.md` | Heavily overlaps with README.md; no longer needed in v2 |
| `README.en.md` | May be kept but no longer force-synced |
| `CHANGELOG.md` (v1.x) | Kept as historical record; create a new v2 CHANGELOG |

---

## Backward Compatibility

- **project.yaml compatible**: v1.3.6 project.yaml can be used in v2.0.0; schema_version auto-upgrades
- **Templates compatible**: all v1.3.6 templates are fully compatible in v2.0.0
- **Scripts compatible**: all v1.3.6 scripts are fully compatible in v2.0.0

---

## Suggested Migration Steps

1. Back up the current pm-master directory
2. Replace SKILL.md with the v2 version
3. Copy the newly added files to the corresponding directories
4. Update config.yaml
5. Delete usage.md
6. Update _user_meta.json version number to 2.0.0
7. Test: verify the new flow with "start an agile project"
