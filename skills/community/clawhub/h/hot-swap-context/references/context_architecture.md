# Context Architecture Guide

## Why this reference exists

Read this file when designing the shape of a portable context system. Use it to move from abstract memory ideas to a concrete architecture with ownership, interfaces, storage patterns, and retrieval rules.

## Canonical architecture

Design the system as a **context operating system**, not as a chat-history archive.

| Component | Function | Design rule |
|---|---|---|
| Context vault | Durable store for typed memory objects | Keep ownership outside any one model vendor |
| Artifact store | Files, drafts, reports, code, decks, spreadsheets, and linked assets | Preserve outputs as first-class memory, not only summaries |
| Retrieval router | Select the smallest useful context for a task | Optimize for just-in-time retrieval, not maximal recall |
| Writeback engine | Update preferences, state, evaluations, and artifacts after work is done | Require explicit write rules by memory type |
| Policy layer | Access control, redaction, retention, deletion, export | Define before broad automation |
| Interface layer | MCP server, API, CLI, SDK, or app integration | Keep the system model-agnostic where possible |

Anthropic’s memory tool is especially relevant here because it explicitly treats memory as a client-side capability that persists between sessions and is stored in developer-controlled infrastructure [1]. MCP matters because it provides an open way for AI applications to connect to external systems including files, databases, tools, and workflows [2].

## Ownership modes

Start with ownership before storage.

| Ownership mode | Best fit | Main requirement |
|---|---|---|
| Personal context vault | Individual builder or operator | Local-first or user-controlled portability |
| Team context layer | Startup or functional team | Shared project memory with scoped permissions |
| Enterprise context mesh | Larger organization | Governance, audit, retention, and identity integration |

Do not blur these modes. Many failures happen because personal preferences, team workflows, and employer-owned artifacts are mixed into one undifferentiated store.

## Memory taxonomy

Use typed memory objects.

| Memory type | Typical contents | Retrieval form |
|---|---|---|
| Identity memory | role, organization, scope, project affiliation | short profile summary |
| Preference memory | tone, formatting, review style, brevity, coding style | concise preference sheet |
| Workflow memory | checklists, SOPs, tool sequences, approval paths | checklist or runbook excerpt |
| Domain memory | terminology, ontology, product knowledge, org concepts | note, snippet, or retrieval chunk |
| Relationship memory | challenge level, escalation behavior, meeting style | behavioral contract |
| Artifact memory | prior outputs and linked work products | file link, summary, or raw artifact |
| Execution memory | task state, pending actions, milestones, decisions | state object |
| Evaluative memory | pass/fail patterns, corrections, quality scores | scorecard or evaluation record |

Use `templates/memory_object.md` to define each object class explicitly.

## Retrieval design rules

Apply these rules every time.

1. Retrieve by task need, not by recency alone.
2. Prefer typed summaries before raw history.
3. Pull artifacts separately from preferences and state.
4. Enforce freshness and confidence thresholds.
5. Keep a clear writeback path for each retrieved object.
6. Cap retrieval volume by token, latency, or cost budget.

## Writeback design rules

Only write back when one of the following is true:

- a stable preference was confirmed
- a reusable workflow was observed
- a durable artifact was produced
- a task-state checkpoint was reached
- an evaluative signal or correction was captured

Do not write back speculative inferences that have not been confirmed or are unlikely to generalize.

## Bundle design

A portable bundle should summarize the workspace without pretending to be the entire system.

Include at minimum:

- manifest
- ownership declaration
- memory object index
- artifact index
- governance summary
- portability constraints
- last-updated timestamps

Use `scripts/build_context_bundle.py` to generate a starter manifest from a workspace.

## Anti-patterns

Avoid these patterns:

| Anti-pattern | Why it fails |
|---|---|
| One giant rolling memory file | impossible to govern or retrieve cleanly |
| Loading all historical context into the prompt | creates context bloat and retrieval noise |
| Treating raw export as operational portability | export is not the same as live context reuse |
| Storing everything as “preferences” | collapses state, artifacts, and policy into one bucket |
| Auto-saving every inference | creates memory corruption and trust problems |

## Implementation note

When the user wants a concrete starting point, scaffold the workspace first with `scripts/init_context_os.py`, then edit the generated manifest, governance file, and scorecard.

## References

[1]: https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool "Memory tool - Claude API Docs"
[2]: https://modelcontextprotocol.io/docs/getting-started/intro "What is the Model Context Protocol (MCP)? - Model Context Protocol"
