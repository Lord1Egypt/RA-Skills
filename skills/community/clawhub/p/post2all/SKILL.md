---
name: post2all
description: Create, validate, draft, schedule, publish, update, cancel, and manage platform-specific social posts across connected post2all accounts. Use when the user wants OpenClaw to publish to multiple social networks, adapt copy per platform, handle images or video, or maintain a review-first social workflow.
metadata:
  openclaw:
    requires:
      bins:
        - post2all
    install:
      - kind: node
        package: "@post2all/cli"
        bins:
          - post2all
    envVars:
      - name: POST2ALL_API_KEY
        required: false
        description: Optional post2all API key. The CLI can also use a key stored locally with `post2all config set-key`.
    emoji: "📣"
    homepage: https://www.post2all.com/openclaw
---

# post2all for OpenClaw

Use post2all as the publishing layer for OpenClaw social workflows.

OpenClaw can research, remember context, generate content, run routines, and decide what should happen next. post2all handles the handoff to the user's connected social accounts: account discovery, platform capabilities, validation, drafts, media uploads, scheduling, publishing, updates, cancellation, and supported deletion workflows.

Default to a **draft-first workflow**. Let the agent do the repetitive work, then let the user review and schedule or publish the content they approve.

For reusable examples, read `references/workflows.md`.
For authentication and connection guidance, read `references/setup.md`.
For publishing boundaries and approval rules, read `references/safety.md`.

## Before using post2all

A post2all account/workspace and at least one connected social account are required for real publishing. Available capabilities depend on the connected platforms, workspace permissions, and post2all plan.

Check that the CLI is available:

```bash
post2all --help
```

If it is not available, the ClawHub install metadata declares the Node package `@post2all/cli` and the `post2all` binary.

Before workspace operations, validate authentication:

```bash
post2all config whoami --json
```

Credentials can come from `POST2ALL_API_KEY` (preferred) or the local configuration. The user should store a key themselves with `post2all config set-key`, which prompts for the key or reads it from stdin so it stays out of shell history and the conversation:

```bash
post2all config set-key
```

Never print, repeat, log, or commit an API key. Do not ask the user to paste an API key into the conversation.

The hosted post2all MCP server is an alternative connection method for OpenClaw environments that support remote HTTP MCP with OAuth:

```text
https://mcp.post2all.com/mcp
```

For **embedded SaaS social-account onboarding**, use the public REST API or official SDK instead of MCP. A SaaS backend starts `POST /api/v1/accounts/connect/:platform`, sends the end user's browser to the returned provider authorization URL, and verifies the final `connectionId` from its backend after post2all redirects the browser back to the SaaS. The end user does not need a post2all account or post2all login. Keep the post2all API key server-side. Mastodon connections also take a `handle` (for example `you@mastodon.social` or `mastodon.social`) so OAuth runs on the user's own server. Instagram connections take an optional `connectionMethod` (`instagram_login` by default, or `facebook_login` to connect every eligible Instagram professional account behind the user's Facebook Pages, which is what unlocks Reel audio). See `https://www.post2all.com/docs/api-reference/account-connections`.

For production REST/SDK post creation, use a stable `Idempotency-Key`, retain response `X-Request-Id` values, and respect rate-limit metadata and `Retry-After`. Credit integrations can read billing and advisory publishing capacity through the public API/SDK. Credit workspace owners/admins create webhook endpoints and copy the one-time signing secret from the post2all dashboard; management is not a public REST, SDK, CLI, or MCP surface. Verify signed deliveries, deduplicate by event ID, and reconcile against current resources. See `https://www.post2all.com/docs/webhooks`.

## Profiles and organized work

Business, Agency, and manually onboarded credit workspaces can optionally organize clients, brands, or customers into Profiles. Business supports 2 profiles, Agency supports up to 10, and credit workspaces support up to 10,000; Creator does not include profile operations.

Discover profiles with `post2all profile list --json` or `profiles_list` when MCP is connected. Use the root `--profile-id <profileId>` option for profile-aware CLI account/post work, or pass optional `profileId` to MCP tools that expose it. REST/SDK code can use `client.forProfile(profileId)`, which sends `x-profile-id`. Treat this as an organization/filtering context rather than a separate security credential. Never invent a profile ID.

Use `post2all account profile <accountId> <profileId>` to assign an existing account, or `--clear` to remove its profile assignment. Moving an account does not move historical posts or break existing publishing/retry flows. Deleting a profile preserves its accounts and posts as profile-less resources. For embedded SaaS onboarding, REST/SDK can start a connection from a profile client so the connected account is organized under that profile; MCP still does not perform provider OAuth account connection/reconnection.

## Core publishing workflow

Follow this sequence for reliable publishing work:

1. Verify post2all access.
2. List connected accounts. Never guess account IDs or platform values.
3. Inspect the latest publishing schema/capabilities for all selected accounts.
4. Load account-specific publishing options only when the schema requires them, such as Pinterest boards, Discord channels, or TikTok creator restrictions.
5. Upload local media before creating the post and use the returned media IDs/objects.
6. Build one target per destination account and apply platform-specific copy/settings only where needed.
7. Validate before creating whenever the connected interface exposes validation.
8. Save a draft unless the user clearly asked to schedule or publish.
9. Before scheduling or immediate publishing, show the final destinations and material when meaningful and obtain the required user approval.
10. Report the post ID, delivery state, target accounts, and scheduled time.

Useful CLI commands:

```bash
post2all config whoami --json
post2all accounts --json
post2all constraints <accountId...> --json
post2all account publishing-options <accountId...> --json
```

Treat current publishing capabilities as authoritative. Platform rules change. Do not rely on memorized character limits, required fields, privacy values, board IDs, channel IDs, or creator restrictions.

## Account model

Every destination is its own target. Multiple accounts on the same platform must remain separate targets.

Example:

```json
{
  "platform": "threads",
  "accountId": "acc_threads_123",
  "settings": {
    "caption": "A shorter Threads version",
    "topicTag": "buildinpublic"
  }
}
```

Use shared content when the same message works everywhere. Use target-level captions/settings when a platform or account needs a different version.

## Delivery modes

Use one of three delivery modes.

Draft:

```json
{ "mode": "draft" }
```

Immediate:

```json
{ "mode": "now" }
```

Scheduled:

```json
{
  "mode": "scheduled",
  "scheduledAt": "2026-09-02T09:00:00+05:30"
}
```

CLI equivalents:

```text
--delivery draft
--delivery now
--delivery scheduled --scheduled-at <timestamp>
```

If no CLI delivery flag is provided, post2all creates a draft.

Always use a timezone-aware ISO 8601 timestamp with `Z` or an explicit UTC offset. Resolve phrases such as "tomorrow morning" using the user's timezone before scheduling.

## Create a draft

Drafts are the safest default for an autonomous OpenClaw loop:

```bash
post2all post create \
  --content "Draft copy for review" \
  --delivery draft \
  --json
```

A useful agent pattern is:

1. collect ideas during the day;
2. turn the useful ones into post2all drafts;
3. let the user review the draft queue once per day;
4. schedule only the approved posts.

## Schedule a post

Only schedule after the user has approved the content/destinations or has explicitly configured a trusted recurring workflow that permits scheduling.

```bash
post2all post create \
  --content "Scheduled update" \
  --targets '[{"platform":"linkedin","accountId":"acc_linkedin_123","settings":{}}]' \
  --delivery scheduled \
  --scheduled-at "2026-09-02T09:00:00+05:30" \
  --json
```

## Publish immediately

Immediate publication is a consequential external action. Use it only when the user clearly requests it and the final post is ready.

```bash
post2all post create \
  --content "New release shipping today 🚀" \
  --targets '[
    {
      "platform": "linkedin",
      "accountId": "acc_linkedin_123",
      "settings": {}
    },
    {
      "platform": "threads",
      "accountId": "acc_threads_123",
      "settings": {
        "caption": "Shorter Threads version"
      }
    }
  ]' \
  --delivery now \
  --json
```

## Media

Upload local media before post creation:

```bash
post2all media upload ./launch.png --json
```

Then use the returned media record:

```bash
post2all post create \
  --content "Launch day" \
  --media '[{"id":"media_123","altText":"Product dashboard showing the new launch workflow"}]' \
  --targets '[{"platform":"instagram","accountId":"acc_instagram_123","settings":{}}]' \
  --delivery draft \
  --json
```

Do not pass local filesystem paths directly to post creation.

Composition is inferred from the attached media. Check the current publishing schema before assuming an account supports text-only, images, video, mixed media, alt text, thumbnails, or other media features.

## Platform-specific settings

Do not invent platform settings. Discover the current schema/options first.

Examples of settings post2all may expose include:

- per-platform captions;
- YouTube title, description, tags, category, privacy, and thumbnail controls;
- Instagram thumbnails;
- Pinterest board, link, title, and AI disclosure controls;
- Threads topic tags;
- Mastodon visibility, content warning, and sensitive-media controls (character limits vary by server, so read them from the schema);
- Discord channels and auto-crosspost;
- Telegram link and notification controls;
- TikTok posting method, privacy, interaction, disclosure, and photo-music controls.

Dynamic values must come from the connected account's latest options. Never guess a Pinterest board ID, Discord channel ID, or TikTok privacy value.

## TikTok boundary

TikTok has additional creator and policy requirements.

Before scheduling or publishing TikTok content:

1. load fresh creator information/options;
2. show the selected creator identity;
3. review the media and caption/title;
4. require a creator-supported privacy choice for Direct Post;
5. review interaction and commercial-disclosure settings;
6. obtain the user's explicit consent to TikTok's required confirmations when applicable.

Do not silently choose privacy or disclosure values.

## Inspect and manage posts

```bash
post2all posts --status scheduled --limit 100 --json
post2all post get <postId> --json
```

Common statuses include:

- `draft`
- `scheduled`
- `publishing`
- `published`
- `completed`
- `partially_failed`
- `failed`

A `completed` post can include an upload-only destination that still requires the user to finish publication inside the platform app.

## Update a draft or scheduled post

Inspect the existing post first when there is any risk of replacing media or targets.

```bash
post2all post update <postId> \
  --content "Revised content" \
  --delivery draft \
  --json
```

Publish an approved existing draft:

```bash
post2all post update <postId> --delivery now --json
```

## Cancel a schedule

```bash
post2all post cancel <postId> --json
```

Cancellation preserves the post2all record while removing the pending schedule.

## Deletion

Deletion is destructive. Inspect the post and confirm the exact target before deleting anything.

For supported live social deletion, inspect the post and use the current `deletion.available` / `deletion.reason` state for the specific published target. Only offer live deletion when the server reports it as available.

```bash
post2all post delete-published <postId> \
  --post-account-id <postAccountId> \
  --json
```

Removing the post2all record is separate:

```bash
post2all post get <postId> --json
post2all post delete <postId> --json
```

Deleting the post2all record does **not** imply that already-published social content was removed from its platform.

## OpenClaw operating pattern

A strong unattended workflow keeps the boundary between the agent loop and publishing explicit:

- OpenClaw can continuously research, remember, generate, and refine.
- post2all stores the publishable artifacts as drafts/schedules.
- the user can review the queue periodically instead of reviewing every agent step.
- immediate publishing remains explicit unless the user has intentionally configured a trusted automation.

This gives the user most of the automation benefit while keeping the social publishing handoff auditable and reversible where possible.

## Errors and recovery

When a command fails, use the returned error rather than repeatedly retrying the same request.

Typical recovery:

- invalid/expired auth: reconfigure the local post2all key;
- invalid accounts: list accounts again and refresh IDs;
- invalid request: inspect the exact field path returned by post2all;
- missing media: upload again or use a valid retained media record;
- unsupported media/settings: refresh the current capabilities/options;
- rate limited: wait before retrying;
- plan/permission restriction: explain the restriction rather than looping.

Prefer `--json` for any command whose result will be parsed or used by the agent in a later step.
