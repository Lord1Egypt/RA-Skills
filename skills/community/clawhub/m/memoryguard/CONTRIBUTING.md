# Contributing to MemoryGuard

Thanks for your interest in contributing! This guide covers the basics.

## Reporting Bugs

Open a [GitHub Issue](../../issues) and include:

- **MemoryGuard version** (`memoryguard --version`)
- **OS and Python version**
- **Steps to reproduce** — exact commands you ran
- **Expected vs. actual behavior**
- **Relevant logs** (remove any secrets/tokens first)

Before opening a new issue, search existing ones to avoid duplicates.

## Submitting a Pull Request

1. **Fork** the repository and clone your fork.
2. **Create a branch** from `main`:
   ```bash
   git checkout -b feature/my-feature
   ```
3. **Make your changes**. Keep commits focused — one logical change per commit.
4. **Run tests** (see below).
5. **Open a Pull Request** against `main`.

In your PR description, include the following checklist:

```
- [ ] I have read and agree to the CLA (see CLA.md)
- [ ] I have added tests for my changes (or explained why tests are not needed)
- [ ] All existing tests pass
- [ ] I have not introduced new third-party dependencies without discussion
```

PRs without the CLA checkbox confirmed will not be merged.

## Code Style

- Follow existing **PEP 8** style. Match the style you see in surrounding code.
- **Pure standard library first.** MemoryGuard avoids runtime third-party
  dependencies. Do not add new dependencies without opening an issue to
  discuss it first.
- Keep functions small and focused. Prefer explicit over clever.
- No network calls, no telemetry, no account systems in the open-source core.

## Testing

Run the full test suite from the repository root:

```bash
cd memoryguard
python -m unittest discover -s tests
```

Tests use only the standard library (`unittest`). No pytest or extra
test-runner dependencies required.

When adding a feature or fixing a bug, add a test that verifies the **intent**
of the change — not just that the code runs, but that it solves the problem
described in the issue.

## Branch Strategy

- **`main`** — always stable. Releases are tagged from `main`.
- **Feature branches** — develop new work on `feature/*` or `fix/*` branches,
  then merge via PR.
- Avoid long-lived branches. Rebase onto `main` before opening a PR if `main`
  has moved ahead.

## Questions?

Open an issue with the `question` label, or start a discussion in the
Discussions tab. We are happy to help.
