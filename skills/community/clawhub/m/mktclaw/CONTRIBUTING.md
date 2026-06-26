# Contributing to MktClaw

## How to Contribute

### Bug Reports & Feature Requests

Open a GitHub issue using the appropriate template. Provide as much context as possible — including the Agent type, industry, and expected vs actual output.

### Pull Requests

1. **Fork** the repo and create a branch from `main`.
2. **Run evals** before submitting: `python scripts/test_runner.py --evals evals/evals.json --results results.json`
3. **Update version** if changing behavior: bump `version.json` following semver convention.
4. **Open a PR** against `main` with a clear description of what changed and why.

### Code Style

- Python: `black` + `isort` + `flake8` (see `.pre-commit-config.yaml`)
- Markdown: Keep lines under 100 chars where possible
- YAML: 2-space indentation

### Commit Messages

Follow conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`

### Questions

Open a Discussion or contact the maintainers via Issues.
