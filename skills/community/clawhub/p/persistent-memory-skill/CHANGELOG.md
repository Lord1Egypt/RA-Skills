# Changelog

## v0.8.0 — 2026-07-15

- Added optional Summary-first loading for active on-demand memory files.
- Preserved full-file loading for legacy files without a valid Summary.
- Required reviewed summary updates whenever a confirmed body change affects a summarized fact.
- Kept `_core/`, indexes, and archives outside the feature scope.
- Kept section-level loading, automatic summary creation, and bulk migration out of scope.

## v0.7.1 — 2026-07-14

- Added `memory upgrade` / `升级记忆` for existing memory roots missing lifecycle folders.
- Added normalized relative-path validation, protected core/control paths, and explicit confirmation before lifecycle changes.
- Added destination-collision refusal and preserved active index lines for reliable recovery.
- Required active files to be archived before deletion and separated expired-trash confirmation from normal health checks.
- Corrected baseline-loading, compatibility, and cross-agent wording in both README files.
- Defined the boundary between managed memory and raw project materials.
- Corrected the directory tree and initialization steps in both skill files.
- Clarified that Summary-first and section-level loading are not part of this release.

## v0.7

- Added archive, delete, recover, and memory-health lifecycle instructions.
