# 🌿 Gitrama — Git History Intelligence for OpenClaw

Gitrama brings AI-powered semantic search and intelligence to your Git history, directly through your OpenClaw assistant.

## What It Does

Ask your OpenClaw agent natural language questions about any git repository:

- **"What changed in the auth module this week?"** → AskGIT analyzes commits, diffs, and contributors to give you a clear answer
- **"Write me a commit message"** → Analyzes staged changes and generates a proper conventional commit
- **"Create a branch name for adding OAuth"** → Generates `feature/add-oauth-authentication`
- **"Who's been working on the API?"** → Contributor insights with activity patterns

## Features

| Feature | Command | Description |
|---------|---------|-------------|
| AskGIT Chat | `gtr chat` | Semantic Q&A about your repo history |
| Smart Commits | `gtr commit` | AI-generated conventional commit messages |
| Branch Names | `gtr branch` | Clean branch names from task descriptions |
| Repo Insights | `gtr chat` | Contributor analysis, change patterns |

## How to Use

1. Install the skill: `clawhub install gitrama`
2. Make sure gitrama is installed: `pip install gitrama`
3. Navigate to any git repo and ask your OpenClaw agent about it

No API keys needed — all AI processing is handled server-side via api.gitrama.ai.

## Examples

> "Hey, can you check what's changed in this repo over the last week?"

> "Generate a commit message for my staged changes"

> "Create a branch name for the ticket: implement rate limiting on the API"

> "Who are the top contributors to the frontend directory?"

## How It Works

```
Local CLI (gtr) → gathers git context → POST to api.gitrama.ai → AI response
```

Git context is collected locally. AI processing happens on Gitrama's servers. Nothing sensitive runs on your machine.

## Requirements

- Python 3.8+
- Git

## Links

- 🌐 Website: [gitrama.ai](https://gitrama.ai)
- 📦 PyPI: [pypi.org/project/gitrama](https://pypi.org/project/gitrama/)

## License

© 2026 Gitrama. All Rights Reserved.
