---
name: orbcafe-pivot-ainav
description: Build ORBCAFE advanced analytics interactions using CPivotTable/usePivotTable and voice navigation using CAINavProvider/useVoiceInput. Use when requests involve drag-drop pivot dimensions, aggregation controls, preset management, or space-key voice navigation workflows.
---

# ORBCAFE Pivot + AINav

## Scope

Use this skill for advanced analytics interaction and voice navigation.

Primary APIs:
- `CPivotTable`, `usePivotTable`
- `CAINavProvider`, `useVoiceInput`, `CVoiceWaveOverlay`, `COrbCanvas`

## Workflow

1. Determine if request is pivot, voice, or combined from `references/domain-patterns.md`.
2. Start from matching recipe in `references/recipes.md`.
3. Apply interaction and reliability constraints in `references/guardrails.md`.

## Output Contract

1. `Module choice`: pivot or AINav (or both).
2. `Minimal implementation`: controlled if persistence/integration needed.
3. `Ops note`: one operational requirement (preset persistence or ASR endpoint contract).
