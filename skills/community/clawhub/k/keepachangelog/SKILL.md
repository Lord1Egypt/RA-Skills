---
name: keepachangelog
description: Maintain CHANGELOG.md in Keep a Changelog 1.1.0 format. Use when the user asks to create a changelog, record recent changes or draft release notes, cut or tag a release, or audit an existing changelog — and before editing any CHANGELOG.md for another reason.
---

# Keep a Changelog

A changelog is written for one **reader**: a human, mid-upgrade, deciding what this release means for them. Every rule below serves that reader.

## Format rules

- The file opens with the header prose from the skeleton in [references/template.md](references/template.md) — it names the format and the versioning scheme the file follows.
- `## [Unreleased]` always sits first, collecting changes for the next release.
- Every released version has its own section, newest first: `## [X.Y.Z] - YYYY-MM-DD` (ISO 8601 date).
- Entries sit under `### Added` / `### Changed` / `### Deprecated` / `### Removed` / `### Fixed` / `### Security`, in that order, listing only the categories that have entries:
  - **Added** — new features.
  - **Changed** — changes in existing functionality.
  - **Deprecated** — features that still work but are scheduled for removal.
  - **Removed** — features removed in this release.
  - **Fixed** — bug fixes.
  - **Security** — vulnerability fixes.
- Version headings are markdown link references, resolved in a block at the foot of the file to compare URLs; the block covers every heading.
- A withdrawn release keeps its section, marked `## [1.0.1] - 2026-06-14 [YANKED]`, with a line saying why it was pulled.

## Writing entries

An entry earns its place by being **notable**: the reader would notice the change or act on it. Internal refactors, CI tweaks, and invisible dependency bumps fall below the bar; security fixes are always above it.

- Write the change the reader experiences, in the reader's vocabulary: "Config paths may now be relative to the project root", not the commit title that produced it.
- Commits are raw material, never entries: translate each one, merge several into one notable change, split one that hides two.
- **Deprecated** is the reader's upgrade warning: name the replacement and, when known, the removal version.
- A breaking **Changed** entry says it breaks and names the migration step.

## Create a changelog

1. Copy the skeleton from [references/template.md](references/template.md) into `CHANGELOG.md`.
2. List released versions from `git tag` (fall back to version history in the package manifest); create a dated section per version, newest first. For a history deeper than a handful of versions, ask the user how far back to backfill.
3. Fill each section from `git log <prev-tag>..<tag>`, applying the Writing entries rules.
4. Write the link-reference block covering every heading.

Done when: the file matches the skeleton's shape, every version section has an ISO date and a resolving link reference, and `## [Unreleased]` sits at the top.

## Record changes

1. Establish the range to cover: from the newest change already recorded (the latest version's tag, or the last commit that touched `CHANGELOG.md` if Unreleased has entries) to `HEAD`.
2. Walk `git log` over that range commit by commit, judging each against the notable bar.
3. Write each notable change under its category in `## [Unreleased]`.

Done when: every commit in the range is accounted for — turned into an entry, folded into an existing entry, or judged below the notable bar.

## Cut a release

1. Choose the version, unless the user named one: any Removed or breaking Changed entry → MAJOR; else any Added, Changed, or Deprecated entry → MINOR; else PATCH.
2. Rename `## [Unreleased]` to `## [X.Y.Z] - <today>` and open a fresh, empty `## [Unreleased]` above it.
3. Update the link-reference block: `[Unreleased]` compares `<new-tag>...HEAD`; the new version compares `<previous-tag>...<new-tag>`.

Done when: an empty Unreleased sits at the top, the new section carries today's date and every former Unreleased entry, and both updated references resolve.

## Audit a changelog

1. Check every Format rule and every Writing entries rule against the file, top to bottom.
2. Cross-check `git tag` against version sections: a released version with no section is a violation — the reader mistakes the gap for "nothing changed".
3. Report violations grouped by rule, each with its concrete fix; apply the fixes when the request was to fix rather than to review.

Done when: every rule has been checked against every section, and each violation found is fixed or reported.
