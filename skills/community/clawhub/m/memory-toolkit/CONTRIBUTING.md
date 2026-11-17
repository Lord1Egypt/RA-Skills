# Contributing — OpenClaw Memory Toolkit

This file is for **maintainers of this repository**. It documents how a change
travels from the repo to the published artifact, and the invariants the release
gate enforces. If you only want to *use* the skill, read the [README](README.md)
instead.

## Release Pipeline (repo → skill → GitHub → ClawHub)

> **MUST — every memory-skill change goes through `scripts/release.sh`.**
> No exception. A change to `skills/memory-health/**` is not "done" until
> `scripts/release.sh check` passes green. Do not tag, do not push a release,
> do not hand anything to ClawHub before that. If the gate fails, fix the drift
> or the invariant — never bypass the gate.

One artifact, one direction, four stages. **Never edit the installed skill directly;
never let the repo and the skill drift.**

```
  local repo          installed skill            GitHub            ClawHub
  .work/mh-v213  ──▶  skills/memory-health/  ──▶  push main + tag ──▶  manual (Stéphane)
```

1. **Edit in the repo** (`.work/mh-v213`). Commit there.
2. **Sync repo → skill.** The installed skill is what the agent and the nightly
   cron actually load, so it must be updated from the repo, never the reverse.
   `SKILL.md` is the one exception: the skill copy carries a YAML frontmatter
   (`name:` / `description:`) that the repo omits, so its **body** is synced while
   the frontmatter is preserved.
3. **Run the gate:** `scripts/release.sh check`. It refuses to pass until
   repo↔skill files are byte-identical (SKILL body), `trace_extractor` is a single
   source, version markers and OLLAMA_* loopback invariants hold, every script
   parses, the loopback test passes and the tree is clean.
4. **Tag + push:** `scripts/release.sh release vX.Y.Z "message"`, then create the
   GitHub release.

> **MUST — a git tag is NOT a release. Create the GitHub Release too.** The
> operator had to point this out on 2026-10-05: v3.2.1 had its tag pushed but
> appeared nowhere in the repo's Releases tab. The tag is a bare pointer; the
> Release is the readable, dated entry a human actually sees. After pushing the
> tag, always run:
> ```bash
> gh release create vX.Y.Z \
>   --title "vX.Y.Z — <title>" \
>   --notes "<same content as the CHANGELOG entry>"
> ```
> Verify with `gh release list` — the new version must appear as `Latest`. A
> release is not "done" until it is in that list.

5. **ClawHub** is published by the operator, from the repo.

> **MUST — every release updates the CHANGELOG *and* the README.** The operator
> asked for this explicitly (2026-10-05): a release is not just a tag. Before
> tagging, always:
> - **CHANGELOG.md** — add a new entry at the top: `## vX.Y.Z — <title> (<date>)`
>   with `### Added` / `### Changed` / `### Fixed` sections as applicable. Cite
>   the cause, not just the change (what broke, why, how it was found). Never
>   rewrite history: correct an older entry only to fix a factual error.
> - **README.md** — update anything the release makes stale: version numbers,
>   recommended models, new scripts, changed flags, requirements.
> - **SKILL.md** — bump the `current release vX.Y.Z` marker so the gate's
>   version-markers check passes.
>
> Skipping either document leaves GitHub showing a release nobody can read.
> This is part of "done", exactly like the green gate.

## Known single-source exception

`trace_extractor.py` exists in two places: the repo and
`skills/trace-extractor/trace-extractor.py`. The skill copy is the **live** one
(the cron uses it). The gate compares them and warns on divergence; port the live
copy into the repo before tagging so they converge forward.

## Public repo — no personal or health data, ever

The repository is **public**. Anything committed to it is world-readable, and a git
history rewrite is expensive and imperfect (forks, caches, GitHub-side copies).
Two mistakes were made and repaired on 2026-10-05; do not repeat them.

1. **Never write personal data into a published file — especially health data.**
   A fix to an adjacent skill mentioned a real medication name in `CHANGELOG.md`.
   That is health data in a public repo. Describe the *behaviour* (`defaults to a
   non-existent identifier`), never the identifier. The same goes for hostnames,
   tokens, account ids, and anything else that identifies a person or a system.
   Ask: *"does this belong in this repo, and does it expose anything private?"*
   before writing, not after.
2. **Stay in scope.** This repo documents the memory pipeline. A fix to an
   unrelated skill does not belong in its CHANGELOG, name or no name. Document
   what the repo *is*, not everything you happened to touch that day.

If a leak does happen: scrub the working tree, rewrite history
(`git filter-repo --replace-text`), delete and recreate the affected tags and
releases, force-push, and **verify every one of those steps from the remote** —
not from memory.

## Why the gate is non-negotiable

The repo and the installed skill are two copies of the same artifact. The moment
they drift, the cron runs one version while GitHub shows another, and nothing
tells you which is real. The gate exists to make drift impossible to ship
silently. A skipped gate is a defect waiting for a quiet month to surface.
