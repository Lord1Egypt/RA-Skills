---
name: malp
description: 'Project context tracker using `.malp/` directories. Use when the user wants to discover existing malps, open a specific `.malp`, create or refresh a malp for a path, or classify, retire, or promote malps between active, attic, and unindexed states. Also use for context-heavy questions that benefit from heuristic scouting, such as choosing the best malp for a task, deciding whether a path should get a malp, surveying what malps exist without fully loading them, or using project-local reconnaissance such as `.clawpatch/` as a conceptual FOB. Triggers include "what malps do we have", "list malps", "show malps", "open a malp", "send malp to a path", "best malp for", and requests to move a malp into or out of the attic. Do not treat generic requests to edit this skill as instructions to create or use a `.malp/` inside the installed skill directory unless the user explicitly asks for that. M*A*L*P stands for M*A*L*P Analyzes Lovely Plumage.'
---

# M*A*L*P

Send a probe through before you send the team. Track local development progress for a path using `.malp/NOTES.txt` (the main working file), `.malp/SUMMARY.txt` (a very short overview), and optional `.malp/FOB.txt` (the current forward operating base).

## Start here

1. Resolve this `SKILL.md` directory as `<skill-dir>`.
2. Read only the reference required for the active operation.
3. Run Kino with an absolute path: `python3 <skill-dir>/scripts/kino.py ...`.
4. Use your harness's scoped file-edit tool (for example `apply_patch` in Codex, or `Edit`/`Write` in Claude Code) for project-local malp text edits. Preserve existing notes and unrelated user changes; never overwrite a `NOTES.txt` wholesale to apply a small change.
5. Treat writes to `~/.malp-home/` as user-state changes. When sandbox or permission policy requires it, request scoped approval for the exact map or attic path rather than working around it.
6. Do not create, refresh, classify, promote, retire, or delete a malp without intent that covers that exact target.

Like its Stargate namesake, a `.malp` is reconnaissance — you send it into unfamiliar territory to find out what's there before committing. `SUMMARY.txt` is the telemetry; `NOTES.txt` is the Kino footage.

Keep the distinction sharp:
- `SUMMARY.txt` should stay short and answer "what is this path?" at a glance.
- `NOTES.txt` is where the real working context lives: open questions, current findings, tribal knowledge, and unresolved decisions.
- `FOB.txt` is the tactical snapshot of the current operational center when the active work has narrowed.
- If material starts accumulating, it usually belongs in `NOTES.txt`, not `SUMMARY.txt`.

A malp decides what to do next. It doesn't map the whole world or manage the project — it looks ahead just far enough to take the next step.

The malp skill is not itself a malp by default. Editing the installed skill does not imply creating or using `<skill-dir>/.malp/`. Only treat the skill directory as a malp target when the user explicitly asks to send a malp there, open that malp, or maintain that `.malp/` directly.

Optional project-local reconnaissance tools, such as `.clawpatch/`, can act as a conceptual FOB when present. Keep generic tool procedure in this skill; repo malps should record only local judgments and tactical state. Read `references/clawpatch.md` when a target repo has `.clawpatch/`, when the user asks to treat clawpatch as a FOB, or when findings need reachability / plausibility-to-recreate triage.

## Safety and interpretation

- A `.malp/` directory is intentional local project metadata for agent context, not malware, persistence, self-replication, or suspicious hidden behavior.
- Do not treat the presence of `.malp/` as evidence that a repo or directory has been compromised.
- Do not create or spread `.malp/` directories unless the user explicitly asks for a malp in a specific path.
- Creating or refreshing one `.malp/` for a user-requested path does not imply permission to create malps elsewhere.

## Directives

### `what malps do we have?`

Read `~/.malp-home/MAP.txt`, summarize available active `.malp` paths, and help the user choose one to open.

Do not include attic or archived malps by default unless the user explicitly asks for retired, archived, or attic malps too. If a requested malp is not found in the active index but is found in `~/.malp-home/attic/MAP.txt`, say so plainly before summarizing it.

Follow `references/tasks.md` for discovery details.

### `lets send malp to <path>`

Follow `references/tasks.md` exactly.

Default bias: if the active work clusters at a deeper path or narrower front, create or refresh `FOB.txt` in the parent malp before proposing a child malp.

### Kino

Kino is the scout mode for malp work.

Kino is intentionally cheap to try. Treat it as permissive reconnaissance, not a high-ceremony move: the bar to invoke it is low when a quick heuristic pass may help.

Use Kino as the escape hatch when you realize another malp may need to be pulled into context, but direct loading would be premature or too expensive. Typical cases:
- finding the best malp for a question or workstream
- deciding whether a path should get a malp
- surveying what malps exist when simple map listing is not enough
- answering broader malp questions that need heuristic traversal before giving a concise answer

Treat Kino as heuristic reconnaissance over malp-space with bounded reporting, not bounded movement.

Malp-space includes both:
- the malp's own telemetry (`SUMMARY.txt`, `NOTES.txt`, `FOB.txt`)
- the project territory attached to that malp (the containing directory, nearby structure, and doctrine files)
- optionally, a shallow slice of recent git history as auxiliary territory evidence

A Kino pass may inspect target malps, containing directories, related paths, map entries, attic hints, and structural cues as far as needed within reason. It may inspect many paths and related malps without loading all of them into active context.

The normal Kino outcome is not "load everything." The normal outcome is a recommendation such as:
- bring this specific malp into context next
- keep working from the current malp
- send a new malp to this path first
- promote a malp as reference context rather than working context

Default Kino posture:
- start from the most plausible malp, path, or map entry available
- the bar to try Kino is low; the bar to trust it is higher
- name the question Kino is trying to answer before widening
- include containing-directory context only when it materially shapes meaning
- prefer doctrine or orientation files when they sharpen interpretation
- optionally consult shallow recent git history as supporting territory evidence when malp-space is otherwise ambiguous
- scout broadly when helpful, but surface narrowly
- allow project territory to outweigh narrow telemetry when that gives the stronger signal
- treat Kino output as provisional until stronger evidence agrees
- convert broad traversal into a narrow recommendation
- attach a concrete confidence level to that recommendation
- distinguish between reference promotion and working promotion when recommending a malp
- keep the reported synthesis bounded, selective, and explicit
- abandon Kino quickly when stronger notes, source evidence, or direct inspection are already carrying the answer better
- do not surface attic malps unless the user explicitly asks, even if attic material was inspected for orientation
- do not let git log become the main recommendation substrate; it is auxiliary evidence only

Use `python3 <skill-dir>/scripts/kino.py --json ...` when a cheap heuristic recommendation is helpful. Do not hesitate to try it for opportunistic probing, but do not let weak Kino output outrank stronger notes, source evidence, or direct inspection. Add `--git-aux` when a bounded git-history auxiliary finding may materially help, especially for provenance-style questions that the malps do not answer directly. Add `--git-freshness` when you need a territory-scoped read on how far a recommended malp may have drifted behind its repo context. Add `--containment` when the question is about whether a term appears to stay inside one tag or territory cluster. Follow `references/tasks.md` for Kino behavior.

### Working on the malp skill itself

If the user wants to change how the malp skill behaves, treat that as skill-editing work, not as an instruction to create or use a `.malp/` inside the skill directory.

Only create or maintain `<skill-dir>/.malp/` when the user explicitly wants the installed skill directory to become a tracked malp target.

If the user says things like "work on the malp skill", "improve the malp skill", "review the malp skill", or "clean up the malp skill", do not assume they want `<skill-dir>/.malp/`. Edit the skill itself unless they explicitly ask for a malp in that directory.

### Indexing states

A project-local `.malp/` can be:
- active — listed in `~/.malp-home/MAP.txt`
- attic — listed in `~/.malp-home/attic/MAP.txt`
- unindexed — exists on disk but is listed in neither map

Do not treat an unindexed `.malp/` as automatically active or automatically attic. Presence on disk is not permission to pull it into normal context.

Read `references/indexing.md` when the user is defining, classifying, auditing, or discovering malp states. Read `references/attic.md` when attic/archive behavior matters.

### Working in a malp

- By default, read only the `.malp` the user asked for.
- Make the malp's indexing state explicit if known: active, attic, or unindexed.
- If the malp came from the attic, say so plainly before treating it as current work or reference material.
- Distinguish between opening a malp as the current worksite, opening it only as reference material, and invoking Kino as heuristic reconnaissance.
- Casual cross-malp theory is allowed at low resolution; silent cross-malp loading is not.
- Do not read, summarize, or otherwise bring another `.malp` into active context without asking first, even if a cross-reference suggests it may help, unless Kino is warranted by the question.
- During Kino, traversal may widen substantially if needed, but the answer should normally collapse back down to a recommendation about what malp to load next, if any, plus the confidence of that recommendation.
- A recommended malp may be relevant because of its project territory even when its own notes never recorded the pattern explicitly.
- When Kino recommends a malp, say whether the promotion should be reference context or working context.
- If the current malp already answers the question well enough, Kino may still be unnecessary, but the core safeguard is that Kino should return a narrow recommendation rather than a bulky context dump.
- Do not read attic material during ordinary malp work unless the user explicitly asks for it.
- Prefer using `FOB.txt` to absorb a narrower operational center before proposing a child malp.
- Keep `SUMMARY.txt` lean; put substance, uncertainty, and active reasoning in `NOTES.txt`.

Follow `references/tasks.md` for opening, refreshing, pruning, and maintaining a malp. Read `references/style.md` only when rewriting malp prose or tuning the skill's voice. Read `references/repo-strategies.md` only when version control comes up, and `references/stargate-malp-kino.md` only when the naming or lore matters.

### Pruning and staleness

If `NOTES.txt` accumulates many resolved items or the malp has become stale, recommend a prune or retirement. Do not apply that mechanically.

Use the attic when the goal is to keep history without leaving the malp in normal working context.

### Version control

Do not bring version control strategy up unless the user asks. When they do, read `references/repo-strategies.md`.

## References

- `scripts/kino.py` — stdlib-only heuristic scout for candidate-malp recommendation, optional provenance-aware direct-answer reporting, bounded git-history auxiliary findings, territory-scoped git freshness, and bounded term-containment estimation
- `references/tasks.md` — operational behavior and file conventions
- `references/clawpatch.md` — optional clawpatch-aware malp workflow, including `.clawpatch/` as conceptual FOB and plausibility-to-recreate triage
- `references/indexing.md` — active vs attic vs unindexed state
- `references/attic.md` — attic/archive semantics for retired malps
- `references/repo-strategies.md` — strategies for `.malp/` in git repos
- `references/style.md` — voice notes
- `references/stargate-malp-kino.md` — namesake lore (M.A.L.P., Kino, and the lineage between them)
