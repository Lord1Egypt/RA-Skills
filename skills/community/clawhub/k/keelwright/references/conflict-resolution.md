# CONFLICT-resolution (T53, v1.8.x)

> **Source:** Originally added in Wave 3.5 (`c31b776`, "CI badge + CONFLICT-resolution section").
> **Status:** Restored in v1.10.1 after being dropped during the v1.9.0/v1.10.0 layered refactor.
> **Why it matters:** This is a *safety process*, not a code feature. Losing it means two agents
> can silently auto-merge conflicting policy into the skill source — invalidating the A/B QA
> results that Gate 2 depends on. Load this reference whenever a merge/rebase produces a conflict
> in `keelwright` source.

---

## The process

When two agents/subagents, or a rebase/merge, produce conflicting changes:

1. **Never auto-merge** a conflict into the skill's own source. Stop.
2. **Triage**: is the conflict in *generated code* (re-run the agent) or in *authored policy*
   (human decides)? Generated-code conflicts → discard both, re-run on current main (no rebase).
3. **Authored-policy conflict** (e.g. two reviewers changed the same rule): surface BOTH versions
   to the human with a one-line diff summary. Do NOT pick a winner silently.
4. **Rebase conflicts during QA**: rerun the agent on current `main`; never hand-resolve a
   benchmark arm's code (that invalidates the A/B result — see Gate 2).
5. **Record** the conflict + resolution in `PROGRESS.md` so the next session doesn't repeat it.

---

## When to load this

| Trigger | Action |
|---------|--------|
| `git merge` / `git rebase` shows conflict in `SKILL.md`, `references/*.md`, or `scripts/*.py` | Stop. Follow steps 1-5. |
| Two parallel subagents edited the same file | Triage: generated code (step 2) vs authored policy (step 3). |
| QA benchmark arm shows unexpected diff after rebase | Never hand-resolve (step 4). Re-run on `main`. |
| Conflict resolved | Append to `PROGRESS.md` with: files, both versions summary, chosen resolution, date. |

---

## Cross-references

- **Gate 2** (Independent LOGIC review) — `references/security-gates.md`
- **Loop termination / escalation** — `references/circuit-breaker.md`
- **Session tracking** — `PROGRESS.md` (created by bootstrap, gitignored by default)
- **SKILL.md Map table** — links here under "Merge/rebase conflict in skill source"

---

*Restored: keelwright v1.10.1. Original author: Hermes Agent (Wave 3.5, 2026-08-30).*
