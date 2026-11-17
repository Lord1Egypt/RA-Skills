# Contributing to mu-dev-workflow

Thank you for your interest in contributing! This project follows a design-first methodology — please read the [SKILL.md](SKILL.md) workflow before starting any work.

## How to Contribute

1. **Open an issue first** — describe the problem or feature you want to work on
2. **Wait for discussion** — maintainers will confirm the direction before any code is written
3. **Fork & branch** — create a feature branch from `main`
4. **Follow the workflow** — design doc → critical self-check → implementation → verification
5. **Submit a PR** — use the PR template, include verification output

## Development Workflow

This project dogfoofs its own methodology. When contributing:

- **Stage 1**: Clarify requirements (open an issue, discuss)
- **Stage 2**: Design with critical self-check (three questions: real problem? reinventing the wheel? edge cases?)
- **Stage 3/4**: Implement with sub-agent review if needed
- **Stage 5**: Verify with actual command output (no "should work")

## Code Style

- Markdown files: follow existing formatting conventions
- Keep SKILL.md under 300 lines (excluding frontmatter)
- One concept per file in references/
- No external dependencies — pure Markdown

## Reporting Issues

Use the issue templates provided. Please include:
- What you expected to happen
- What actually happened
- Steps to reproduce
- Your agent environment (Claude Code, Cursor, CatPaw, etc.)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
