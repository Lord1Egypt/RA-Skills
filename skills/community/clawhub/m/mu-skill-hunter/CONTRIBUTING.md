# Contributing to mu-skill-hunter

Thank you for your interest in contributing! This project welcomes contributions of all kinds.

## How to Contribute

### Reporting Bugs

1. Check existing issues to avoid duplicates
2. Open a new issue using the Bug Report template
3. Include: OS, Python version, error output, steps to reproduce

### Suggesting Features

1. Open an issue using the Feature Request template
2. Describe the use case and expected behavior
3. If possible, sketch a rough implementation plan

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes — keep Python scripts stdlib-only (no external pip packages)
4. Test your changes locally
5. Commit with a clear message: `feat: add X` / `fix: resolve Y` / `docs: update Z`
6. Open a PR using the PR template

## Development Guidelines

- **Python 3.8+ stdlib only** — no external pip dependencies
- **External CLIs are optional** — the tool must degrade gracefully when `clawhub`, `skillhub`, or `skills` CLI is not installed
- **Security first** — never output raw code from scanned skills; scanner output is summary-only
- **Parallel over sequential** — use `subprocess.Popen` for parallel CLI calls with per-call timeouts

## Code Style

- Follow PEP 8
- Use type hints where helpful
- Keep functions focused and well-documented
- Comments in English or Chinese are both acceptable

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
