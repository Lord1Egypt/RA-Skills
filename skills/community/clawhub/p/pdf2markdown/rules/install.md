---
name: pdf2markdown-cli-installation
description: |
  Install the PDF2Markdown CLI and handle authentication.
  Package: https://www.npmjs.com/package/pdf2markdown-cli
  Docs: https://pdf2markdown.io/docs
  Cross-platform: macOS, Windows, Linux
---

# PDF2Markdown CLI Installation

Supports **macOS, Windows, Linux**.

## Quick setup

```bash
npx -y pdf2markdown-cli init -y
```

Installs the CLI, configures authentication, and installs skills. Verify:

```bash
npx pdf2markdown-cli --version
```

## Manual install

Choose by package manager:

```bash
# npm (default)
npm install -g pdf2markdown-cli

# pnpm
pnpm add -g pdf2markdown-cli

# yarn
yarn global add pdf2markdown-cli
```

## Verify

After global install, both `pdf2markdown` and `pdf2md` are available:

```bash
pdf2markdown --status
# or
pdf2md --status
```

## Authentication

Get an API key from https://pdf2markdown.io/dashboard.

```bash
pdf2markdown login
# or
pdf2markdown login --api-key "p2m_live_xxxx"
```

Environment variable (all platforms):

```bash
# macOS / Linux
export PDF2MARKDOWN_API_KEY="p2m_live_xxxx"

# Windows (CMD)
set PDF2MARKDOWN_API_KEY=p2m_live_xxxx

# Windows (PowerShell)
$env:PDF2MARKDOWN_API_KEY="p2m_live_xxxx"
```

## Install skills

```bash
# Install to all detected agents
pdf2markdown setup skills
# or
pdf2md setup skills

# Install to a specific agent
pdf2markdown setup skills --agent cursor
pdf2md setup skills --agent opencode
```

Supported agents: `cursor`, `codex`, `claude`, `opencode`, `agents`, `windsurf`, `continue`, `project` (project installs to `.cursor/skills` and `.opencode/skills`, same as firecrawl/skills).

## Windows notes

- Ensure Node.js and npm are in PATH
- Global install may require admin rights, or use `npx pdf2markdown-cli` to avoid global install
- Credentials are stored in `%APPDATA%\pdf2markdown-cli\`

## Command not found

If neither `pdf2markdown` nor `pdf2md` is found:

1. Check npm global bin is in PATH: `npm bin -g`
2. Use npx: `npx pdf2markdown-cli --version`
3. Reinstall: `npm install -g pdf2markdown-cli`
