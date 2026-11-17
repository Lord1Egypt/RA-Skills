# Changelog

All notable changes to this project are documented here.

## [1.2.1] - 2026-09-07 (unreleased; development/review-pending)

### Added

- Standard-library structured JSON renderer and schema-backed example input.
- Minimal PEP 621 project metadata with an explicit empty runtime dependency list.
- Release manifest defining the generic package allowlist and excluded evidence/local files.
- Minimal GitHub Actions CI workflow for pushes and pull requests; it uses the standard library for project checks and adds no `pypdf` or `jsonschema` dependency. This unreleased entry records configuration only, not a remote run.
- Review-pending appendix and delivery-contract specification covering optional data appendices, QA evidence manifests, and package handoffs; no runtime support is claimed by this entry.

### Changed

- Qualified A4, pagination, footer placement, and logical-page claims so browser/PDF output is verified rather than guaranteed.
- Documented Kimi WebBridge as the recommended interactive/PDF preview path and Playwright as a formal repeatable E2E option.
- Sanitized generic text examples and regenerated the structured HTML example from its fixture.
- Kept legacy binary preview artifacts outside the generic release allowlist until they are regenerated from sanitized fixtures.
- Hardened custom CSS checks against escaped and comment-spliced `@import`/`url()` tokens, and converted malformed grid column values into contract errors instead of raw type errors.