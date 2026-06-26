# Massblogger Skill

Manage WordPress sites, generate AI content, run research pipelines, and operate a full content portfolio through a single hosted MCP server — no local install required.

---

## Overview

- **What it does:** Connects OpenClaw to the Massblogger MCP server, giving the agent full read/write access to WordPress (posts, pages, categories, tags, media, menus, users, settings, comments, plugins, themes, revisions, scheduling) plus Massblogger's native content generation, pSEO, automation, and media pipelines.
- **When to use it:** When you want an AI agent to manage one or more WordPress sites — writing, editing, publishing, restructuring, bulk operations, cross-site changes — without you copying HTML or switching tabs.
- **Requirements:** A Massblogger account at massblogger.com, at least one WordPress site connected in Massblogger (with Application Password stored), and an MCP token generated from Massblogger settings.

---

## Quick start

### Install

Add to your OpenClaw config (`~/.openclaw/openclaw.json`):

```json
{
  "mcpServers": {
    "massblogger": {
      "url": "https://massblogger.com/api/mcp",
      "transport": "http"
    }
  }
}
```

Or using the OpenClaw CLI:

```bash
openclaw config set mcpServers.massblogger.url "https://massblogger.com/api/mcp"
openclaw config set mcpServers.massblogger.transport "http"
```

### Configure

Add your Massblogger MCP token in the **OpenClaw runtime environment** (Control UI env editor if available, process env, or `~/.openclaw/.env`):

```bash
# Required — set in OpenClaw runtime environment:
#   MASSBLOGGER_MCP_TOKEN  — your Massblogger MCP Bearer token
#
# Generate your token at: https://massblogger.com/dashboard/settings
# Settings → Agentic SEO → Hosted MCP access → Generate token
#
# The token is scoped to your account only. Each user gets their own token.
```

Once your token is in the OpenClaw environment, update the config to pass it as a header:

```json
{
  "mcpServers": {
    "massblogger": {
      "url": "https://massblogger.com/api/mcp",
      "transport": "http",
      "headers": {
        "Authorization": "Bearer $MASSBLOGGER_MCP_TOKEN"
      }
    }
  }
}
```

If your version of OpenClaw does not support header interpolation, use the fallback token header instead:

```bash
openclaw config set mcpServers.massblogger.url "https://massblogger.com/api/mcp"
openclaw config set mcpServers.massblogger.env.x-massblogger-mcp-token "$MASSBLOGGER_MCP_TOKEN"
```

### Verify

In OpenClaw, ask:

```text
List my Massblogger websites
```

You should see a list of your connected sites with their delivery type (WordPress, webhook, or API). If the list is empty, confirm your Application Password is stored in Massblogger under the website settings.

---

## Environment variable contract

| Variable | Purpose | Required | Where to set |
|---|---|---|---|
| `MASSBLOGGER_MCP_TOKEN` | Bearer token for MCP authentication | Yes | OpenClaw runtime environment |

The MCP token is the only credential required on the agent side. WordPress Application Passwords are stored inside Massblogger (not passed by the agent) and used server-side when making WordPress REST API calls on your behalf.

---

## Core tasks

```text
List all my WordPress sites and tell me which ones have posts scheduled for this week
```

```text
Write a 1500-word article about the best lightweight camping stoves for myblog.com, publish it as a draft, generate a featured image, and set the Yoast meta description
```

```text
List the last 20 published posts on myblog.com that are missing a Yoast meta description, then write and set one for each
```

```text
We rebranded from GearLife to TrailPro — run a search and replace across all my sites and show me a dry run first
```

```text
Clone post 142 from myblog.com to gearblog.com and hikingblog.com as drafts, matching categories by name
```

```text
Enable publish guard on myblog.com so the agent can only save drafts, not publish directly
```

```text
Restore the last revision of post 88 on myblog.com — something broke after the last update
```

---

## Configuration

### WordPress Application Password

The Massblogger MCP server authenticates to WordPress on your behalf using a stored Application Password. To connect a WordPress site:

1. In WordPress admin go to **Users → Profile → Application Passwords**
2. Enter a name (e.g. "Massblogger") and click **Add New Application Password**
3. Copy the generated password
4. In Massblogger go to the website settings and paste the password, your WordPress username, and your WordPress URL

The Application Password user must have **Editor** or **Administrator** role for full tool access. Author-level credentials work for creating and editing their own posts only — they cannot restore trashed content, manage plugins, or edit other users' posts.

### Token management

Your MCP token is shown once in Massblogger settings. If you lose it:

1. Go to **Massblogger → Settings → Agentic SEO → Hosted MCP access**
2. Click **Revoke** to invalidate the old token
3. Click **Generate** to create a new one
4. Update `MASSBLOGGER_MCP_TOKEN` in your OpenClaw runtime environment

### Publish guard (optional safety flag)

Publish guard is a per-website server-side flag that blocks the agent from publishing content directly. When enabled, any tool call with `status: publish` is silently redirected to `status: draft`:

```text
Enable publish guard on myblog.com
```

```text
Disable publish guard on myblog.com
```

```text
Is publish guard enabled on myblog.com?
```

This setting survives across sessions and cannot be bypassed by the agent.

---

## Full tool catalog

### WordPress — Posts

- `list_wordpress_posts` — list posts with search, status, category, tag, and page filters
- `get_wordpress_post` — fetch full raw HTML content and all metadata for a single post
- `create_post` — create a post; supply only the fields you need
- `update_post` — update any subset of a post's fields; no full body required
- `delete_wordpress_post` — move to trash or permanently delete with `force: true`
- `restore_wordpress_post` — restore a trashed post back to draft or publish

### WordPress — Pages

- `list_wordpress_pages`, `get_wordpress_page`, `create_wordpress_page`, `update_wordpress_page`, `delete_wordpress_page`, `restore_wordpress_page`

### WordPress — Categories & Tags

- `list_wordpress_categories`, `create_wordpress_category`, `update_wordpress_category`, `delete_wordpress_category`
- `list_wordpress_tags`, `create_wordpress_tag`, `update_wordpress_tag`, `delete_wordpress_tag`

### WordPress — Media

- `list_wordpress_media`, `upload_wordpress_media`, `update_wordpress_media`, `delete_wordpress_media`
- `set_wordpress_featured_image` — set or clear featured image on any post or page
- `insert_image_into_post` — insert an image at beginning, end, after intro, or before conclusion without replacing the full body
- `search_replace_post_content` — find and replace text inside any post or page

### WordPress — Revisions

- `list_post_revisions` — see full revision history with dates and content previews
- `restore_post_revision` — roll back a post or page to any saved revision

### WordPress — Scheduling

- `list_scheduled_posts` — see all future-scheduled posts ordered by date
- `reschedule_post` — change a post's scheduled publish date

### WordPress — Menus

- `list_wordpress_menus`, `get_wordpress_menu`, `create_wordpress_menu`
- `add_wordpress_menu_item`, `update_wordpress_menu_item`, `delete_wordpress_menu_item`

### WordPress — Users

- `list_wordpress_users`, `get_wordpress_user`, `create_wordpress_user`, `update_wordpress_user`, `delete_wordpress_user`

### WordPress — Comments

- `list_wordpress_comments`, `update_wordpress_comment`, `delete_wordpress_comment`
- `bulk_moderate_comments` — approve/hold/spam/trash multiple comments in one call
- `delete_all_spam_comments` — clear all spam site-wide or per post; supports `dryRun: true`

### WordPress — Settings, Plugins & Theme

- `get_wordpress_settings`, `update_wordpress_settings`
- `list_wordpress_plugins`, `activate_wordpress_plugin`, `deactivate_wordpress_plugin`
- `get_wordpress_theme`

### WordPress — SEO

- `update_wordpress_seo` — set Yoast SEO title and meta description (requires Yoast plugin)

### Massblogger — AI Images

- `generate_image_for_website` — generate an AI image using DALL-E, stored in Massblogger media library
- `generate_and_set_featured_image` — generate, upload to WordPress, and set as featured image in one call
- `list_massblogger_media` — browse the Massblogger media library
- `use_massblogger_media_in_wordpress` — upload a Massblogger media item to a WordPress site

### Massblogger — Content & Research

- `list_websites`, `get_site_context`, `research_topics`, `list_saved_topics`
- `generate_post_from_saved_topic`, `create_massblogger_post`, `run_automation_for_website`
- `get_activity_logs`

### Massblogger — pSEO

- `list_pseo_campaigns`, `list_pseo_pages`, `create_pseo_campaign`, `update_pseo_page`

### Cross-site operations

- `search_replace_across_sites` — find/replace across multiple WordPress sites; supports `dryRun: true`
- `clone_post_to_sites` — copy a post to multiple target sites with category matching and featured image transfer
- `bulk_update_post_status` — change the status of multiple posts in one call

### MCP Safety

- `get_publish_guard`, `set_publish_guard`

---

## Security & Guardrails

### Permissions and scopes

The Massblogger MCP server only exposes data owned by the authenticated user. Each MCP token is scoped to a single Massblogger account — the server rejects requests for websites or data belonging to any other user, even if the token is valid.

WordPress operations use a stored Application Password, not your main WordPress account password. Application Passwords can be revoked independently from your WordPress account.

For write-sensitive operations (plugin activation, user deletion, bulk status changes), the WordPress user associated with the Application Password must hold **Editor** or **Administrator** role. Operations that exceed the stored credential's capability return a WordPress-level authorization error — not a silent failure.

### Secrets handling

- Your MCP token authenticates to the Massblogger server only. It is never forwarded to WordPress or any third-party service.
- WordPress Application Passwords are stored in Massblogger and used server-side. They are never returned to the agent or included in tool call responses.
- Never paste your MCP token or Application Password into a chat prompt. Set them in the OpenClaw runtime environment (Control UI env editor, process env, or `~/.openclaw/.env`).
- If a token is compromised: revoke it immediately in Massblogger settings (Settings → Agentic SEO → Hosted MCP access → Revoke) and generate a replacement.
- If an Application Password is compromised: revoke it in WordPress admin under Users → Profile → Application Passwords and update the stored value in Massblogger website settings.

### Confirmation before risky actions

Operations that are irreversible or affect multiple items are designed to require deliberate intent:

- **Permanent delete** (`delete_wordpress_post`, `delete_wordpress_page`, `delete_wordpress_media`): requires explicitly passing `force: true` — omitting this moves content to trash instead.
- **Cross-site search/replace** (`search_replace_across_sites`): supports `dryRun: true` to preview all changes before committing.
- **User deletion** (`delete_wordpress_user`): requires either `reassignTo` (user ID to receive the deleted user's posts) or `deleteContent: true` — the tool errors if neither is provided.
- **Spam deletion** (`delete_all_spam_comments`): supports `dryRun: true` to count affected comments before deleting.
- **Publish guard** (`set_publish_guard`): persists server-side and cannot be bypassed by the agent once set.

### Data minimization

List and summary tools return only the fields needed for the next action — ID, title, slug, status, date, and key IDs. Full content is returned only when explicitly requested via `get_wordpress_post` or `get_wordpress_page`. Activity logs include tool name and summary only — full post content is never stored in logs.

### Network access

All network calls originate from the Massblogger server, not from the agent's machine. The agent sends tool arguments to `https://massblogger.com/api/mcp`; the server makes WordPress REST API calls to your site on your behalf.

AI image generation calls go from the Massblogger server to the OpenAI Images API using your Massblogger-managed OpenAI key. Generated images are stored in Google Cloud Storage under your Massblogger account and returned as public HTTPS URLs.

### Local storage

This skill uses a remote MCP server — no local files are written by the MCP server itself. Your MCP token lives wherever you place it in the OpenClaw runtime environment. No WordPress credentials, session tokens, or content is written to local disk.

### Revoke and rotate

| Credential | How to revoke | How to rotate |
|---|---|---|
| Massblogger MCP token | Massblogger → Settings → Agentic SEO → Hosted MCP access → Revoke | Generate a new token on the same page, update `MASSBLOGGER_MCP_TOKEN` in OpenClaw env |
| WordPress Application Password | WordPress admin → Users → Profile → Application Passwords → Revoke | Generate a new Application Password, update in Massblogger website settings |

---

## Troubleshooting

**"Unauthorized" when calling restore, plugin, or user management tools**

The WordPress Application Password belongs to a user with insufficient role. These tools require **Editor** or **Administrator**. In WordPress admin, check the role of the user whose Application Password is stored, or generate a new Application Password from an Administrator account and update it in Massblogger.

**"WordPress credentials are missing for this website"**

The website record in Massblogger is missing `wpUrl`, `wpUsername`, or `wpAppPassword`. Go to the Massblogger website settings for that site and fill in all three fields.

**"Website not found"**

The `website` argument doesn't match any site in your account. Use `list_websites` first to see exact domain names and IDs, then pass one of those values.

**Tool call times out on `generate_post_from_saved_topic` or `research_topics`**

These tools run the full Massblogger generation pipeline and can take up to 5 minutes for long-form content. If your MCP client times out before that, increase the client-side timeout or use `create_massblogger_post` with pre-written content instead.

**`publishGuardApplied: true` in the response**

This is informational, not an error. It means publish guard is on for that site and the post was saved as draft instead of published. Use `set_publish_guard` with `enabled: false` to allow direct publishing, or manually publish the draft in WordPress admin.

**Menu tools return "No menus returned" or fail**

Menu write tools require the **WP REST API Menus** plugin or WordPress 6.x with Full Site Editing enabled. Install the plugin from the WordPress plugin directory and retry.

---

## Release notes

### 1.0.0

- Full WordPress CRUD: posts, pages, categories, tags, media, users, settings, comments, menus, plugins, themes (75 tools total)
- Post and page revision history with one-call rollback
- AI image generation via DALL-E integrated with WordPress featured image pipeline
- Cross-site search/replace and post cloning
- Publish guard safety flag (per-website, server-side)
- Bulk comment moderation and spam clearing
- Scheduling management (list scheduled, reschedule)

---

## Links

- **Massblogger:** https://massblogger.com
- **MCP setup docs:** https://massblogger.com/docs/openclaw
- **WordPress Application Passwords guide:** https://massblogger.com/docs/wordpress/application-passwords

---

## Publisher

* **Publisher:** @massblogger
