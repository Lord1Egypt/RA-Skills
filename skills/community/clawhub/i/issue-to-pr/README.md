# 🔧 issue-to-pr

[![Skills.sh](https://img.shields.io/badge/skills.sh-issue--to--pr-blue)](https://skills.sh/4yDX3906/issue-to-pr)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An AI Agent Skill that automatically reads a GitHub issue, analyzes the codebase, implements a fix, and submits a pull request — end-to-end, with one confirmation.

---

## ⚡ Quick Install

```bash
npx skills add 4yDX3906/issue-to-pr
```

Or install via [ClawHub](https://clawhub.com):

```bash
clawhub install issue-to-pr
```

> **That's it!** Once installed, just give your AI agent a GitHub issue URL and watch it work.

---

## ✨ Features

- **8-Phase Automated Workflow** — from issue parsing to automatic PR submission
- **GitHub CLI Integration** — uses `gh` for fast, authenticated access with `fetch_content` fallback
- **Smart Repo Detection** — auto-detects if you're already in the right repo or clones it
- **Default Branch Detection** — automatically identifies `main`, `master`, or custom default branches
- **Minimal Diffs** — changes only what's necessary, respecting existing code style
- **Built-in Verification** — runs tests, linting, and format checks before finishing
- **Interactive PR Submission** — review changes first, then auto-submit with one confirmation
- **Auto-Fork Support** — automatically forks repositories when you lack write access
- **Structured Output** — generates commit messages and PR descriptions ready to use

## 📋 Prerequisites

| Tool | Required | Notes |
|------|----------|-------|
| `git` | ✅ Yes | Must be installed and configured |
| `gh` (GitHub CLI) | 📌 Recommended | Enables fast issue fetching and PR creation. Install: [cli.github.com](https://cli.github.com) |

## 📦 Installation

### Option 1: ClawHub (Recommended)

```bash
clawhub install issue-to-pr
```

### Option 2: One-Line Install Script

```bash
bash scripts/install.sh
```

Or directly from the repo:

```bash
git clone https://github.com/ClawHub/issue-to-pr.git
cd issue-to-pr
bash scripts/install.sh
```

### Option 3: Manual Install

```bash
mkdir -p ~/.qoder/skills/issue-to-pr
cp SKILL.md ~/.qoder/skills/issue-to-pr/SKILL.md
```

## 🚀 Usage

In your AI-powered editor (Qoder, Cursor, Claude Code, etc.), simply provide a GitHub issue URL:

```
/fix-issue https://github.com/owner/repo/issues/123
```

Or describe it naturally:

```
Fix this GitHub issue: https://github.com/facebook/react/issues/12345
```

The agent will automatically:
1. Parse the issue URL and fetch details
2. Clone or locate the repository
3. Analyze the codebase to find the root cause
4. Implement a minimal fix
5. Run tests and linting
6. Present changes and wait for your confirmation
7. Auto-submit a PR (commit, push, and create PR) upon approval

## ⚙️ How It Works

```
  GitHub Issue    Parse & Fetch    Analyze Code    Implement Fix    Run Tests    Submit PR
 ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌─────────┐   ┌─────────┐
 │    📋    │ ─▶ │    🔍    │ ─▶ │    🧠    │ ─▶ │    🔧    │ ─▶ │   ✅    │─▶ │   🚀    │
 └──────────┘    └──────────┘    └──────────┘    └──────────┘    └─────────┘   └─────────┘
  Read issue      Fetch details    Trace code       Minimal fix     Lint & test   Push & PR
  from GitHub     & clone repo     & find root      respecting       to verify     with one
                                   cause            code style       quality       confirmation
```

| Phase | Description |
|-------|-------------|
| **1. Parse URL** | Extract `owner`, `repo`, and issue `number` from the GitHub URL |
| **2. Fetch Issue** | Retrieve issue title, body, labels, and comments via `gh` or web scraping |
| **3. Locate Repo** | Check the current workspace or clone the repository |
| **4. Analyze** | Search the codebase, trace code paths, and identify the root cause |
| **5. Implement Fix** | Apply minimal, style-consistent code changes |
| **6. Verify** | Run the project's test suite and linters |
| **7. Present Changes** | Show fix summary and diff, wait for user confirmation |
| **8. Submit PR** | Auto commit, push (with fork fallback), and create PR |

## 🔒 Security & Privacy

- All code analysis and modifications happen **locally on your machine**
- Only standard Git/GitHub operations (clone, push, PR) communicate with GitHub
- Uses your existing `gh` CLI authentication — no additional credentials stored
- The agent **never pushes code or creates PRs without your explicit approval**
- No telemetry or usage data is collected

## 🖥️ Supported Platforms

- [Qoder](https://qoder.ai)
- [Cursor](https://cursor.sh)
- [Claude Code](https://claude.ai)
- [Windsurf](https://windsurf.ai)
- [GitHub Copilot](https://github.com/features/copilot)

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
