---
name: ghst
description: Work with Ghost blogs using the ghst CLI tool. Supports full Ghost Admin API access including posts, pages, members, tags, newsletters, themes, stats, social web (ActivityPub), and more.
homepage: https://github.com/TryGhost/ghst
metadata:
  openclaw:
    emoji: "👻"
    homepage: "https://github.com/TryGhost/ghst"
    requires:
      bins: ["ghst"]
      env: ["GHOST_URL", "GHOST_STAFF_ACCESS_TOKEN"]
    primaryEnv: "GHOST_URL"
    install:
      - id: "ghst-npm"
        kind: "node"
        package: "@tryghost/ghst"
        bins: ["ghst"]
        label: "Install ghst (npm)"
      - id: "ghst-npx"
        kind: "node"
        command: "npx @tryghost/ghst"
        label: "Run via npx"
---

# `ghst` CLI Skill

This skill wraps the [ghst](https://github.com/TryGhost/ghst) CLI tool, which allows the agent to interact directly with any Ghost instance via the Ghost Admin API.

## Prerequisites & Installation

For this skill to function, the `ghst` binary must be available in the system's `$PATH`.

### Local Installation

Install the CLI globally from the official npm registry using npm:

```bash
npm install -g @tryghost/ghst
```

Alternatively, you can run it via `npx` without a permanent installation (though this is slower for repeated agent tasks):

```bash
npx @tryghost/ghst --help
```

> **Security**: Always install `@tryghost/ghst` from the official npm registry (`https://www.npmjs.com/package/@tryghost/ghst`). Consider pinning to a specific, reviewed version rather than relying on whatever version resolves at runtime (e.g., `npm install -g @tryghost/ghst@1.2.3`). Keep the package updated intentionally and review release notes before upgrading.

### Docker / Containerized Environments

If you are running OpenClaw in Docker, ensure the `ghst` binary is included in your container image by adding the installation command to your `Dockerfile`:

```dockerfile
RUN npm install -g @tryghost/ghst
```

## Configuration & Authentication

To interact with a Ghost instance, the agent requires a Ghost API URL and a Ghost Staff Access Token. There are two main ways to achieve this within the ghst skill:

1. **Explicit flags**: `--url` and `--staff-token`
2. **Environment variables**: `GHOST_URL` and `GHOST_STAFF_ACCESS_TOKEN`


### Staff Account & Token Security

To minimize risk, create a **dedicated Ghost staff account** specifically for agent access and grant it only the **least privileges** required (e.g., Author or Editor rather than Owner). Store the `GHOST_STAFF_ACCESS_TOKEN` securely—never commit it to version control or expose it in chat logs. If the token is ever leaked, rotate it immediately via the Ghost Admin panel, and disable or remove the token when the agent no longer needs access.

### Instructions for Bot Owners

1. Navigate to your Ghost Admin panel.
2. Go to **Settings** -> **Staff** (or **Users**) -> Edit your User Profile.
3. At the bottom, generate or copy a **Staff Access Token**.

**Option 1 — `~/.openclaw/.env` (recommended for personal use)**

Add the variables directly to your `~/.openclaw/.env` file:

```env
GHOST_URL="https://your-blog-url.ghost.io"
GHOST_STAFF_ACCESS_TOKEN="your-staff-access-token-id:secret"
```

**Option 2: `openclaw.json` skill entry (per-skill injection)**

In `~/.openclaw/openclaw.json`, add an `env` block under your skill's entry:

```json
{
  "skills": {
    "entries": {
      "ghst": {
        "enabled": true,
        "env": {
          "GHOST_URL": "https://your-blog-url.ghost.io",
          "GHOST_STAFF_ACCESS_TOKEN": "your-staff-access-token-id:secret"
        }
      }
    }
  }
}
```

Once configured, restart your agent or wait for the config to be picked up.

### Advanced Environment Variables

For complex setups, the following environment variables are supported:

| Variable | Description |
| :--- | :--- |
| `GHOST_URL` | Canonical URL of the Ghost instance. |
| `GHOST_STAFF_ACCESS_TOKEN` | `{id}:{secret}` for Admin API access. |
| `GHOST_CONTENT_API_KEY` | Hex key for Content API access (via `ghst api --content-api`). |
| `GHOST_API_VERSION` | Target API version (e.g., `v5.0`). Defaults to latest. |
| `GHOST_SITE` | Default site alias/profile to use. |
| `GHST_CONFIG_DIR` | Custom path for CLI configuration. |
| `GHST_OUTPUT` | Set to `json` to force JSON output globally. |
| `NO_COLOR` | Disable ANSI color sequences. |


## Agent Guidelines & Usage

When operating the `ghst` skill, the agent must adhere to the following rules to ensure robust and safe usage.

### 1. Robust Scripting

- **Always use `--json` or `--jq`**: Ensure your commands produce machine-readable JSON output rather than human-readable text.
  ```bash
  ghst post list --json
  ghst post list --json --jq '.posts[].title'
  ```
- **Use `--non-interactive`**: Since you are running in an automated environment, never issue commands that prompt for user input unexpectedly. Use `--yes` in combination with `--non-interactive` for any required destructive operations that you have received user approval for.
  ```bash
  ghst comment delete <comment-id> --yes --non-interactive
  ```
- **Non-Interactive Auth**: If you need to authenticate a new site programmatically:
  ```bash
  ghst auth login --non-interactive --url "https://blog.com" --staff-token "..."
  ```

### 2. Editing Posts and Pages

For detailed instructions on the "Read-Edit-Write" workflow to edit post or page lexical content (including minor rewording and URL changes), see the [`editing.md`](references/editing.md) reference.

### 3. Searching and Filtering Posts and Pages

When you need to find specific posts or pages (e.g., by title, status, or tag), refer to the advanced filtering and NQL query examples documented in [`post.md`](references/post.md) and [`page.md`](references/page.md).

### Command Reference

Detailed documentation for each resource can be found in the `references/` directory:

| Resource | Description |
| :--- | :--- |
| [`ghst post`](references/post.md) | Publish, schedule, and manage posts. |
| [`ghst page`](references/page.md) | Manage pages and static content. |
| [`ghst tag`](references/tag.md) | Create and manage site tags. |
| [`ghst member`](references/member.md) | Manage members, imports, exports, and bulk operations. |
| [`ghst socialweb`](references/socialweb.md) | ActivityPub feeds, profile management, and social interactions. |
| [`ghst comment`](references/comment.md) | Moderate, hide, show, and delete comments. |
| [`ghst newsletter`](references/newsletter.md) | Create and manage newsletters and bulk settings. |
| [`ghst tier`](references/tier.md) | Manage membership tiers. |
| [`ghst offer`](references/offer.md) | Create and manage subscription offers. |
| [`ghst stats`](references/stats.md) | Site analytics, growth reporting, and post traffic. |
| [`ghst setting`](references/setting.md) | Retrieve and update site-level settings. |
| [`ghst image`](references/image.md) | Upload media assets to Ghost. |
| [`ghst theme`](references/theme.md) | Upload, activate, and validate site themes. |
| [`ghst label`](references/label.md) | Label management for members and content. |
| [`ghst user`](references/user.md) | Manage staff users and retrieve profile info. |
| [`ghst site`](references/site.md) | General site information. |
| [`ghst webhook`](references/webhook.md) | Configure and listen for Ghost webhooks. |
| [`ghst migrate`](references/migrate.md) | Import tools for WordPress, Medium, Substack, and CSV. |
| [`ghst auth`](references/auth.md) | CLI authentication, site switching, and token management. |
| [`ghst config`](references/config.md) | CLI tool configuration and defaults. |
| [`ghst api`](references/api.md) | Direct raw API explorer for Admin and Content APIs. |


**Example Workflows:**

*   **Bulk Post Tagging**: `ghst post bulk --filter "status:draft" --update --add-tag "Release"`
*   **Member Cleanup**: `ghst member bulk --filter "status:free" --action delete --yes --non-interactive`
*   **Analytics Export**: `ghst stats posts --range 30d --csv --output ./report.csv`
*   **Social Interaction**: `ghst socialweb note --content "Hello from the CLI"`


### 4. Safe Operation & Protections

- **Approvals & Notices**: You must obtain **explicit user confirmation** before performing any of the following actions:
    - Publishing, scheduling, or unpublishing posts/pages
    - Deleting posts, pages, members, comments, labels, themes, or any resource
    - Bulk updates or bulk deletes (`ghst ... bulk ...`)
    - Changing site settings (`ghst setting set`)
    - Creating, updating, or deleting webhooks (`ghst webhook`)
    - Importing or exporting data (`ghst migrate`, `ghst member export`)
    - Raw API calls (`ghst api`)

    **Note**: The CLI emits `GHST_AGENT_NOTICE:` lines on `stderr` when a manual confirmation is interrupted. If you see this, you **must** stop and ask the user for explicit approval.

- **Prefer Listing / Fetching First**: Before performing any destructive or mutating action, prefer to list or fetch the target resource to verify its identity. Always use **exact IDs** or **exact slugs** rather than fuzzy matching or assumptions.

- **Destructive Commands**: Only use `--yes --non-interactive` for the following once the user has explicitly approved:
    - `ghst member bulk --action delete`
    - `ghst label bulk --action delete`
    - `ghst socialweb delete`
    - `ghst auth logout`
    - `ghst auth link` (when replacing active link)
- **File Safety**: CLI tools like `member export` and `migrate export` will refuse to overwrite existing files. Check for file existence before exporting if necessary.
- **Security Check**: Never print or output sensitive tokens (e.g., values coming from `ghst auth token` or `config --show-secrets`) into the chat unprompted. Treat them as privileged credentials.


