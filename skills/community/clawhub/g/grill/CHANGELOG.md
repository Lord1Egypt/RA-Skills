# grill changelog

Earlier history lives in the repo-level CHANGELOG.md.

## 0.1.2 - 2026-08-08

- Added the shared Untrusted content section required for skills that ingest external data.

## 0.1.1 - 2026-08-08

- Added deterministic unit tests for `scripts/grill-scan.sh` under `tests/` (14 cases covering each scanner section, exit codes, and the fence-aware tilde check) and declared the test command in skill.json, per the repository script-test contract.

## 0.1.0 - 2026-07-08

- Added skill.json metadata (tests, changelog) for the Brigade skill registry.
