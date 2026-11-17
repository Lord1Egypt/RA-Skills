# 0001. Working reports are not released

Date: 2026-10-07
Status: Accepted

## Context

An audit of a long-running subproject found 227 generated reports sitting next
to the manuscript. They were committed, they were indexed from release
documents, and every one of them was a snapshot of a state that had since
moved on. Readers hitting the repository saw conclusions from months earlier
presented as current.

A report is not documentation. It is a measurement taken at a moment: scan
output, an audit of one revision, a review of one chapter. Its value decays
immediately and its wording is not edited to the standard of the rest of the
tree.

## Decision

Reports are generated into a workspace-local directory that `.gitignore`
excludes. They are never committed, and no release file links to one.

When a report's conclusion has lasting value, the conclusion is promoted: into
`CHANGELOG.md` if it changed behaviour, into `docs/adr/` if it changed a
convention, into `references/` if it changed how a novel is written. The report
itself stays out.

## Consequences

- History no longer contains stale conclusions, so `git log` reads as a record
  of decisions rather than of measurements.
- A report cannot be cited in a PR discussion by URL. This is the intended
  cost: the discussion should quote the finding, not point at a file that only
  exists on one machine.
- The reference checker enforces the second half of this rule mechanically
  (ADR-0002), so the convention does not depend on remembering it.
