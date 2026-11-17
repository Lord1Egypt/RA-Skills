# docs/

Engineering documentation: decisions, conventions, and anything a contributor
needs that is too long for `README.md` and too stable for a changelog entry.

## What is here

| Document | What it records |
|---|---|
| [adr/README.md](adr/README.md) | Architecture decision records — index and template |
| [adr/0001-reports-are-not-released.md](adr/0001-reports-are-not-released.md) | Why working reports are never committed |
| [adr/0002-release-references-release.md](adr/0002-release-references-release.md) | The release-only reference rule and why it needs tooling |
| [adr/0003-dual-track-chapter-naming.md](adr/0003-dual-track-chapter-naming.md) | Two legal chapter naming schemes, and how to register a third |

## What is deliberately not here

**Reports.** Audit reports, review reports, and scan output are working
artefacts. They are generated into the workspace-local directory that
`.gitignore` excludes, they are not committed, and release files do not link to
them (see ADR-0001). If a report is worth keeping for readers, its conclusion
is promoted into `CHANGELOG.md`, an ADR, or `references/` — the report itself
stays out of the tree.

**Methodology.** Writing method, templates, and worked examples live in
`references/`. This directory is about the repository, not about novels.

## Adding a document

1. Under 500 lines (see [CONTRIBUTING.md](../CONTRIBUTING.md)).
2. No reference from a release file to a path outside the release tree.
3. Run `python scripts/dev.py all` before opening a PR.
