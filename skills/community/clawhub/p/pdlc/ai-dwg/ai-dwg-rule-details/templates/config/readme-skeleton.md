<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Template: README.md (Project Root)

```markdown
# {System Name}

{One-paragraph description from Architecture Vision}

## Quick Start

```bash
# Prerequisites: Docker, {runtime}, {package manager}

git clone {repo-url}
cp .env.example .env
docker compose up -d
{install-command}
{migrate-command}
{dev-command}
```

## Architecture

**Style:** {architecture style}
**Stack:** {primary technology}
**Docs:** See `info/PROJECT_INSTRUCTIONS.md` for full development guide

## Project Structure

```
{generated folder structure — modules list}
```

## Development

- **Setup:** See [PROJECT_INSTRUCTIONS.md](./PROJECT_INSTRUCTIONS.md)
- **Contributing:** See [CONTRIBUTING.md](./CONTRIBUTING.md)
- **Onboarding:** See [ONBOARDING.md](./ONBOARDING.md)

## Commands

| Command | Purpose |
|---------|---------|
| `{dev}` | Start dev server |
| `{test}` | Run tests |
| `{lint}` | Lint code |
| `{build}` | Build for production |

## Documentation

- Architecture rules: `rules/`
- Architecture decisions: `{adr-path}`
- API docs: `{api-docs-url}` (when running)

## License

{license type}
```
