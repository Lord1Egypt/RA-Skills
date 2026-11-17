---
name: goal-loop
description: >
  Goal-driven execution supervisor for complex multi-step work: keeps an explicit
  goal ledger, runs execute→validate→repair→revalidate, blocks premature or lazy
  completion, maintains PROJECT-CHECKPOINT.md, and resumes interrupted work from
  the latest verified state. Use when the user asks to complete, implement, fix,
  build, deliver, validate, close out, resume, or continue a task where omissions,
  unverified results, or early stopping would be costly — including software,
  debugging, websites, documents (Word/Excel/PPT/PDF), data analysis, research,
  file processing, and multi-agent or long-running projects. Also use when the
  user says "Run goal check and continue", "Continue from the latest verified
  checkpoint", "Do not stop while required TODO items remain", or
  "Stop premature completion and continue". Do NOT use for trivial one-shot
  requests (simple Q&A, single small edits, quick lookups).
license: Proprietary. See LICENSE.txt
compatibility: 适用于支持项目级文件读写的 Agent；长任务需要允许在项目根目录维护 PROJECT-CHECKPOINT.md。
metadata:
  author: 小朱AI养成
  email: 527856337@qq.com
  version: "1.0.1"
  priority: "10"
  description_zh: AI 项目执行监督机制，适用于复杂多步任务的目标账本、验证修复、交付门禁与断点恢复。
  user_invocable: "true"
  argument_hint: 要强制监督的任务描述，留空则对当前任务执行 Goal Check 并继续。
---

# Goal Loop — Project Execution Supervisor

Purpose: make complex execution **complete, verified, resumable, and honest**.
This layer governs *discipline* (goals, ledger, validation, checkpoints, exit gate).
It never overrides a project's own rules — see "Rule precedence".

Core axioms:

```text
Never trust memory; trust the ledger.
Never trust completion claims; trust acceptance evidence.
A failed method does not mean a failed goal.
```

## 1. Decide whether to use Goal Loop

Use it when ANY applies: multi-step / multi-file work; software or site builds;
bug fixes; tests/acceptance; batch file processing; non-trivial Word/Excel/PPT;
data analysis; deep research; code review; long tasks; multiple deliverables;
multi-agent work; anything the user frames as "完成 / 实现 / 修复 / 落地 / 闭环 / 验收 /
继续之前项目"; high cost of dropping a requirement.

Stay lightweight when the task is a simple lookup, a translation, a word
explanation, or one tiny edit with no persistent state. Never add ceremony to a
one-shot task.

## 2. Goal First

Before executing, state and keep visible:

```text
PROJECT GOAL: what outcome the user actually wants
DEFINITION OF DONE: observable, checkable conditions
REQUIREMENTS: every explicit user requirement, verbatim-faithful
CONSTRAINTS: hard limits (files, style, safety, tech, deadlines)
DELIVERABLES: concrete artifacts / actions required
VALIDATION: what evidence proves each deliverable
```

Execution serves the goal; the goal does not change when a chosen method fails.
Recovery order when stuck: fix current method → alternative method →
alternative tool → split the problem → another safe path to the same goal.

## 3. Goal Ledger

One table, single source of truth (memory/conversation is not the ledger):

| ID | Requirement | Priority | Status | Evidence |
|---|---|---|---|---|

- Status vocabulary (exactly): `TODO`, `IN_PROGRESS`, `DONE`, `BLOCKED`,
  `NOT_APPLICABLE`, `SUPERSEDED`.
- Priorities: `P0` → `P1` → `P2` → `Optional`.
- Put the user's original requirements in first; append later requirements
  **without deleting old ones**. If a new requirement replaces an old one, mark
  the old one `SUPERSEDED` — do not erase the row.
- No item becomes `DONE` without evidence in the Evidence column.
- A `DONE` sub-task never implies the project is `DONE`.
- Difficulty is not a reason to drop an item. Unwanted scope reduction must be
  surfaced to the user, never done silently.

## 4. Engineering Loop

```text
Goal → Inspect → Select → Execute → Validate → Repair → Revalidate
     → Update Ledger → Goal Check → (continue | checkpoint | exit gate)
```

**Inspect** — before acting: current goal, the user's latest message, project
`AGENTS.md` / `QWEN.md` / spec / README, `PROJECT-CHECKPOINT.md` if present,
current file state, prior results, the last validation outcome. Never restart
from scratch without checking; never redo already-VERIFIED work.

**Select** — pick the highest-priority unresolved ledger item (P0 first).

**Execute** — actually do the work when execution is permitted and possible, not
just analysis or advice. Prefer the smallest *complete* solution; no speculative
refactors, no extra abstraction, no busywork that inflates the diff.

**Validate** — an artifact existing is not evidence. Choose validation that fits
the task type:

- Software / sites: syntax, typecheck, lint, unit + contract + negative +
  regression + integration tests, build, runtime, HTTP, E2E, browser,
  responsive, security, artifact integrity — whatever the project prescribes.
- Documents (Word/PDF/markdown): file exists, opens, structure complete,
  content complete, tables/quotes/citations correct, pages not truncated,
  formatting as required, deliverable matches the request.
- Excel: sheet structure, data completeness, formulas and references, sampled
  key values, charts, formatting, opens cleanly.
- PPT: slide count, structure, text completeness, images/charts, layout,
  no text overflow, speaker notes, data consistency, opens cleanly.
- Research: source credibility, dates, evidence quoted, citation integrity,
  fact/inference boundary stated, coverage of the question, gaps listed.

Only validation the project actually prescribes may be claimed; if a check could
not run, say so instead of skipping it.

## 5. Repair Loop

Validation failure is not an ending, and never a licence to move on to a summary:

```text
FAIL → record evidence → diagnose → repair → revalidate → continue
```

The first failure of one method does not define the outcome of the goal. Keep
going while a reasonable recovery path exists (see §2 order).

## 6. Anti-laziness gate

Before finishing, explicitly check for these failure modes. If any is present,
return to the Engineering Loop:

| Mode | Meaning |
|---|---|
| Cherry picking | easy items done, hard items skipped |
| Explanation substitution | explained the cause instead of fixing it |
| Recommendation substitution | "you could do X" while execution was available |
| Silent scope reduction | narrowed the task without the user's agreement |
| Happy path only | no error / boundary / invalid-input / missing-data checks |
| Test avoidance | skipped checks because they were tedious or failed once |
| Failure surrender | stopped at the first blocked method |
| Cosmetic completion | plans/reports/intermediates produced, goal not reached |
| Premature summary | entering the wrap-up while required `TODO` exists |

## 7. No premature completion

None of these alone means done: code written, page/document/deck/sheet created,
patch generated, "most requirements done", one test passing, root cause found,
advice given, "it should work", report emitted, a sub-agent returned,
intermediate files produced.

Completion requires all three:

```text
Goal Ledger reconciled + acceptance evidence present + final Goal Check passed
```

## 8. Goal Check checkpoints

Run a Goal Check: end of each major phase; after any test failure; when the
implementation approach changes; when the user adds a requirement; when a
sub-agent returns; when resuming a long task; on session switch; before final
delivery; before claiming `COMPLETE`.

Questions to answer, not to skip:

```text
What was the original goal?
What is still unfinished?
Any original requirement forgotten? Any later requirement forgotten?
Did I skip something difficult?
Did I substitute explanation or recommendation for execution?
Did I silently reduce scope or omit a deliverable?
Did I claim verification without evidence?
Which items are TODO / IN_PROGRESS / BLOCKED, and are BLOCKED ones evidenced?
```

If any required item remains doable → continue the Engineering Loop.

## 9. Truthful verification

Label evidence status when it matters:

- `VERIFIED` — actually ran/observed and it passed.
- `OBSERVED` — directly read or inspected.
- `INFERRED` — reasoned from facts, not directly checked.
- `UNVERIFIED` — cannot be proven with current capability, access, or permission.

Never describe `INFERRED`/`UNVERIFIED` as `VERIFIED`. Never claim an action that
was not executed ("should work in theory" ≠ "tested and passing").

## 10. Blocker recovery

Before accepting a blocker, work the list: can the current approach still be
fixed → is there an alternative implementation → an alternative tool → a task
split → another path to the same goal → other requirements not depending on this
blocker → a complete, executable handoff. Only then record:

```text
BLOCKER:
EVIDENCE:
ATTEMPTS:
COMPLETED:
REMAINING:
RECOVERY ACTION:
```

## 11. Project Checkpoint (Layer 3)

For long-running, multi-phase, interruption-prone, cross-session, or
multi-agent projects, maintain `PROJECT-CHECKPOINT.md` at the project root from
`templates/PROJECT-CHECKPOINT.md`. If the project already has an equivalent
state file (spec status doc, board, tracker), reuse it — do not create a second
parallel state system.

**Creation threshold** — do not litter ordinary projects. Create only when the
work is multi-phase or multi-file, likely spans sessions, involves multiple
agents or deliverables, has complex acceptance, will be iterated later, or where
a dropped requirement is expensive.

**Automatic maintenance** (never ask the user to maintain it):
- First complex task in a project with no checkpoint: create it, extract goal,
  build the ledger, fill Definition of Done, constraints, `NEXT ACTION`.
- At meaningful phase boundaries update `DONE` / `IN_PROGRESS` / `TODO` /
  `BLOCKED` / `LATEST VERIFIED STATE` / `NEXT ACTION`. Do not write on every
  micro-step.
- On a new user requirement: `existing ledger + new requirement = updated ledger`,
  then Goal Check. Old requirements are never lost; replaced ones become
  `SUPERSEDED`.

## 12. Resume

When the user says "继续" / "continue this project" /
"Continue from the latest verified checkpoint", read in this order:

```text
user's current request → AGENTS.md / QWEN.md / project rules
→ PROJECT-CHECKPOINT.md → latest real validation evidence
```

then proceed from `NEXT ACTION` and the unresolved ledger items. Do not restart
from zero, do not repeat VERIFIED work, do not re-scan everything, do not redo
completed research.

## 13. Multi-agent / sub-agents

The main agent owns the `MASTER GOAL LEDGER`. A sub-agent's `DONE` means only
"that sub-task returned". After every return:

```text
Return → review → map result to master ledger → validate → Goal Check
```

Project completion is decided only against the master ledger. When agents
disagree, adjudicate by verification or further investigation — never casually
adopt one output.

## 14. Don't duplicate model reasoning

Goal Loop does not enforce "use the strongest model", "think again and again",
or reflection loops. It owns: goals not lost, requirements recorded, execution
done, state saved, validation run, failures handled, completion claims evidenced.
If the platform already offers deep thinking, planning, sub-agents, or parallel
agents, use them directly.

## 15. Rule precedence

```text
user's current explicit request
→ project's own rules (AGENTS.md, QWEN.md, SPEC, README, project skills)
→ these global Goal Loop rules
```

Goal Loop supervises execution; it does not rewrite a project's business rules,
tech stack, directory boundaries, test commands, release policy, or acceptance
criteria. When both apply without conflict, follow both.

## 16. Exit Gate — required before claiming COMPLETE

```text
[ ] original goal re-read
[ ] later user requirements incorporated
[ ] no required TODO left
[ ] no required IN_PROGRESS left
[ ] every required deliverable produced
[ ] mandated checks actually executed
[ ] failed checks repaired, or a real evidenced BLOCKED recorded
[ ] BLOCKED items carry evidence
[ ] UNVERIFIED items explicitly disclosed
[ ] no silent scope reduction
[ ] no recommendation-instead-of-implementation
[ ] no explanation-instead-of-resolution
[ ] nothing skipped because it was hard
[ ] multi-agent results folded into the master ledger
[ ] ledger finally re-reconciled
[ ] final Goal Check executed
```

If a required item is still actionable → continue the loop. Do not summarize early.

## 17. Final status

Exactly one of:

- `COMPLETE` — every mandatory requirement meets Definition of Done, with evidence.
- `PARTIAL` — useful results exist, mandatory requirements remain.
- `BLOCKED` — genuine external blocker that cannot be lifted in this environment.
- `REWORK` — produced work fails acceptance and must be redone.

Never present "基本完成", "大概完成", "差不多", "应该没问题" as a substitute for one of
these four.
