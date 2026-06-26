# AGENTS.md

This repository uses a strict implementation and review standard.
All changes must satisfy both the task goal and the repository review policy.

## Core working rule

Before making or finalizing any change, always align with:

- the current user request
- the existing codebase conventions
- `.codex/review_policy.md`

Do not treat "code compiles" as "task is complete".
Do not stop at partial implementation if the intended behavior is still incomplete.

---

## Primary objective

For every task, your goal is to deliver a change that is:

- functionally complete
- internally consistent
- minimally invasive
- testable
- documented when needed
- free of obvious code smell

You must actively check for missing follow-up changes, not just modify the first file that looks relevant.

---

## Definition of done

A task is only done when all of the following are true:

1. The expected goal of the current task is completely implemented.
2. All directly affected code paths are updated.
3. Related callers, types, configs, and interfaces are checked for drift.
4. Relevant tests are added or updated when behavior changes.
5. Relevant documentation is updated when external behavior changes.
6. No obvious temporary workaround or bad smell is introduced.
7. The final state is coherent enough for another engineer to continue from it safely.

If any of the above is not satisfied, the task is not complete.

---

## Required implementation behavior

When editing code, always:

- understand the local context before changing it
- trace the impacted execution path
- check for affected imports, exports, interfaces, schemas, configs, commands, and docs
- prefer root-cause fixes over superficial patches
- keep naming clear and consistent with the repository style
- avoid unrelated refactors unless they are necessary to complete the task safely

Do not:

- leave placeholder logic unless explicitly requested
- leave silent regressions in adjacent code paths
- introduce duplicate logic when existing abstractions can be extended safely
- bypass validation, typing, or guardrails just to make the change pass
- add TODO / FIXME / HACK as a substitute for completing the work
- leave debug output, temporary comments, or dead branches

---

## Completeness checklist

Before ending a task, explicitly verify:

- Was the requested behavior actually implemented end to end?
- Were all impacted files updated, not just the most obvious one?
- Are there related tests that now need to change?
- Are there docs, examples, configs, or command descriptions that now need to change?
- Did this introduce coupling, duplication, dead code, or temporary logic?
- Is there any edge path that was left inconsistent?

If uncertainty remains, keep working until the uncertainty is resolved or clearly surfaced.

---

## Testing standard

When code behavior changes, you must evaluate test impact.

### Required behavior

- add tests for new behavior when the repo has an existing testing pattern
- update tests when prior expected behavior has changed
- run the most relevant tests available for the modified area
- if lint or typecheck is part of the normal repo workflow, run it when relevant

### Minimum expectation

If business logic, API behavior, UI behavior, schema, config handling, or command behavior changes, assume test impact exists unless proven otherwise.

Do not claim success without checking whether tests were needed.

### If tests are not added

Only skip test changes when there is a strong reason, such as:

- no test framework exists for that area
- the change is purely non-functional
- the repository genuinely does not cover that layer

In such cases, state the limitation clearly in the final summary.

---

## Documentation standard

Documentation must be updated when a change affects any of the following:

- public behavior
- API contract
- CLI usage
- config fields or env vars
- setup steps
- developer workflow
- examples shown to users or contributors

Possible documentation targets include:

- `README.md`
- `docs/`
- usage examples
- inline developer docs
- changelog or migration notes
- API or schema reference docs

Do not assume documentation is optional just because code is the primary change.

---

## Review policy

You must follow `.codex/review_policy.md` as the final quality bar.

Before ending a task, review the current change against that policy, especially for:

- implementation completeness
- modification omissions
- test omissions
- documentation omissions
- bad smells

If the current change does not pass that review bar, continue iterating before stopping.

---

## Code smell avoidance

Treat the following as quality failures unless explicitly justified:

- TODO / FIXME / HACK left in changed paths
- debug prints or temporary logs
- duplicated logic
- dead code
- inconsistent naming
- partial migration
- overly coupled changes
- hidden breaking behavior
- validation bypasses
- brittle special-case patches

Prefer a clean, maintainable solution over the fastest local edit.

---

## Change scope discipline

Keep changes focused on the task, but do not ignore necessary adjacent fixes.

Good scope:

- everything required for correctness, tests, and docs

Bad scope:

- unrelated refactors
- broad stylistic rewrites with no task value
- speculative architecture changes

If a nearby issue blocks correctness, fix it.
If it is unrelated and non-blocking, leave it alone.

---

## Expected final summary format

When finishing a task, provide a concise summary that covers:

1. what was implemented
2. which files were changed
3. what tests were added, updated, or run
4. whether documentation was updated
5. any remaining limitation or risk, if one truly remains

Do not state or imply the task is complete unless it passes the standards in this file and in `.codex/review_policy.md`.

---

## Priority order

When tradeoffs exist, use this order:

1. correctness
2. completeness
3. consistency with repository patterns
4. test coverage and verification
5. documentation sync
6. minimal and clean change set

Speed is not a reason to lower the quality bar.

---

## Repository-specific override

If the repository contains more specific local instructions in nested `AGENTS.md` files, apply the more local instruction for files in that scope, while keeping this root policy as the baseline.
