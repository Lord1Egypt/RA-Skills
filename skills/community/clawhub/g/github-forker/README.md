# github-forker

A Claude Code skill that extracts GitHub repository URLs from text or images, forks them, and stars the originals — all in one step.

## Features

- Extract GitHub URLs from plain text (with or without `https://`, with sub-paths)
- Extract GitHub URLs from screenshots or images (via vision)
- Resolve truncated URLs (e.g. `github.com/owner/re...`) using GitHub search + context inference
- Fork all found repositories via GitHub API
- Star the original repository after each successful fork
- Batch support: handles multiple repos in a single message

## Installation

Copy the skill directory to `~/.claude/skills/`:

```bash
cp -r github-forker ~/.claude/skills/github-forker
```

## Setup

This skill uses the GitHub REST API via `curl` — no `git` CLI or SSH key required.

### 1. Install curl

**macOS** — pre-installed. Verify:
```bash
curl --version
```

**Ubuntu / Debian**
```bash
sudo apt update && sudo apt install curl -y
```

**Windows** — included in Windows 10/11. Or install via [curl.se](https://curl.se/windows/).

### 2. GitHub Token

Generate a classic PAT with `repo` or `public_repo` scope:
**GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)**

```bash
# Set for current session
export GITHUB_TOKEN="ghp_..."

# Persist across sessions
echo 'export GITHUB_TOKEN="ghp_..."' >> ~/.zshrc   # zsh
echo 'export GITHUB_TOKEN="ghp_..."' >> ~/.bashrc  # bash
```

## Usage

Just mention a GitHub repo and ask to fork it:

```
帮我 fork 这个：https://github.com/owner/repo
fork this: github.com/owner/repo
copy this repo to my account: https://github.com/owner/repo/tree/main/subdir
```

Works with truncated URLs from screenshots too:

```
fork git [image with github.com/owner/re...]
```

The skill will infer the full repo from context, fork it, and star the original automatically.
