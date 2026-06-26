# Coding & Development

## Languages & Runtimes
- Node.js (v22), Python 3, Go available on this system
- Use `exec` to run any CLI tool
- Package managers: npm, pip, go install

## Git Workflow
- `git status`, `git diff`, `git log` for context
- `git add`, `git commit`, `git push` for changes
- Branch strategy: feature branches, PR-based merge
- Use `gh` CLI for GitHub operations (PRs, issues, CI)

## Code Patterns

### Project Setup
- Initialize with appropriate tooling (npm init, go mod init, etc.)
- Set up linting (eslint, ruff, golangci-lint)
- Configure CI/CD (GitHub Actions, etc.)

### Debugging
- Read error messages carefully
- Use `console.log` / `print` for quick debugging
- Check dependencies and versions
- Reproduce in isolation

### Refactoring
- Make small, testable changes
- Run tests after each change
- Use grep/search for impact analysis

## Delegation
- Use `coding-agent` skill for complex coding tasks
- Spawn sub-agents for parallel work via `sessions_spawn`
- Kilo CLI for autonomous terminal coding: `kilo run --auto "task"`

## Best Practices
- Write readable code over clever code
- Document non-obvious decisions
- Keep functions small and focused
- Use meaningful variable names
- Handle errors explicitly

## Available CLIs
- `gh` — GitHub operations
- `git` — Version control
- `node` / `npm` — JavaScript ecosystem
- `python3` / `pip` — Python ecosystem
- `go` — Go development
- `kilo` — Agentic coding assistant
