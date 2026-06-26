---
name: halo-blog
version: 1.0.0
description: Use when managing a Halo blog instance via CLI, including authentication, posts, pages, themes, plugins, attachments, backups, comments, moments, notifications, or public site search.
metadata:
  openclaw:
    category: content-management
    requires:
      bins: ["halo"]
    cliHelp: "halo --help"
---

# Halo Blog CLI Skill

A command-line tool skill for managing [Halo](https://www.halo.run) blog instances.

## Installation

```bash
npm install -g @halo-dev/cli
```

Verify:

```bash
halo --version
halo --help
```

Requirements: Node.js >= 22

## Quick Start

1. **Authenticate** (see [references/auth.md](references/auth.md)):
   ```bash
   halo auth login --profile local --url http://127.0.0.1:8090 --auth-type bearer --token <token>
   ```

2. **Create a post from Markdown** (see [content.md](references/content.md) for full format rules):
   ```bash
   halo post import-markdown --file ./article.md --force
   ```
   Markdown files are automatically converted to HTML by default; if conversion fails, falls back to raw Markdown import.

3. **List posts**:
   ```bash
   halo post list
   ```

## Command Areas

| Area | Commands | Reference |
|------|----------|-----------|
| Authentication | `halo auth *` | [auth.md](references/auth.md) |
| Publishing Rules | Markdown → HTML workflow, front matter, visibility checks | [publishing.md](references/publishing.md) |
| Posts & Pages | `halo post *`, `halo single-page *` | [content.md](references/content.md) |
| Themes, Plugins, Attachments, Backups, Moments | `halo theme *`, `halo plugin *`, `halo attachment *`, `halo backup *`, `halo moment *` | [operations.md](references/operations.md) |
| Comments & Notifications | `halo comment *`, `halo notification *` | [moderation.md](references/moderation.md) |
| Public Search | `halo search *` | [search.md](references/search.md) |

## Shared Conventions

- **Profile selection**: Use `--profile <name>` when working with multiple Halo instances.
- **JSON output**: Use `--json` for scripted or automated workflows.
- **Non-interactive safety**: Destructive commands (`delete`, `uninstall`, overwrite imports) usually require `--force` when run non-interactively.
- **Basic Auth requirement**: If using basic auth instead of bearer token, ensure Halo is started with `--halo.security.basic-auth.disabled=false`.

## Common Workflows

### Switch between environments

```bash
halo auth profile list
halo auth profile use production
```

### Export and import a post

```bash
halo post export-json my-post --output ./post.json
halo post import-json --file ./post.json --force
```

### Publish via Markdown file

```bash
halo post import-markdown --file ./article.md --force
```

### Upgrade all App Store themes/plugins

```bash
halo theme upgrade --all
halo plugin upgrade --all --yes
```

### Search public content without login

```bash
halo search --keyword "halo" --url https://www.halo.run
```

## Troubleshooting

- **Login fails with anonymous user**: Basic auth is likely disabled on the Halo server. Add `--halo.security.basic-auth.disabled=false` to Halo startup flags.
- **Credential issues**: Run `halo auth profile doctor` to diagnose keyring/config problems.
- **Profile not found**: Ensure `--profile` matches an existing profile from `halo auth profile list`.
