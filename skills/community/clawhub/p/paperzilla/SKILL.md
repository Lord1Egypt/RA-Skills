---
name: paperzilla
description: Use the Paperzilla CLI (pz) to browse research projects and feeds, inspect canonical papers and project recommendations, leave feedback, export JSON, and generate Atom feed URLs. Trigger when users ask to check Paperzilla feeds, list projects, inspect paper details, tune recommendations, or automate feed workflows.
version: 0.3.1
homepage: https://docs.paperzilla.ai/guides/cli
metadata: { "openclaw": { "requires": { "bins": ["pz"] }, "homepage": "https://docs.paperzilla.ai/guides/cli" } }
---

# Paperzilla CLI (`pz`) 🦖

Use `pz` to read canonical papers, browse project recommendations, inspect projects, leave recommendation feedback, and automate Paperzilla workflows from the terminal.

Prefer `--json` whenever an agent needs structured output.

## Install

### macOS
```bash
brew install paperzilla-ai/tap/pz
```

### Windows (Scoop)
```bash
scoop bucket add paperzilla-ai https://github.com/paperzilla-ai/scoop-bucket
scoop install pz
```

### Linux
```bash
curl -sL https://github.com/paperzilla-ai/pz/releases/latest/download/pz_linux_amd64.tar.gz | tar xz
sudo mv pz /usr/local/bin/
```

### Build from source (Go 1.23+)
```bash
git clone https://github.com/paperzilla-ai/pz.git
cd pz
go build -o pz .
mv pz /usr/local/bin/
```

## Update

First check the currently installed version:

```bash
pz --version
```

Then ask `pz` how it should be upgraded:

```bash
pz update
```

`pz update` detects common install methods and prints the right upgrade instructions for:
- Homebrew
- Scoop
- GitHub release binaries
- source builds

If detection is ambiguous, override it explicitly:

```bash
pz update --install-method homebrew
pz update --install-method scoop
pz update --install-method release
pz update --install-method source
```

Common upgrade paths:

### macOS
```bash
brew update
brew upgrade pz
```

### Windows
```bash
scoop update pz
```

### Linux / Releases
```bash
curl -sL https://github.com/paperzilla-ai/pz/releases/latest/download/pz_linux_amd64.tar.gz | tar xz
sudo mv pz /usr/local/bin/
```

### Source install
```bash
git pull
go build -o pz .
sudo mv pz /usr/local/bin/
```

## Authentication

```bash
pz login
```

You need login for project-oriented commands like `project`, `feed`, `rec`, and `feedback`.

## Core model: canonical papers vs project recommendations

This distinction matters:
- `pz paper <paper-ref>` works with a **canonical Paperzilla paper**
- `pz rec <project-paper-ref>` works with a **recommendation inside one project**

A canonical paper is shared globally. A recommendation is that paper as it appears in one specific project, with project-specific relevance and feedback.

## Core commands

### Check for updates
```bash
pz update
```

### List projects
```bash
pz project list
```

### Show one project
```bash
pz project <project-id>
```

### Browse project feed
```bash
pz feed <project-id>
```

Useful flags:
- `--must-read`
- `--since YYYY-MM-DD`
- `--limit N`
- `--json`
- `--atom`

Examples:
```bash
pz feed <project-id> --must-read --since 2026-03-01 --limit 5
pz feed <project-id> --json
pz feed <project-id> --atom
```

### Inspect a canonical paper
```bash
pz paper <paper-id-or-short-id>
pz paper <paper-id-or-short-id> --json
pz paper <paper-id-or-short-id> --markdown
```

Use `pz paper --project <project-id>` when you want to resolve that canonical paper inside one of your projects and see recommendation context.

Example:
```bash
pz paper <paper-id> --project <project-id>
```

### Inspect a project recommendation
```bash
pz rec <project-paper-id-or-short-id>
pz rec <project-paper-id-or-short-id> --json
pz rec <project-paper-id-or-short-id> --markdown
```

Use `pz rec` when the identifier came from `pz feed --json`.

### Leave recommendation feedback
```bash
pz feedback <project-paper-id> upvote
pz feedback <project-paper-id> star
pz feedback <project-paper-id> downvote --reason not_relevant
pz feedback <project-paper-id> downvote --reason low_quality
pz feedback clear <project-paper-id>
```

Feedback is **project-specific**. The same canonical paper can have different feedback in different projects.

## Output and automation

- Prefer `--json` for machine parsing.
- Use recommendation IDs from `pz feed --json` with `pz rec` and `pz feedback`.
- Use canonical paper IDs with `pz paper`.
- `--atom` returns a personal feed URL for feed readers.
- `pz rec --markdown` may queue markdown generation if needed.
- Anonymous `pz paper --markdown` only prints markdown when it is already available.

## Agent usage guidance

- If the user asks to inspect a paper from a project feed, prefer `pz rec` first.
- If the user asks about the paper as a global/canonical object, use `pz paper`.
- For scripting, fetch feeds with `--json` and then pass IDs into `pz rec`, `pz feedback`, or `pz paper` as appropriate.

## Configuration

```bash
export PZ_API_URL="https://paperzilla.ai"
```

## References

- Docs: https://docs.paperzilla.ai/guides/cli
- Quickstart: https://docs.paperzilla.ai/guides/cli-getting-started
- Repo: https://github.com/paperzilla-ai/pz
