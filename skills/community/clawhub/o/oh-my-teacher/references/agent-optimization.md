# Agent Optimization

Use this file after `references/agent-adapter-contract.md` when running in any
named or generic agent. Its purpose is to turn detected capabilities into the
best Oh My Teacher execution path.

## Launch Protocol

At the start of a course-review session, do this once:

1. Identify the agent id from `agents/registry.json` when possible; otherwise use
   `generic`.
2. Read the matching `agents/<agent>.yaml` adapter.
3. Probe visible capabilities without asking the user when tools are already
   inspectable.
4. Select one optimization profile from the table below.
5. State only the selected environment and strategy, not the whole probe.
6. Begin with the smallest useful learning artifact.

Do not delay a conceptual explanation or single practice question to complete a
full probe. Probe only when the current task needs the capability.

## Optimization Profiles

| Profile | Required capability | Best path |
|---|---|---|
| `scripted-agent` | `file-read` + `file-write` + `shell` | Use local files, run deterministic scripts for snapshots/SRS/flashcards, and validate generated artifacts. |
| `file-agent` | `file-read` + `file-write`, no shell | Read materials and write Markdown artifacts; do not claim scripts ran. |
| `retrieval-agent` | `kb-retrieval` or `citations` | Build source-grounded maps, cite materials, label evidence, and keep unsupported claims as assumptions. |
| `memory-agent` | `memory` | Store stable course facts, exam dates, user preferences, and durable summaries only. |
| `ide-agent` | `ide` | Emphasize programming-course review, runnable examples when shell exists, diagnostics, code traces, and project-linked exercises. |
| `visual-agent` | `rendering` | Prefer Mermaid, LaTeX, plots, tables, or HTML visuals when the host renders them. |
| `planner-agent` | `task-plan` | Use native task plans for multi-step ingestion or mock-exam workflows; keep student-facing study plans in `/plan`. |
| `delegating-agent` | `subagents` | Delegate large read-only scans; keep grading, final synthesis, and user feedback in the main agent. |
| `reminder-agent` | `proactive-message` or `scheduler`, plus explicit user opt-in | Use `references/opt-in-reminders.md` to schedule or generate daily/weekly knowledge digests; never enable reminders silently. |
| `prompt-agent` | none confirmed | Use inline Markdown snapshots, SRS tables, flashcards, plans, and ASCII visuals. |

Profiles can combine. Example: an IDE with file-write and shell should use both
`ide-agent` and `scripted-agent`.

## Capability To Behavior

- `file-read`: inspect course materials directly; cite filenames or headings
  when possible.
- `file-write`: save course snapshots, dashboards, mock exams, wrong-question
  notes, flashcard source Markdown, and generated demos when useful.
- `shell`: prefer `scripts/snapshot.py`, `scripts/srs.py`, and
  `scripts/export_flashcards.py`; run tests for generated scripts or code demos.
- `sandbox`: ask for approval only when the operation requires it; provide an
  inline fallback if approval is denied.
- `search`: use for official course pages, public syllabi, or platform docs; do
  not use web search to invent exam emphasis.
- `kb-retrieval`: use before asking the student to paste materials.
- `citations`: attach source anchors to material-grounded claims.
- `memory`: write only stable facts; do not store transient mistakes without a
  course context.
- `task-plan`: track long agent workflows, not every student-facing reply.
- `subagents`: use for large read-only scans; never let workers silently grade or
  mutate course state.
- `ide`: connect explanations to the open project, diagnostics, examples, tests,
  and code traces.
- `rendering`: choose the richest visual the host supports; downgrade to ASCII
  when rendering is uncertain.
- `proactive-message`: only after explicit user opt-in, send reminder messages
  using the daily/weekly digest contract in `references/opt-in-reminders.md`.
- `scheduler`: only after explicit user opt-in, schedule delayed or recurring
  review reminders; when missing, output an inline digest and copyable reminder
  config.
- `unknown`: start as `prompt-agent` and upgrade only after a capability is
  confirmed.

## Best Use By Agent Family

- General coding agents: select `scripted-agent` when files and shell exist;
  otherwise use `file-agent` or `prompt-agent`.
- IDE agents: select `ide-agent` first for programming courses, then add
  `scripted-agent` if shell exists.
- Knowledge-base agents: select `retrieval-agent` and cite course materials
  before generating plans or quizzes.
- Local model agents: select `prompt-agent`; keep outputs short and one task at a
  time unless the wrapper exposes stronger tools.
- Chat-only agents: select `prompt-agent`; provide copyable artifacts.
- Proactive-capable agents: add `reminder-agent` only when the runtime exposes
  proactive-message or scheduler tools and the user has explicitly opted in.

## Quality Gates

Every optimized run must satisfy these gates:

1. No phantom tool use: never claim a read, write, script, citation, memory, or
   render operation that did not happen.
2. No platform privilege: agent id changes capability hints only, not teaching
   behavior.
3. No command drift: slash-command behavior comes from `references/INDEX.md` and
   command references, not adapters.
4. Source discipline: distinguish course-material evidence from general course
   inference.
5. Repair bias: after practice or grading, produce a concrete repair action and
   update SRS when supported.
6. Reminder consent: proactive reminders and daily/weekly digest schedules must
   be explicitly requested by the user and must stop when the user asks.
