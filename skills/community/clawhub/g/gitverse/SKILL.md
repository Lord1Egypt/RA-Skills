---
name: gitverse
description: GitVerse API integration for working with repositories, issues, and pull requests. Use when Codex needs to interact with GitVerse (gitverse.ru) for operations including listing or viewing repositories (personal or organization), listing or inspecting issues, listing viewing or creating pull requests, getting repository information, or any other GitVerse operations.
---

# GitVerse Skill

OpenClaw skill for GitVerse API integration.

## When to Use

Use this skill when you need to:
- List or view repositories
- List or view issues
- List, view, or create pull requests
- View repository information

## Installation

```bash
cd ~/.nvm/versions/node/v22.12.0/lib/node_modules/openclaw/skills/gitverse
npm install
npm run build
```

## Configuration

Set environment variable:
```bash
export GITVERSE_TOKEN=your_token_here
```

Or create `.env` file in the skill directory:
```
GITVERSE_TOKEN=your_token_here
```

## Usage

Run commands via node:
```bash
node ~/.nvm/versions/node/v22.12.0/lib/node_modules/openclaw/skills/gitverse/dist/index.js <command>
```

## Commands

### Repositories

```bash
# List your repositories
node dist/index.js repos list

# List organization repositories
node dist/index.js repos list --org <org>

# Get repository info
node dist/index.js repos info --owner <owner> --repo <repo>
```

### Issues

```bash
# List issues
node dist/index.js issues list --owner <owner> --repo <repo>
node dist/index.js issues list --owner <owner> --repo <repo> --state open

# View issue
node dist/index.js issues view --owner <owner> --repo <repo> --number <number>

# List issue comments
node dist/index.js issues comments --owner <owner> --repo <repo> --number <number>
```

### Pull Requests

```bash
# List pull requests
node dist/index.js pulls list --owner <owner> --repo <repo>
node dist/index.js pulls list --owner <owner> --repo <repo> --state open

# View pull request
node dist/index.js pulls view --owner <owner> --repo <repo> --number <number>

# Create pull request
node dist/index.js pulls create --owner <owner> --repo <repo> --title "Title" --head feature --base main

# List PR commits
node dist/index.js pulls commits --owner <owner> --repo <repo> --number <number>

# List PR files
node dist/index.js pulls files --owner <owner> --repo <repo> --number <number>
```

## Usage with OpenClaw

When you ask me to work with GitVerse, I will use this skill:

```
"Покажи мои репозитории"
→ node dist/index.js repos list

"Покажи issues в saic/ai_minister"
→ node dist/index.js issues list --owner saic --repo ai_minister

"Создай PR в saic/chatbot"
→ node dist/index.js pulls create --owner saic --repo chatbot --title "..." --head feature --base main
```

## Notes

- Requires GITVERSE_TOKEN environment variable
- API base URL: https://api.gitverse.ru
- Rate limits are handled by the SDK
- All commands output JSON

## Publishing to ClawHub

This skill is published on [ClawHub](https://clawhub.ai/skill/gitverse).

To install:
```bash
clawhub install gitverse
```

## Repository

Source code available on [GitVerse](https://gitverse.ru/v.shakhunov/gitverse-skill).

## License

MIT-0
