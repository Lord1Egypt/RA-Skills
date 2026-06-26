# Release process

This repository is intended for local inspection before publishing.

## Pre-publish inspection

- Verify source files under `src/`
- Run `scripts/check.sh`
- Run `scripts/publish.sh --dry-run`
- Confirm package version and release notes

## Publish

Run `scripts/publish.sh` after checks pass.

## Current target release

- Version: `0.2.0`
