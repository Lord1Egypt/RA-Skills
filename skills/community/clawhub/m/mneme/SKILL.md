---
name: mneme
description: Maintain persistent cross-session agent memory in the Mneme plain-text format (.mneme files) — decisions, facts, preferences, gotchas, goals. Use when an .mneme file is present, when the user wants durable long-term agent memory, or asks to remember a decision/preference/gotcha across sessions. Read via the spine, recall by cue, write/supersede cells (content immutable, state mutable), calibrate trust by state/seen, and lint with the bundled tool.
version: 0.1.0
---

# Mneme — agent memory protocol

Mneme is a plain-text format for an agent's **persistent, cross-session memory**. A memory
file (`*.mneme`) is a list of **cells** (one decision/fact/preference each, self-contained),
and a derived **spine** (one line per cell: id + state + gist). Full spec: <https://github.com/casperkwok/mneme>.

**Core rule — content is immutable, state is mutable.** A cell's `gist`/body/`cue` is a fact
about the past, never edited. Its `state`/`seen`/`conf` is its relation to *now*, updated as
reality moves. To change content, add a new cell that supersedes the old.

## When to use
- A `*.mneme` file exists in the project → it is the memory; follow this protocol.
- The user wants durable memory ("remember this across sessions", "记住这个决策/偏好/踩坑").
- You just produced something a future session would be wrong or redo without.

## Cell format
```
@ DEC-0042  storage/cache                 # @ ID(PREFIX-NNNN, unique, never reused) + topic-path
gist  Local cache uses SQLite, not JSON   # one self-contained line; promoted into the spine
state live   conf high   since 2026-06-03   seen 2026-06-03
cue   concurrent writes / cache corruption / local storage choice   # recall keywords
> why / cost / context (free prose, may span multiple > lines)
link  supersedes DEC-0031                 # typed relation, repeatable
```
- **state**: `proposed` (not yet authoritative) · `live` (current/authoritative) ·
  `stale` (maybe expired, verify first) · `superseded` (replaced) · `retired` (dead, audit only).
  Spine/working-memory shows only `live` + `stale`.
- **ID prefixes**: `DEC` decision · `OKR` goal · `PREF` preference · `GOTCHA` pitfall ·
  `FACT` fact/constraint · `TODO` long-lived todo. Extensible.
- **link relations**: `supersedes`/`superseded-by` (pair them), `relates`, `depends-on`,
  `blocks`, `refines`.
- Line-oriented, no nesting; unknown lines are ignored; `#` lines are comments.

## Protocol (SOP)
1. **Boot** — when project context matters, read only the *spine*, not whole files:
   `python scripts/mneme_tool.py spine <file>` (or `grep '^@\|^gist\|^state'`). Keep it resident.
2. **Recall** — before acting, match the task topic against each cell's `cue` and `topic-path`;
   expand only the cells that hit. Recall generously, then judge relevance by content.
3. **Trust** — `live + conf high + recent seen` → use directly. `stale` / `conf low` / old
   `seen` → verify against the real source first, then bump `seen` to today (raise `state`/`conf`
   if warranted). `proposed` → not a conclusion; don't act on it unless the task is to advance it.
4. **Write** — when something durable is produced, append a new cell: next id via
   `python scripts/mneme_tool.py new-id PREFIX <file>` (never hand-count), self-contained `gist`,
   set `state`/`conf`, `since = seen = today`, write `cue` (which future topics should recall it —
   don't skip), `>` for the why, `link` as needed. **Append to end; never silently edit an old cell.**
   Test: *would a future session be wrong or redo work without this?* If yes, write it.
5. **Supersede** — to revise a belief: new cell + old cell set `superseded` + mutual `link`
   (`supersedes`/`superseded-by`). To merely reaffirm: only bump the old cell's `seen`. Content
   is never edited in place.
6. **Conflict** — two `live` cells disagree → prefer higher `conf`, then newer `seen`, and tell
   the user explicitly; then supersede the loser.
7. **Hygiene** — one claim per cell; gist self-contained; long content external (link/path only);
   ids never reused.

## Tooling (don't rely on agent discretion)
`scripts/mneme_tool.py` (zero deps):
- `spine <file>` — derive the spine (live/stale).
- `lint <file>` — health-check: duplicate ids, missing required fields, asymmetric/dangling
  supersede links, bad dates, and **`live` cells whose `seen` is older than 45 days** (decay).
  Exit code 1 on errors — wire into a git `pre-commit` hook so lifecycle metadata can't silently rot.
- `new-id PREFIX <file>` — allocate the next collision-free id.

## Don't use Mneme for
High-frequency precise queries / transactions (use a DB), large blobs (store externally, link
only), throwaway within-session scratch, or things that belong in code/docs. Mneme holds the
*why* — decisions, constraints, lessons, preferences — not every *what*.
