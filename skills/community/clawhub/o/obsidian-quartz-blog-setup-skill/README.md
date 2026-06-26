# Obsidian Quartz Blog Setup

A skill for AI coding agents that automates the complete setup of a [Quartz v4](https://quartz.jzhao.xyz/) static blog from an [Obsidian](https://obsidian.md) vault, with deployment to [GitHub Pages](https://pages.github.com/) via GitHub Actions.

## What It Does

Given your Obsidian vault path and a few configuration items, this skill guides the AI agent through:

1. **Environment check** — verifies Git, Node.js (>= 20), npm are available
2. **Install Quartz** — clones the official Quartz v4 repo and runs `npm install`
3. **Initialize** — runs `npx quartz create` with Obsidian-compatible settings
4. **Sync notes** — copies all `.md` files from your vault to Quartz's `content/` directory, excluding `.obsidian/`, `.trash/`, `.git/`, `node_modules/`
5. **Local preview** — builds and serves the site at `http://localhost:8080`
6. **Configure** — updates `quartz.config.ts` with your site title and base URL
7. **Deploy** — creates a GitHub Actions workflow (`deploy.yml`) using the official `actions/deploy-pages@v4`, cleans up inherited Quartz workflows, and pushes to the `v4` branch

The entire process requires only one round of user input (vault path, project directory, GitHub repo URL, site title, base URL).

## Installation

### Claude Code

```bash
# Navigate to your Claude skills directory
cd ~/.claude/skills   # macOS/Linux
cd %USERPROFILE%\.claude\skills   # Windows

# Clone this skill
git clone https://github.com/orbisz/obsidian-quartz-blog-setup.git
```

After cloning, restart Claude Code or start a new session. The skill will be automatically detected.

### Codex (OpenAI)

```bash
# Navigate to your Codex skills directory
cd ~/.codex/skills   # macOS/Linux
cd %USERPROFILE%\.codex\skills   # Windows

# Clone this skill
git clone https://github.com/orbisz/obsidian-quartz-blog-setup.git
```

Restart Codex to load the new skill.

### OpenCode

```bash
# Navigate to your OpenCode skills directory
cd ~/.opencode/skills   # macOS/Linux
cd %USERPROFILE%\.opencode\skills   # Windows

# Clone this skill
git clone https://github.com/orbisz/obsidian-quartz-blog-setup.git
```

### Generic (Any AI tool that supports SKILL.md)

If your tool uses a different skills directory, just clone into the appropriate location:

```bash
git clone https://github.com/orbisz/obsidian-quartz-blog-setup.git <your-skills-dir>/obsidian-quartz-blog-setup
```

The skill is a single `SKILL.md` file — no dependencies, no build step.

## Usage

Once installed, tell your AI agent something like:

> "帮我把 Obsidian 笔记部署为 Quartz 博客，我的知识库在 C:\Users\xxx\my-vault"

Or in English:

> "Set up a Quartz blog from my Obsidian vault and deploy it to GitHub Pages"

The skill will ask for the remaining configuration and handle the rest.

## Prerequisites

- **Obsidian** with a vault of Markdown notes
- **Git** — [install](https://git-scm.com/downloads)
- **Node.js >= 20** (LTS recommended) — [install](https://nodejs.org/)
- **A GitHub account** with a new empty repository created (no README, .gitignore, or license)
- **GitHub Pages** enabled on the repository with Source set to "GitHub Actions"

## File Structure

```
obsidian-quartz-blog-setup/
├── SKILL.md    # The skill definition (instructions for the AI agent)
└── README.md   # This file
```

## Companion Skill

For incremental updates after the initial setup (syncing new/changed notes and pushing to GitHub), use the companion skill: [obsidian-wiki-blog-push](https://github.com/orbisz/obsidian-wiki-blog-push).

## License

MIT
