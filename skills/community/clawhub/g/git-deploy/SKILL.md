---
name: git-deploy
description: Simple deployment skill for local git operations. Use when you need to add, commit, and push changes to the Git repository. Designed for quick local deployments (Tasks #3, #4, #5).
---

# Git Deploy

## Overview

This skill automates the standard git workflow for local development:
- Stage all changes
- Commit with a message
- Push to the current branch

The script uses pre-configured repository URL and token.

## Usage

```bash
scripts/deploy.sh "feat: Task #X - Description"
```

## Repository

- **URL**: http://git.homelab:3000/vitali/SigmaFlow-Svelte.git
- **Token**: c865b793f09a3b79b65ebdfbd75c5b17395188d2

## Notes

- The script assumes it is run in the project root.
- If you need to push to a specific branch, modify the script or commit message.
