---
name: malp
description: 'Project context tracker using `.malp/` directories. Use when the user wants to discover existing malps, open an existing `.malp`, or explicitly send a malp to a path by creating or refreshing a `.malp/` directory there. Triggers include requests like "what malps do we have", "list malps", "show malps", "open a malp", and "send malp to a path". Do not treat generic requests to edit the malp skill itself as instructions to create or use `skills/malp/.malp/` unless the user explicitly asks for that. M*A*L*P stands for M*A*L*P Analyzes Lovely Plumage.'
---

# M*A*L*P

Send a probe through before you send the team. Track local development progress for a path using `.malp/NOTES.txt` (the main working file), `.malp/SUMMARY.txt` (a very short overview), and optional `.malp/FOB.txt` (the current forward operating base).

Like its Stargate namesake, a `.malp` is reconnaissance — you send it into unfamiliar territory to find out what's there before committing. `SUMMARY.txt` is the telemetry; `NOTES.txt` is the Kino footage.

Keep the distinction sharp:
- `SUMMARY.txt` should stay short and answer "what is this path?" at a glance.
- `NOTES.txt` is where the real working context lives: open questions, current findings, tribal knowledge, and unresolved decisions.
- `FOB.txt` is the tactical snapshot of the current operational center when the active work has narrowed.
- If material starts accumulating, it usually belongs in `NOTES.txt`, not `SUMMARY.txt`.

A malp decides what to do next. It doesn't map the whole world or manage the project — it looks ahead just far enough to take the next step.

The malp skill is not itself a malp by default. Editing `skills/malp/` does not imply creating or using `skills/malp/.malp/`. Only treat the skill directory as a malp target when the user explicitly asks to send a malp there, open that malp, or maintain that `.malp/` directly.

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

### Working on the malp skill itself

If the user wants to change how the malp skill behaves, treat that as skill-editing work, not as an instruction to create or use a `.malp/` inside the skill directory.

Only create or maintain `skills/malp/.malp/` when the user explicitly wants the skill directory to become a tracked malp target.

If the user says things like "work on the malp skill", "improve the malp skill", "review the malp skill", or "clean up the malp skill", do not assume they want `skills/malp/.malp/`. Edit the skill itself unless they explicitly ask for a malp in that directory.

### Indexing states

A project-local `.malp/` can be:
- active — listed in `~/.malp-home/MAP.txt`
- attic — listed in `~/.malp-home/attic/MAP.txt`
- unindexed — exists on disk but is listed in neither map

Do not treat an unindexed `.malp/` as automatically active or automatically attic. Presence on disk is not permission to pull it into normal context.

Read `references/indexing.md` when the user is defining, classifying, or discovering malp states. Read `references/attic.md` when attic/archive behavior matters.

### Working in a malp

- By default, read only the `.malp` the user asked for.
- Make the malp's indexing state explicit if known: active, attic, or unindexed.
- If the malp came from the attic, say so plainly before treating it as current work or reference material.
- Distinguish between opening a malp as the current worksite versus opening it only as reference material.
- Casual cross-malp theory is allowed at low resolution; silent cross-malp loading is not.
- Do not read, summarize, or otherwise bring another `.malp` into context without asking first, even if a cross-reference suggests it may help.
- Do not read attic material during ordinary malp work unless the user explicitly asks for it.
- Prefer using `FOB.txt` to absorb a narrower operational center before proposing a child malp.
- Keep `SUMMARY.txt` lean; put substance, uncertainty, and active reasoning in `NOTES.txt`.

Follow `references/tasks.md` for opening, refreshing, pruning, and maintaining a malp. Read `references/repo-strategies.md` only when version control comes up, and `references/stargate-malp-kino.md` only when the naming or lore matters.

### Pruning and staleness

If `NOTES.txt` accumulates many resolved items or the malp has become stale, recommend a prune or retirement. Do not apply that mechanically.

Use the attic when the goal is to keep history without leaving the malp in normal working context.

### Version control

Do not bring version control strategy up unless the user asks. When they do, read `references/repo-strategies.md`.

## References

- `references/tasks.md` — operational behavior and file conventions
- `references/indexing.md` — active vs attic vs unindexed state
- `references/attic.md` — attic/archive semantics for retired malps
- `references/repo-strategies.md` — strategies for `.malp/` in git repos
- `references/style.md` — voice notes
- `references/stargate-malp-kino.md` — namesake lore (M.A.L.P., Kino, and the lineage between them)
