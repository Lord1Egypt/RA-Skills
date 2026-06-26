# CLAUDE.delegate.md

This is the open-source Claude Delegate repo.

## Before changing behavior
- Read `README.md`, `SKILL.md`, and `references/setup.md` first.
- If you change `scripts/`, keep the docs aligned with the real runtime behavior.
- Preserve portable OSS defaults. Do not bake Henry-specific machine paths into the public package unless they are clearly examples or env overrides.

## Priority
- Keep install and first-run behavior obvious.
- Keep the difference between the local delegate lane and ACP explicit.
- Keep new bootstrap behavior simple enough that operators can understand and override it.
