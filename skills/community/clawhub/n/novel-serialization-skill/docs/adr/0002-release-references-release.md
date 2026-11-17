# 0002. Release files reference release files only

Date: 2026-10-07
Status: Accepted

## Context

Two conventions for writing a path inside Markdown had been used
interchangeably, and they resolve differently:

- A path in backticks is *documentation*. It names a file so a reader can find
  it, and it is written relative to the repository root.
- A link — a label in `[]` followed by a target in `()` — is *navigation*. It
  is followed by a renderer relative to the file that contains it.

Rewriting one using the other's convention moves the target silently. A link
that resolved correctly becomes a link to nothing, and no Markdown linter
notices, because the target is prose.

The second problem is scope. Release documents were pointing into private work
areas — personal notes, drafts, the throwaway directory. On a public clone
those targets do not exist, so every such reference is a dead end for a reader.

## Decision

A file inside the release tree may only reference files that are also inside
the release tree. Files outside it may reference anything.

`scripts/check_refs.py` classifies every reference into one of seven buckets —
`OK`, `LOCAL`, `TEMPLATE`, `BARE`, `PRIVATE_OK`, `NONRELEASE`, `MISSING` — and
CI fails on `NONRELEASE`. `PRIVATE_OK` exists precisely so that a report or a
working note can keep pointing at private material without tripping the rule.

## Consequences

- The two path conventions are checked separately instead of being merged into
  one heuristic that is wrong half the time.
- Links are decoded before resolution. Without that, every link into a filename
  containing a space is a false `MISSING`.
- Root-absolute links (`/SKILL.md`) resolve from the repository root, matching
  how GitHub renders them, rather than from the filesystem root where they
  never resolve.
- Template paths (`角色名.md`, `{name}.md`) are reported as `TEMPLATE` and not
  as failures; documentation legitimately describes shapes that do not exist.
- Paths that are only ever *described* — subproject state files, example
  manuscripts, paths written from a subproject's point of view — are exempted
  in `.refsignore`, one regex per line with a reason. The same file is read by
  a local run, by pre-commit and by CI, so the three cannot disagree.
- A `MISSING` from a report or working note is bucketed as `PRIVATE_MISSING`
  and never gated on: those files describe another tree. Only `MISSING` from a
  release file fails the build. With that split, CI can gate on
  `NONRELEASE,MISSING` and the release tree is genuinely clean.
