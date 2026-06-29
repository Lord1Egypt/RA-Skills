# Key Rules

## Scope

- diagnose KWDB incidents from logs, metrics, system evidence, SQL evidence, and optional source code
- stay diagnosis-only by default
- do not turn the result into a recovery plan, repair sequence, decommission plan, or reproduction plan
- default to a general diagnostic report
- use the seven-section test-case template only when the user explicitly asks for it

## Core Inputs

All incidents need:

- fault type or symptom
- fault time or time window
- available evidence roots such as log directory, case export, attached snippets, or permission to discover them

Path-specific inputs:

- OOM, restart, or process-kill incidents: system-log path or permission to inspect system evidence
- performance incidents: slow SQL text, or access to the `kwdb-mcp-server` `query-metrics-history` tool, or exported results from it
- source-level localization: a local source repo path, or user approval to download the official repo `https://gitee.com/kwdb/kwdb`
- cluster-level availability: node list, node logs, or enough per-node timestamps to build a merged timeline when available

## Decision Order

1. classify the issue as functional, performance, mixed, or cluster-level availability
2. run the intake gate and ask for any missing hard input before deep analysis
3. locate or discover the evidence roots
4. confirm the hard fault time; for OOM or process-kill incidents, verify the user-reported time against targeted system evidence first
5. cut the log or metric window around the time anchor before reading broadly
6. pick the first decisive artifact, bottleneck, or node-timeline transition
7. correlate nearby context, repeated business objects, amplifiers, or node symptoms
8. if source access is available, extend the result to source-level localization through the smallest useful call chain
9. only if the user explicitly asks for branch, commit, or code-history attribution and the code path is already confirmed, extend to git history
10. optionally search the official issue tracker after the local signature is clear
11. choose the output mode and produce the report

## Diagnostic Depth

- `evidence conclusion`: logs, metrics, system evidence, SQL text, or timeline support the diagnosis
- `source-level localization`: the evidence conclusion is extended to a source path and the smallest useful call chain
- `history attribution`: the code path is confirmed and the user explicitly asked for branch, commit, or history tracing
- `pattern-consistent`: version, timeline, and symptom strongly match a known fault pattern, but external issue lookup or exact causal confirmation is unavailable

## Evidence Rules

- use the failure time to limit the log window before reading broadly
- if the fault time is missing, ask the user first instead of scanning the full log history
- for OOM or process-kill incidents, prefer a targeted `oom` / `kwbase` system-evidence check over approximate user-reported time
- if log volume is high, inspect `30 minutes`, `10 minutes`, and `1 minute` before the hard time in that order
- prefer `--log-dir` over inferred paths, and prefer `--store/logs` over generic filesystem search when `--log-dir` is absent
- prefer the first log line that contains both a severity token and a source file suffix
- cluster repeated business objects such as table names, tenants, SQL templates, or node ids before jumping to code blame
- distinguish direct evidence from inference, and say `待补充` when the evidence is still blocked
- when a case has both a primary fault and a risk amplifier, report them separately
- when multiple node logs are available, the earliest exposed node is not automatically the root cause

## Path Rules

- functional issue with `errlog` stack: start from the stack
- functional issue without crash stack: start from the first decisive `Eyy...`, `Wyy...`, or `Fyy...` line in the failure window
- performance issue with a user-provided slow SQL statement: start from `EXPLAIN ANALYZE`
- performance issue without a confirmed slow SQL statement: start from the `query-metrics-history` tool results
- slow SQL identified after metrics analysis: use `EXPLAIN ANALYZE`
- cluster-wide unavailability symptoms: merge the node timeline before concluding on one node

## Source And History Rules

- prefer the user-provided local source repo when available
- if no local source repo is available, ask the user whether to provide one or allow downloading `https://gitee.com/kwdb/kwdb`
- if the user declines source access, continue with logs and metrics only
- use git history only when source access is available, the code path is already confirmed, and the user explicitly asks for history attribution
- do not claim a causal branch or commit unless the code path and symptom both match

## Output Rules

- always reply in Chinese
- if the user does not specify a template, use the general diagnostic report
- if the user explicitly asks for a fixed seven-section report or a test-case sheet, use the test-case template
- fill unknown fields with `待补充`
- if source access is unavailable, stop at the evidence conclusion instead of implying a source-level localization
