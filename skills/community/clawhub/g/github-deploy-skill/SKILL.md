---
name: GitHub Deploy Skill
slug: github-deploy-skill
version: 1.0.0
description: Commit and push local project changes to GitHub, with optional repo creation and deployment hints.
author: cruciata
tags:
  - latest
  - github
  - deploy
  - powershell
---

# GitHub Deploy Skill

This skill provides a reusable PowerShell script for Windows to automate:

1. Git checks
2. Commit creation
3. Push to remote branch
4. Optional GitHub repository creation (via GitHub CLI)
5. Optional deployment hints (for Streamlit flow)

## Included file

- `github-deploy-skill.ps1`

## Parameters

- `-CommitMessage` (required): commit message text
- `-Repo` (optional): GitHub repository in `owner/repo` format
- `-Branch` (optional): target branch, default `main`
- `-CreateRepo` (optional switch): create repo with `gh` if missing
- `-SkipDeployHint` (optional switch): do not print deployment hint

## Usage

From any Git project folder:

```powershell
powershell -ExecutionPolicy Bypass -File .\github-deploy-skill.ps1 -CommitMessage "feat: update" -Repo "owner/repo" -Branch "main"
```

Create repository automatically:

```powershell
powershell -ExecutionPolicy Bypass -File .\github-deploy-skill.ps1 -CommitMessage "init" -Repo "owner/new-repo" -CreateRepo
```

## Expected output

- Success: commit and push completed
- Failure: explicit error with reason (missing command, auth, push/network, remote config)

## Requirements

- Git installed and available in PATH
- Network access to remote Git host
- If `-CreateRepo` is used: GitHub CLI (`gh`) installed and authenticated

## Notes

- Works with repositories that do not yet have a first commit.
- If `origin` does not exist, pass `-Repo` and the script will add it automatically.
