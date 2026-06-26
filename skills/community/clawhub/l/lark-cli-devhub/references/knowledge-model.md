# Knowledge Model

Dev Hub separates human browsing from AI retrieval.

## Source Of Truth

| Layer | Role | AI Use |
|---|---|---|
| Base | Structured facts: Projects, Areas, Tasks, Bugfixes, Pitfalls, Playbooks, Decisions, Releases, Artifacts, AI Runs | Search first; use field names and keywords |
| Docs/Wiki | Long-form design notes, retrospectives, runbooks, incident notes | Open when a Base record links to a useful page |
| Whiteboard | Architecture, workflow, dependency, and knowledge maps | Visual aid; always pair with a Base Artifact summary |
| Tasks | Operational work queue and ownership | Use for current work state, not historical root cause detail |

## Records

- `Projects`: repository identity, default branch, current focus, wiki URL.
- `Areas`: modules or domains with code paths and risk level.
- `Tasks`: planned work, bugs, blockers, next action, and Feishu task URL.
- `Bugfixes`: symptom, evidence, root cause, fix, verification, regression risk.
- `Pitfalls`: reusable traps and what to check next time.
- `Playbooks`: diagnosis order, required evidence, commands, and forbidden actions.
- `Decisions`: accepted technical/product choices and review triggers.
- `Releases`: branch, commit, verification, rollback notes, related tasks and bugfixes.
- `Artifacts`: Docs, Whiteboards, dashboards, links, and summaries.
- `AI Runs`: what the AI did, what evidence it checked, what changed, and writeback status.

## Avoiding Memory Conflict

Use agent memory for collaboration behavior:

- preferred tone
- approval habits
- how the user likes summaries
- recurring workflow preferences

Use Lark CLI Dev Hub for project facts:

- bugs and fixes
- code paths and architecture decisions
- test or verification evidence
- release history
- reusable mistakes and playbooks

This keeps AI personal memory small and keeps project knowledge portable across Codex, Claude Code, and teammates.
