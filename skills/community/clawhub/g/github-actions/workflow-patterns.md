# Workflow Patterns - GitHub Actions

These snippets are for workflow files inside `.github/workflows/`.
Placeholders such as `${{ github.* }}` and `${{ secrets.* }}` are resolved by GitHub Actions, not by the agent.

## Baseline Validation Workflow

Use this shape for most repos that need pull request validation plus main-branch checks:

```yaml
name: ci

on:
  pull_request:
  push:
    branches: [main]

concurrency:
  group: ci-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - run: npm test
      - run: npm run build
```

## Reusable Workflow vs Composite Action

Use `workflow_call` when:
- multiple repos need the same job contract
- permissions, environments, or secrets vary by caller
- outputs should flow back to the parent workflow

Use a composite action when:
- the repeated logic is a step bundle, not a workflow policy
- the caller should keep control of jobs, runners, and permissions

## Reusable Workflow Skeleton

```yaml
name: reusable-node-ci

on:
  workflow_call:
    inputs:
      node-version:
        required: false
        type: string
        default: "20"

jobs:
  test:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
          cache: npm
      - run: npm ci
      - run: npm test
```

## Matrix Guidance

Use a matrix when it changes release confidence, not just because the feature exists.

- Strong use cases: multiple operating systems, supported runtimes, or shard counts
- Weak use cases: duplicate smoke tests with no compatibility value
- Add `fail-fast: false` only when partial failures still teach something useful
- Cap matrix size before minutes and log volume dominate feedback quality

## Artifact Promotion Pattern

Build once, test once, promote the exact artifact:
- build job produces versioned artifact
- verification jobs consume that artifact
- release or deploy job promotes the verified artifact instead of rebuilding

This avoids "tested one thing, shipped another" drift.
