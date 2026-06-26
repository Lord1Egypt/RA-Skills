# Export Policy

## Principle

The export process must ensure that the artifact is entirely self-contained, scrubbed of host-specific context, and strictly follows the boundaries of a single skill. It must not leak internal implementation details or proprietary paths.

## What is Exported

- `SKILL.md`: The main definition of the skill.
- `refs/*.md`: Documentation and reference materials.
- `scripts/*.py`: Executable tools and workflow drivers.
- `policies/*.json`: High-level policies like the workflow or audit configuration.
- `tool/*.json`, `state/*.json`, `policy/*.json`: The 3-layer runtime skeleton configurations.

## What is Blocked

- `__pycache__`, `.git`, `.artifacts`, and other temporary directories.
- Host absolute paths (e.g., `<root_dir>/...` or `<disk_drive>:\...`).
- Explicit network literals (e.g., `http(s)://...` or hardcoded internal domains).
- Any content that fails the constraint checks before publishing.

## Pre-Export Checklist

1. Does the code execute without reliance on missing files?
2. Are all the necessary layers (`tool`, `state`, `policy`) present?
3. Has `run_constraints.py` been run and passed without errors?
4. Does the export directory pass the `run_audit.py` checks?
