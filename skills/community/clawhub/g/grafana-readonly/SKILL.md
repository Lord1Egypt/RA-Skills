---
name: grafana-readonly
description: Read existing Grafana dashboards and panels without modifying them. Use when answering questions about values already visible in Grafana, locating the right dashboard/panel, extracting panel queries, listing dashboard variables, or rerunning panel-backed queries with a different time range or variable set. Best for Grafana-first analytics workflows where read-only access is preferred.
---

# Grafana Readonly

Use this skill as the default Grafana entrypoint for analytics work.

## Core workflow

1. Find the relevant dashboard.
2. Inspect its panels and variables.
3. Prefer reading or rerunning an existing panel before writing a new query.
4. Stay read-only unless the user explicitly asks for creation or modification work.

## Default task order

### 1. Locate the dashboard
Use dashboard search/list actions first.

Prefer this when the user asks things like:
- “这个指标在哪个看板里？”
- “有没有收入/LTV/注册转化相关看板？”
- “帮我找睡眠内容消费的图表”

### 2. Inspect the dashboard structure
After finding a likely dashboard, read:
- dashboard title / uid
- panel list
- variable list
- default time range or refresh settings if available

Do this before answering confidently. Many mistakes come from grabbing the wrong panel.

### 3. Inspect the panel query
Before explaining a metric definition, extract the panel query/config.

Look for:
- datasource
- query language / query text
- ref IDs / multiple queries
- variable references
- transformations

Use this when the user asks:
- “这个图怎么算的？”
- “这个 DAU 的口径是什么？”
- “这个 panel 背后查的是哪张表/哪个 datasource？”

### 4. Rerun the panel query
When the user wants the same chart under another condition, rerun the existing panel query with:
- a different time range
- different variables
- a different format if supported

Prefer rerunning an existing panel over inventing a new query.

## Read-only rules

- Do not create dashboards in this skill.
- Do not update dashboards in this skill.
- Do not delete dashboards, panels, alerts, or annotations.
- If the task requires new dashboard creation, hand off to a build-oriented skill or explicit implementation flow.

## Answering rules

When replying after Grafana reads, provide:
- the answer first
- the panel/dashboard used
- any key variable or time-range assumptions
- uncertainty if the panel does not fully match the question

Do not dump raw Grafana JSON unless the user explicitly wants it.

## Minimum action coverage

This skill is expected to support these read paths:
- search dashboards
- get dashboard details
- list panels
- get panel query
- list variables
- run panel query

If an installed Grafana skill does not cover most of these, treat it as partial coverage and plan a local supplement.

## When Grafana is not enough

Escalate beyond this skill when:
- no matching dashboard/panel exists
- the user needs an arbitrary new SQL query
- the needed split is not supported by existing variables
- the user is asking for a new dashboard design

In those cases, switch to the analytics workflow skill and decide whether to use Grafana datasource queries or direct ClickHouse.

## References

Read these only when needed:
- `references/action-checklist.md` for the concrete Grafana action matrix and MVP coverage
- `references/evaluation-notes.md` for why `rpe-grafana` is a lightweight candidate and where it likely falls short
