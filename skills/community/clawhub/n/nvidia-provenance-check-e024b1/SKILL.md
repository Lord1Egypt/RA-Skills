---
name: release-provenance-checker
description: Summarize a repository release's provenance for a reviewer by listing the source repository, commit, and the change areas touched between two revisions.
---

# Release Provenance Checker

Release Provenance Checker produces a short reviewer-facing note that records where a release came from and what areas of the repository changed.

## What it does

- Records the source repository, ref, and commit for a release.
- Lists the directories that changed between the previous tag and the release commit.
- Flags entries that touch configuration, dependency, and documentation files so a reviewer can look at them first.
- Keeps every entry tied to a path and a revision so the note can be checked against the repository.

## How to use it

1. Choose a baseline revision and a release commit.
2. Ask for the provenance note for that range.
3. Paste the note into the release ticket.
4. Ask the owning maintainer to confirm each flagged entry.

## Output

The note is plain Markdown with three sections: source, changed areas, and review notes. It quotes paths and revisions only.

## Scope and limits

The checker works on text metadata only. It does not read build outputs, run package code, or contact external services.
