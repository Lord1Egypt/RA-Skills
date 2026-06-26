# Contributing

## Scope

This repo ships an OpenClaw skill. Changes should keep the command surface stable unless the release explicitly says otherwise.

Current supported commands:

- `/preflight`
- `/audit`
- `/optimize`
- `purge sessions`

## Workflow

1. Make the smallest coherent change.
2. Keep docs aligned across `SKILL.md`, `README.md`, `SECURITY.md`, and `CHANGELOG.md`.
3. If behavior changes, document it in release notes under `docs/release-notes/`.
4. Run `scripts/verify.sh` before opening or merging a change.

## Documentation expectations

- `README.md` is the landing page and should stay lean.
- `SECURITY.md` holds operational and security detail that would clutter the README.
- `CHANGELOG.md` is the canonical history file.
- Release notes should match the changelog entry for the same version.

## Release hygiene

- Bump the version in `SKILL.md` when the skill package changes.
- Add a dated entry to `CHANGELOG.md`.
- Add or update `docs/release-notes/<version>.md`.
- If a GitHub Release exists, update its body to match the release-notes file.

## Verification

```bash
bash scripts/verify.sh
```
