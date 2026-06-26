# Release Patterns - GitHub Actions

Use this file for versioned releases, deploy approval flow, and artifact promotion.

## Tag-Driven Release Baseline

Use tags when the release should map cleanly to a versioned artifact:

```yaml
name: release

on:
  push:
    tags:
      - "v*.*.*"

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - run: ./scripts/build-release.sh
      - uses: softprops/action-gh-release@v2
        with:
          files: dist/*
```

## Build Once, Promote Later

For serious delivery systems:
- validation workflow builds and verifies the artifact
- release workflow promotes that exact artifact
- deploy workflow consumes the promoted artifact in the target environment

This keeps the chain of custody clear.

## Environment-Gated Deploy Pattern

Use environments for non-trivial deploys:

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - run: ./scripts/deploy.sh
```

Keep production approval in the environment, not hidden in shell prompts.

## Manual Release Dispatch

`workflow_dispatch` is useful for controlled releases when inputs matter.
Use it when:
- release windows are manual
- one artifact can go to multiple environments
- rollback or hotfix inputs must be explicit

Validate every input and do not expose production deploy options to untrusted callers.

## Rollback Readiness

Before calling a release workflow "done", know:
- which artifact version is live
- which previous artifact can be promoted back
- who can approve rollback
- whether database or infrastructure changes need separate reversal

GitHub Actions can coordinate rollback, but it cannot invent a missing rollback plan.
