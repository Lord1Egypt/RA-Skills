---
name: orbcafe-graph-detail-ai
description: Build ORBCAFE graph analytics dialogs, detail pages, and AI settings flows using CGraphReport, chart components, CDetailInfoPage/useDetailInfo, and CCustomizeAgent. Use when requests include KPI/chart drilldown, detail tabs with searchable fields, or configurable AI prompt settings.
---

# ORBCAFE Graph + Detail + Agent

## Scope

Use this skill when the request involves one or more of:
- Graph dialog and chart analytics
- Detail page with searchable sections/tabs and AI fallback
- LLM settings/prompt template editor

## Workflow

1. Pick sub-domain via `references/domain-selector.md`.
2. Load minimal pattern from `references/recipes.md`.
3. Apply domain guardrails from `references/guardrails.md`.
4. Return minimal snippet plus required data model.

## Primary APIs

- Graph: `CGraphReport`, `useGraphReport`, `useGraphChartData`, `useGraphInteraction`, chart components
- Detail: `CDetailInfoPage`, `useDetailInfo`
- Agent settings: `CCustomizeAgent`

## Output Contract

1. `Chosen module`: graph/detail/agent and why.
2. `Minimal code`: one focused snippet.
3. `Data model`: model/tabs/sections/settings shape.
4. `Extension`: one next enhancement (chart interaction, AI fallback, preset templates).
