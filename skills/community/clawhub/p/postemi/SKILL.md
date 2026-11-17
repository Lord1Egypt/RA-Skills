---
name: postemi
description: Postemi schedules and publishes social posts from the command line to 37 platforms and apps, including Facebook, Instagram, X, LinkedIn, TikTok, YouTube, Threads, Bluesky, Pinterest and Mastodon.
homepage: https://postemi.com
metadata: {"openclaw":{"emoji":"🌎","requires":{"bins":[],"env":[]}}}
---

## Install

The npm package and the command are both **`postemi`**.

```bash
npm install -g postemi
postemi auth:login        # opens the browser to approve the login
```

official website: https://postemi.com
API base: https://api.postemi.com
MCP server, for chat clients without a terminal: https://mcp.postemi.com/mcp
(the user signs in to Postemi in the browser; same account, same channels)

---

| Property | Value |
|----------|-------|
| **name** | postemi |
| **description** | CLI for scheduling and publishing posts through the Postemi public API |
| **allowed-tools** | Bash(postemi:*) |

---

## Which channels you can publish to

**Only these. Do not offer a user anything else, and do not try to post to it.**
Postemi's server carries inherited code for many more providers; that code is not
enabled and not supported. Postemi adds channels over time, so
`integrations:list` (below) can show one that is not in this table yet.

| Channel | `identifier` | Status |
|---|---|---|
| X (Twitter) | `x` | Live |
| Facebook (Pages) | `facebook` | Live |
| Instagram (business account through a Facebook Page) | `instagram` | Live |
| Instagram (professional account, no Facebook Page) | `instagram-standalone` | Live |
| LinkedIn (member feed) | `linkedin` | Live |
| TikTok | `tiktok` | Live |
| YouTube | `youtube` | Live |
| Threads | `threads` | Live |
| Bluesky | `bluesky` | Live |
| Pinterest | `pinterest` | Live (a pin needs a `board` id) |
| Telegram | `telegram` | Live |
| Discord | `discord` | Live |
| Slack | `slack` | Live |
| Mastodon (mastodon.social) | `mastodon` | BETA |
| Mastodon (any other server) | `mastodon-custom` | BETA |
| Pixelfed (any server) | `pixelfed` | BETA |
| Tumblr | `tumblr` | BETA |
| WordPress (your own site) | `wordpress` | BETA |
| Ghost (your own site) | `ghost` | BETA |
| Dev.to | `devto` | BETA |
| Hashnode | `hashnode` | BETA |
| Webflow (CMS collection) | `webflow` | BETA |
| Shopify (blog) | `shopify` | BETA |
| Google Chat (a space, by webhook) | `google-chat` | BETA |
| Microsoft Teams (a channel, by webhook) | `microsoft-teams` | BETA |
| Lemmy (a community) | `lemmy` | BETA |
| Nostr | `nostr` | BETA |
| Dribbble | `dribbble` | BETA |
| Twitch (chat) | `twitch` | BETA |
| Kick (chat) | `kick` | BETA |
| Whop (forum) | `whop` | BETA |
| Circle (community) | `circle` | BETA |
| listmonk (newsletter) | `listmonk` | BETA |
| MailerLite (newsletter) | `mailerlite` | BETA |
| MailCheap (newsletter) | `mailcheap` | BETA |
| Mailchimp (newsletter) | `mailchimp` | BETA |
| Kit (newsletter) | `kit` | BETA |
| Brevo (newsletter) | `brevo` | BETA |
| Buttondown (newsletter) | `buttondown` | BETA |
| Google Business Profile | `gmb` | Coming soon, not schedulable yet |
| LinkedIn Pages (company pages) | `linkedin-page` | Coming soon, not schedulable yet |
| Snapchat | `snapchat` | Coming soon, not schedulable yet |

**Pinterest is live.** A pin needs a `board` id in `--settings`; look it up first
(see PROVIDER_SETTINGS.md).

**The BETA channels** connect and publish, but Postemi has not tried them with
many real accounts yet. Say so when the user picks one. Many need settings (a
title for WordPress, Dev.to, Ghost and Hashnode; a picture for Pixelfed; a
community for Lemmy; a list or audience for the newsletters); check
`integrations:settings` and PROVIDER_SETTINGS.md.

**Google Business Profile, LinkedIn Pages and Snapchat are coming soon.** Those
platforms have not approved Postemi yet, so the user cannot connect them. Do not
schedule for them; personal LinkedIn profiles (`linkedin`) work today.

**`integrations:list` is the truth.** The table says what Postemi supports; that
command says what THIS user has actually connected. Check it before you
schedule anything, and never post to an id that is not in its output.

**Never assume another provider exists.** If a user asks for Reddit, Medium,
Farcaster, VK or anything else that is not in the table, the answer is that Postemi does not offer it today.
Do not build a `--settings` payload for it.

---

## ⚠️ Two Hard Rules (Read First)

**Rule 1: Authenticate before anything.** All commands fail without valid credentials.

**Rule 2: Every file passed to `-m` (or to `image`/media fields in JSON mode) MUST first go through `postemi upload`.** Raw filesystem paths (`image.jpg`, `video.mp4`) and external URLs (`https://example.com/...`) are **NOT** accepted by the publishing pipeline. TikTok, Instagram, YouTube, and most other providers reject anything that isn't a Postemi-verified URL. Always:

```bash
RESULT=$(postemi upload <file>)
URL=$(echo "$RESULT" | jq -r '.path')
postemi posts:create ... -m "$URL" ...
```

If you see `-m "something.jpg"` anywhere below, treat it as shorthand for "the `.path` you got back from `postemi upload something.jpg`", never a raw local file.

---

## Output contract

Every command prints its **JSON result, and nothing else, to stdout**;
status lines, warnings and errors go to stderr, and every failure exits 1. So
`postemi upload x.jpg | jq -r '.path'` is always safe, with no stripping needed.
Unknown flags are an error, not silently ignored. If a flag is rejected, it
does not exist; do not retry with variations.

---

## ⚠️ Authentication Required

**You MUST authenticate before running any Postemi CLI command.** All commands will fail without valid credentials.

Before doing anything else, check auth status:
```bash
postemi auth:status
```

If not authenticated:
1. **Sign in:** `postemi auth:login` opens a browser, and the human approves it.
   You never see or handle a key.
2. **No account yet:** `postemi auth:signup` creates one, see below. Only when
   the user asks you to create a Postemi account for them. They can also sign
   up at https://postemi.com/app/signup, which starts a 7-day free trial, and
   then run `postemi auth:login`.

### Creating an account for the user (no free trial)

When the user asks you to make them a Postemi account and they have none:

```bash
postemi auth:signup --email anna@example.com
# → {codeSent:true, terms, privacy, timezone, language, next}   (no terminal: the code is on its way; `next` is the exact second command, every option kept)
postemi auth:signup --email anna@example.com --code 123456 --accept-terms [--workspace-name "Anna's Cafe"] [--timezone Europe/London]
# → {created:true, workspaceId, workspaceName, trial:false, credentials, next}
```

1. Run it with `--email` only. Postemi e-mails the user a six-digit code
   (valid 10 minutes). Ask the user to read the code to you.
2. Show the user the terms (https://postemi.com/terms) and the privacy notice
   (https://postemi.com/privacy) and ask whether they agree. Pass
   `--accept-terms` ONLY after they said yes; never decide it for them.
3. Run it again with `--code` and `--accept-terms`. The CLI keeps the
   sign-in the same way `auth:login` does and never prints it.
4. **There is no free trial on an account made this way**, and until the
   user pays, only the `billing:*` commands work. Next: `billing:plans`,
   confirm a plan with the user, `billing:subscribe`, give them the link.
   Channels are connected by the user in the web app after paying.
5. **You keep working for the user only on a plan with API access**
   (`limits.apiAndMcpAccess: true` in `billing:plans`). Basic has none: if
   the user picks it, tell them BEFORE they pay that you will not be able to
   schedule for them afterwards. `billing:subscribe` answers with
   `apiAndMcpAccess: false` and prints the warning on stderr for such a plan.

Exit 1 with "already has a Postemi account" (HTTP 409) means the address is
taken: the user signs in with `postemi auth:login` instead. A wrong or expired
code: run step 1 again for a new one.

`postemi auth:status` reports a valid key of a workspace that has not paid yet
as `authenticated: true, apiAccess: false, reason: "no-plan"` (exit 0). It is
not an invalid key; do not run `auth:login` for it. Only the `billing:*`
commands work until the workspace is on a plan with API access.

**Do NOT proceed with any other commands until authentication is confirmed.**

### What a key can and cannot do

Keys are **per person, named, and scoped**. They are stored hashed and shown
exactly once, at creation, in the web app under **Settings → Developers**. A
lost key cannot be recovered. It can only be rotated.

Two limits apply to every request, and both explain 403s that look like bugs:

1. **Scopes.** A key carries a subset of `posts:read`, `posts:draft`,
   `posts:publish`, `channels:read`, `channels:write`, `media:write`,
   `analytics:read`. A route refuses a key that lacks its scope.
2. **The owner's current role, re-checked on every request.** A key can never
   do more than the person who created it can do *right now*. If that person is
   demoted, their live keys narrow on the next request, with nobody revoking
   anything. So a key that worked yesterday can legitimately start returning
   403 today with no change to the key.

A key can also be **granted only some workspaces and only some channels**. A
request naming a channel outside the grant is refused even when the scope is
right.

**When you hit a 403, read the message.** The CLI names the missing scope; the key is valid, so `auth:login` does not fix it. Do not
retry, and do not try a different route to get around it. Ask the user to mint
a key with the scope, or to have someone with the right role do it.

---

## Core Workflow

The fundamental pattern for using Postemi CLI:

1. **Authenticate** - Verify or set up authentication (see above)
2. **Workspace** - `postemi workspaces:list`; if more than one and none is `current`, ask the user which, then `postemi workspaces:use <id>`. Channel ids belong to a workspace.
3. **Discover** - List integrations and get their settings
4. **Fetch** - Use integration tools to retrieve dynamic data (Instagram `audioSearch`; Discord and Slack `channels`)
5. **Prepare** - Upload media files if needed
6. **Post** - Create posts with content, media, and platform-specific settings
7. **Analyze** - Track performance with platform and post-level analytics
8. **Resolve** - If analytics returns `{"missing": true}`, run `posts:missing` to list provider content, then `posts:connect` to link it

```bash
# 1. Authenticate
postemi auth:status
# If not authenticated: postemi auth:login   (no client id/secret, it is a device flow)

# 2. Discover
postemi integrations:list
postemi integrations:settings <integration-id>

# 3. Fetch (if needed)
postemi integrations:trigger <integration-id> <method> -d '{"key":"value"}'

# 4. Prepare
postemi upload image.jpg
#    or, when the file is on the person's phone / not on this machine:
postemi upload:link            # show the url to the person, they drop the files
postemi upload:files <id>      # what arrived; use each .path in -m

# 5. Post
postemi posts:create -c "Content" -m "image.jpg" -i "<integration-id>"

# 6. Analyze
postemi analytics:platform <integration-id> -d 30
postemi analytics:post <post-id> -d 7

# 7. Resolve (if analytics returns {"missing": true})
postemi posts:missing <post-id>
postemi posts:connect <post-id> --release-id "<content-id>"
```

---

## Essential Commands

### Workspaces

A credential may reach several workspaces (the user ticked "All my
workspaces" at login, or made a multi-workspace key). The API refuses every
request from such a key that does not name one, with 403 and the message
"This API key spans several workspaces", so check first:

```bash
postemi workspaces:list            # [{id, name, role, current}]
postemi workspaces:use <id>        # persists; every later command acts there
postemi workspaces:current
postemi integrations:list --workspace <id>   # one command elsewhere, without switching
```

Say the workspace name back to the user when they have more than one, and
never pick one for them. After a switch, run `integrations:list` again:
channel ids from the other workspace are invalid here.

### Authentication

**Sign in: device login**
```bash
# Opens a browser. No client ID or secret, the human approves the code shown.
postemi auth:login

# Check auth status (verifies credentials are still valid)
postemi auth:status

# Logout (remove stored credentials)
postemi auth:logout
```

How it works, so you can explain it if the user asks: the CLI calls
`POST /device/code`, prints a short user code and opens the approval page in
the browser, then polls `POST /device/token` until the human (signed in to
Postemi) approves it and chooses which workspace and which channels the
resulting key may reach. This runs inside Postemi's own backend; there is no
separate auth service.

The CLI keeps its own sign-in after that; do not read, print or copy it.

Off a terminal (when you, an agent, run it) the CLI does not ask for a
timezone: pass `--timezone` on date-taking commands, or run
`postemi config:set timezone Europe/London` once. See "Date Handling".

The CLI talks to `https://api.postemi.com`. The MCP server, for chat clients,
is `https://mcp.postemi.com/mcp`. Other hostnames you may have read about do
not exist.

### Upload link: when the file is not on this machine

`postemi upload` needs the file on disk. When the person has it on their phone,
or you cannot see their filesystem, do NOT ask them to host it somewhere
public. Mint a link:

```bash
postemi upload:link
# → {"id":"kR3mQ7xP2nLa","url":"https://…","expiresAt":"…"}
```

Show the `url` to the person verbatim and say: open it, drop the image or
video, come back and tell me it is done. It works signed out and on a phone.
When they say done:

```bash
postemi upload:files kR3mQ7xP2nLa
# → {"status":"ready","count":1,"files":[{"id":"…","name":"clip.mp4","path":"https://…","type":"video"}]}
```

Pass each `path` to `posts:create -m`. `status: "empty"` is not an error: they
have not finished, or spoke before the last file landed. Ask them to check the
page says "uploaded" and run it again. The link lives two hours; mint a new one
if it expires.

### Subscription (only when the user asks)

Four commands, the only place a plan is named. Call them only when the user
asks about plans, asks to subscribe, or asks to manage their subscription;
never suggest a plan or an upgrade otherwise.

```bash
postemi billing:plans                                  # → {current:{tier,plan}, plans:[{plan,slug,monthly,yearly,limits}], trial, trialDays}
postemi billing:subscribe --tier pro --period yearly   # → {status:"requires_payment", checkoutUrl, checkoutId, plan, amount, currency, trial, expiresAt, apiAndMcpAccess}
postemi billing:status                                 # → {state, plan, period, currentPeriodEnd, payerIsCaller, pendingCheckout, apiAndMcpAccess}
postemi billing:manage                                 # → {portalUrl}
```

The flow:

1. Confirm the plan (Basic, Pro, Creator or Team; `--tier basic`, `pro`,
   `creator` or `team`, or the `slug` that `billing:plans` prints) and the
   period (monthly or yearly) with the user. Basic has no API access: if the
   user picks it, tell them BEFORE they pay that you will not be able to
   schedule for them afterwards.
2. Run `billing:subscribe` once and give the user `checkoutUrl`. **The user
   opens it and pays with their OWN Link wallet or card.** Do NOT pay with a
   one-time or agent-issued card, a virtual card number or any credential of
   your own: a Postemi subscription renews monthly or yearly, and a one-time
   credential fails at the first renewal, which ends the plan. `--open` opens
   the link in the browser of this machine; use it only when this machine is
   the user's own.
3. After the user says they have paid, run `billing:status` and check that
   `state` is `trialing` or `active` before continuing setup. It changes
   within seconds of the payment. If `billing:status` shows a
   `pendingCheckout`, hand that link back instead of running
   `billing:subscribe` again.
4. A live subscription is changed, cancelled or invoiced in the Stripe
   portal: `billing:manage` prints the link. Do not describe plans there.

These commands work before the workspace has a plan with API access (they
are how it gets one). `billing:subscribe` and `billing:manage` need a
full-workspace key or an OAuth token held by the person who pays (or a
workspace owner when nobody pays yet); a scoped key is refused with a
message that says so.

### Rate limits

Tiered, **per key, per route, per hour**. Each route keeps its own bucket, so a
polling loop on `posts:list` cannot starve `posts:create`.

| Routes | Limit |
|---|---|
| Reads: `posts:list`, `integrations:list`, `integrations:groups`, `integrations:settings`, `posts:missing`, `posts:find-slot`, notifications | 600/h (the `API_LIMIT` default; production sets 600) |
| Publish and delete: `posts:create`, `posts:delete`, `posts:delete-group`, `posts:status`, `integrations:trigger` | 60/h |
| Analytics and channel refresh: `analytics:platform`, `analytics:post`, `/social/:integration` | 30/h |
| Uploads: `upload`, `upload-from-url` | 30/h |
| Upload links: `upload:link` 60/h, `upload:files` 600/h | |

The bucket is keyed on the hash of the presented key, so rotating a key starts
a fresh allowance and the old secret's allowance dies with it. Exceeding a
limit returns `429`. **Back off; do not retry in a tight loop**: a retry
storm just burns the next hour's allowance too.

### Integration Discovery

```bash
# List all connected integrations
postemi integrations:list

# List integrations belonging to a specific group (customer)
postemi integrations:list --group <group-id>

# List all groups (customers) as {id, name}
postemi integrations:groups

# Get settings schema for specific integration
postemi integrations:settings <integration-id>

# Trigger integration tool to fetch dynamic data
postemi integrations:trigger <integration-id> <method-name>
postemi integrations:trigger <integration-id> <method-name> -d '{"param":"value"}'
```

### Creating Posts

```bash
# Simple post (date is REQUIRED)
postemi posts:create -c "Content" -s "2026-12-31T12:00:00Z" -i "integration-id"

# Draft post
postemi posts:create -c "Content" -s "2026-12-31T12:00:00Z" -t draft -i "integration-id"

# Post with media (upload each file FIRST, see Rule 2)
IMG1=$(postemi upload img1.jpg | jq -r '.path')
IMG2=$(postemi upload img2.jpg | jq -r '.path')
postemi posts:create -c "Content" -m "$IMG1,$IMG2" -s "2026-12-31T12:00:00Z" -i "integration-id"

# Post with comments (each with own media, every file uploaded first)
MAIN=$(postemi upload main.jpg | jq -r '.path')
C1=$(postemi upload comment1.jpg | jq -r '.path')
C2A=$(postemi upload comment2.jpg | jq -r '.path')
C2B=$(postemi upload comment3.jpg | jq -r '.path')
postemi posts:create \
  -c "Main post" -m "$MAIN" \
  -c "First comment" -m "$C1" \
  -c "Second comment" -m "$C2A,$C2B" \
  -s "2026-12-31T12:00:00Z" \
  -i "integration-id"

# Multi-platform post
postemi posts:create -c "Content" -s "2026-12-31T12:00:00Z" -i "$X_ID,$FB_ID,$THREADS_ID"

# Platform-specific settings
postemi posts:create \
  -c "Content" \
  -s "2026-12-31T12:00:00Z" \
  --settings '{"who_can_reply_post":"everyone"}' \
  -i "$X_ID"

# Complex post from JSON file
postemi posts:create --json post.json
```

### Managing Posts

```bash
# List posts (defaults to last 30 days to next 30 days)
postemi posts:list

# List posts in date range
postemi posts:list --startDate "2026-01-01T00:00:00Z" --endDate "2026-12-31T23:59:59Z"

# Delete one post (one channel, with its thread or comments); other channels of its group stay
postemi posts:delete <post-id>

# Delete a whole group: the post on every channel it went to (group from posts:list)
postemi posts:delete-group <group>

# Change post status (draft ↔ schedule)
postemi posts:status <post-id> --status draft     # Move back to draft, terminates any running publish workflow
postemi posts:status <post-id> --status schedule  # Promote a draft into the publishing queue (uses the post's stored date)
```

### Analytics

```bash
# Get platform analytics (default: last 7 days)
postemi analytics:platform <integration-id>

# Get platform analytics for last 30 days
postemi analytics:platform <integration-id> -d 30

# Get post analytics (default: last 7 days)
postemi analytics:post <post-id>

# Get post analytics for last 30 days
postemi analytics:post <post-id> -d 30
```

Returns an array of metrics (e.g. Followers, Impressions, Likes, Comments) with daily data points and percentage change over the period.

**⚠️ IMPORTANT: Missing Release ID Handling**

If `analytics:post` returns `{"missing": true}` instead of an analytics array, the post was published but the platform didn't return a usable post ID. You **must** resolve this before analytics will work:

```bash
# 1. analytics:post returns {"missing": true}
postemi analytics:post <post-id>

# 2. Get available content from the provider
postemi posts:missing <post-id>
# Returns: [{"id": "7321456789012345678", "url": "https://...cover.jpg"}, ...]

# 3. Connect the correct content to the post
postemi posts:connect <post-id> --release-id "7321456789012345678"

# 4. Now analytics will work
postemi analytics:post <post-id>
```

### Connecting Missing Posts

Some platforms (e.g. TikTok) don't return a post ID immediately after publishing. When this happens, the post's `releaseId` is set to `"missing"` and analytics are unavailable until resolved.

```bash
# List recent content from the provider for a post with missing release ID
postemi posts:missing <post-id>

# Connect a post to its published content
postemi posts:connect <post-id> --release-id "<content-id>"
```

Returns an empty array if the provider doesn't support this feature or if the post doesn't have a missing release ID.

### Media Upload

**⚠️ IMPORTANT:** Always upload files to Postemi before using them in posts. Many platforms (TikTok, Instagram, YouTube) **require verified URLs** and will reject external links.

```bash
# Upload file and get URL
postemi upload image.jpg

# EXACTLY EIGHT TYPES ARE ACCEPTED. Anything else returns 400 "Unsupported
# file type.". The server sniffs the magic bytes, so renaming the file does
# not help.
#
#   image/jpeg  image/png  image/gif  image/webp
#   image/avif  image/bmp  image/tiff              (max 10 MB)
#   video/mp4                                      (max 1 GB)
#
# NOT accepted: MOV, MKV, WEBM, AVI, SVG, PDF, DOC/DOCX, and every audio
# format. Convert first:  ffmpeg -i clip.mov -c:v libx264 -c:a aac clip.mp4
# See SUPPORTED_FILE_TYPES.md.

# Workflow: Upload → Extract URL → Use in post
VIDEO=$(postemi upload video.mp4)
VIDEO_PATH=$(echo "$VIDEO" | jq -r '.path')
postemi posts:create -c "Content" -s "2026-12-31T12:00:00Z" -m "$VIDEO_PATH" -i "tiktok-id"
```

---

## Common Patterns

### Pattern 1: Discover & Use Integration Tools

**Most supported channels have no tools at all.** Of the channels in the table
at the top of this file, six expose a tool: Instagram (`audioSearch`),
Discord (`channels`), Slack (`channels`), Pinterest (`boards`), WordPress
(`postTypes`, `categoriesList`, `tagsList`) and Dev.to (`tags`,
`organizations`). The others expose none: `integrations:settings`
returns an empty `tools` array for them, and `integrations:trigger` on them
returns `404 Tool not found`.

**Never guess a method name.** Read the `tools` array from
`integrations:settings` first; the `methodName` there is the only string
`integrations:trigger` will accept.

```bash
IG_ID=$(postemi integrations:list | jq -r '.[] | select(.identifier=="instagram") | .id')

# What can this channel actually do?
postemi integrations:settings "$IG_ID" | jq '.output.tools'
# [ { "methodName": "audioSearch", "description": "Search audio …", "dataSchema": [ … ] } ]
```

**Instagram, find audio for a Reel:**
```bash
# Empty query returns trending audio. type is "music" (default) or "original_sound".
AUDIO=$(postemi integrations:trigger "$IG_ID" audioSearch -d '{"q":"lofi","type":"music"}')
AUDIO_ID=$(echo "$AUDIO" | jq -r '.output[0].id')

VIDEO=$(postemi upload reel.mp4 | jq -r '.path')
postemi posts:create \
  -c "Reel caption" \
  -s "2026-12-31T12:00:00Z" \
  --settings "{\"post_type\":\"post\",\"audio\":{\"id\":\"$AUDIO_ID\"}}" \
  -m "$VIDEO" \
  -i "$IG_ID"
```

### Pattern 2: Upload Media Before Posting

```bash
# Upload multiple files
VIDEO_RESULT=$(postemi upload video.mp4)
VIDEO_PATH=$(echo "$VIDEO_RESULT" | jq -r '.path')

THUMB_RESULT=$(postemi upload thumbnail.jpg)
THUMB_PATH=$(echo "$THUMB_RESULT" | jq -r '.path')

# Use in post
postemi posts:create \
  -c "Check out my video!" \
  -s "2026-12-31T12:00:00Z" \
  -m "$VIDEO_PATH" \
  -i "tiktok-id"
```

### Pattern 3: Twitter Thread

```bash
# Upload every image first (Rule 2)
INTRO=$(postemi upload intro.jpg | jq -r '.path')
P1=$(postemi upload point1.jpg | jq -r '.path')
P2=$(postemi upload point2.jpg | jq -r '.path')
OUTRO=$(postemi upload outro.jpg | jq -r '.path')

postemi posts:create \
  -c "🧵 Thread starter (1/4)" -m "$INTRO" \
  -c "Point one (2/4)" -m "$P1" \
  -c "Point two (3/4)" -m "$P2" \
  -c "Conclusion (4/4)" -m "$OUTRO" \
  -s "2026-12-31T12:00:00Z" \
  -d 5 \
  -i "$X_ID"
# -d is the delay between comments in MINUTES (here: 5 minutes)
```

### Pattern 4: Multi-Platform Campaign (different content per channel)

JSON mode takes the API's real request body: `type`, `date`, `shortLink`,
`tags`, and a `posts` array where each element names an `integration`, its
`value` thread and its `settings`. There is no `"integrations"` key and no
`"provider"` key; a full working file is
[examples/multi-platform-post.json](./examples/multi-platform-post.json).

```bash
IMG=$(postemi upload sale.jpg | jq -r '.path')

cat > campaign.json << EOF
{
  "type": "schedule",
  "date": "2026-12-01T09:00:00Z",
  "shortLink": false,
  "tags": [],
  "posts": [
    {
      "integration": { "id": "<x-id>" },
      "value": [
        { "content": "Holiday sale! 🎄 20% off every plan. #sale", "image": [ { "id": "a", "path": "$IMG" } ] }
      ],
      "settings": { "who_can_reply_post": "everyone" }
    },
    {
      "integration": { "id": "<facebook-id>" },
      "value": [
        { "content": "Our holiday sale is live, 20% off every plan until the end of December. Details on the website!", "image": [ { "id": "b", "path": "$IMG" } ] }
      ],
      "settings": { "post_type": "post" }
    }
  ]
}
EOF

postemi posts:create --json campaign.json
```

### Pattern 5: Validate Settings Before Posting

```bash
#!/bin/bash

INTEGRATION_ID="$X_ID"
CONTENT="Your post content here"

# Get integration settings and extract max length
SETTINGS_JSON=$(postemi integrations:settings "$INTEGRATION_ID")
MAX_LENGTH=$(echo "$SETTINGS_JSON" | jq '.output.maxLength')

# Check character limit and truncate if needed
if [ ${#CONTENT} -gt "$MAX_LENGTH" ]; then
  echo "Content exceeds $MAX_LENGTH chars, truncating..."
  CONTENT="${CONTENT:0:$((MAX_LENGTH - 3))}..."
fi

# Create post with settings
postemi posts:create \
  -c "$CONTENT" \
  -s "2026-12-31T12:00:00Z" \
  --settings '{"key": "value"}' \
  -i "$INTEGRATION_ID"
```

### Pattern 6: Batch Scheduling

```bash
#!/bin/bash

# Schedule posts for the week
DATES=(
  "2026-02-14T09:00:00Z"
  "2026-02-15T09:00:00Z"
  "2026-02-16T09:00:00Z"
)

CONTENT=(
  "Monday motivation 💪"
  "Tuesday tips 💡"
  "Wednesday wisdom 🧠"
)

for i in "${!DATES[@]}"; do
  # Rule 2: upload each file before passing to -m
  IMG=$(postemi upload "post-${i}.jpg" | jq -r '.path')
  postemi posts:create \
    -c "${CONTENT[$i]}" \
    -s "${DATES[$i]}" \
    -i "$X_ID" \
    -m "$IMG"
  echo "Scheduled: ${CONTENT[$i]} for ${DATES[$i]}"
done
```

### Pattern 7: Error Handling & Retry

`posts:create` already retries for you: every run sends an `Idempotency-Key`
(a new UUID per run) and, after a network failure or a 5xx, retries ONCE with
the same key, so the server hands back the post it already made instead of
making a second one. Running the command again is a NEW key and a NEW post.
So never wrap `posts:create` in a retry loop; after a failure, look first:

```bash
#!/bin/bash

CONTENT="Your post content"
INTEGRATION_ID="$X_ID"
DATE="2026-12-31T12:00:00Z"

if postemi posts:create -c "$CONTENT" -s "$DATE" -i "$INTEGRATION_ID"; then
  echo "Post created successfully"
else
  # Did it get through anyway? Check before running it again.
  postemi posts:list --startDate "$DATE" --endDate "$DATE"
fi
```

A 403 that names a missing permission is not retryable: the key is valid
and lacks the scope. A 401 saying the workspace has no plan with API access
is not retryable either: see `billing:plans`.

---

## Technical Concepts

### Integration Tools Workflow

Some integrations expose a tool for data that cannot be hard-coded. Among supported channels Instagram, Discord and Slack do. The workflow:

1. **Check available tools** - `integrations:settings` returns a `tools` array
2. **Review tool schema** - Each tool has `methodName`, `description`, and `dataSchema`
3. **Trigger tool** - Call `integrations:trigger` with required parameters
4. **Use output** - Tool returns data to use in post settings

**Tools on supported channels, exhaustively:**

| Channel | Tools |
|---|---|
| Instagram (`instagram`) | `audioSearch` |
| Discord (`discord`) | `channels` (the server's channels; the `id` goes into `settings.channel`) |
| Slack (`slack`) | `channels` (the workspace's channels; the `id` goes into `settings.channel`) |
| X, Facebook, Threads, Bluesky, YouTube, LinkedIn, TikTok, Telegram | *(none)* |

That is the whole list. There is no `getPlaylists`, no `getCompanies`, no
`getBoards`, no `getFlairs`. Earlier versions of this file invented all four,
and `integrations:trigger` answers `404 Tool not found` for every one of them.

### Provider Settings Structure

Platform-specific settings use a discriminator pattern with `__type` field:

```json
{
  "posts": [
    {
      "provider": "youtube",
      "post": [{ "content": "Video description", "image": [...] }],
      "settings": {
        "__type": "youtube",
        "title": "Video title",
        "type": "public",
        "selfDeclaredMadeForKids": "no",
        "tags": [{ "value": "tech", "label": "Tech" }]
      }
    }
  ]
}
```

Pass settings directly:
```bash
postemi posts:create -c "Content" -s "2026-12-31T12:00:00Z" --settings '{"title":"…","type":"public"}' -i "youtube-id"
# Backend automatically adds "__type" based on integration ID
```

Channels with **no settings of their own** (Threads and Bluesky) take an
empty object. Do not invent fields for them.

**You never have to write `__type` yourself.** The server stamps it from the
integration's provider before validating, overwriting whatever you sent. An
example file carrying `"__type": "EmptySettings"` still works for that reason:
it is being replaced, not accepted.

### Two behaviours that surprise people

**1. A key without `posts:publish` silently produces a draft.** `posts:create`
requires only `posts:draft`. If the key (or its owner's current role, a
Contributor/DRAFTER) lacks `posts:publish`, the server coerces `type` to
`draft` and creates a draft instead of refusing. It is not silent in the
response: **read back the `type` you got, do not assume the one you sent.**
If the user wanted it published, tell them the key cannot, rather than
reporting success.

**2. One X channel per post, always.** A single post may not target two X
channels, whatever the content. X's Developer Policy forbids substantially
similar content from multiple accounts through one developer app, and the
account at risk is Postemi's, shared by every customer. Split it into two posts.
X alongside Facebook, Instagram, Threads, Bluesky, YouTube and the rest is
unaffected. That combination is the entire point.

### Comments and Threading

Posts can have comments (threads on Twitter/X, replies elsewhere). Each comment can have its own media:

```bash
# Upload every file first (Rule 2)
I1=$(postemi upload image1.jpg | jq -r '.path')
I2=$(postemi upload image2.jpg | jq -r '.path')
CI=$(postemi upload comment-img.jpg | jq -r '.path')
A1=$(postemi upload another.jpg | jq -r '.path')
A2=$(postemi upload more.jpg | jq -r '.path')

postemi posts:create \
  -c "Main post" -m "$I1,$I2" \
  -c "Comment 1" -m "$CI" \
  -c "Comment 2" -m "$A1,$A2" \
  -s "2026-12-31T12:00:00Z" \
  -d 5 \  # Delay between comments in minutes
  -i "integration-id"
```

Internally creates (note: every URL is a Postemi-uploaded `.path`, not a raw filename):
```json
{
  "posts": [{
    "value": [
      { "content": "Main post", "image": ["<uploaded image1>", "<uploaded image2>"] },
      { "content": "Comment 1", "image": ["<uploaded comment-img>"], "delay": 5 },
      { "content": "Comment 2", "image": ["<uploaded another>", "<uploaded more>"], "delay": 5 }
    ]
  }]
}
```

### Date Handling

**The contract: ALWAYS pass an explicit offset, or pass `--timezone` with an
IANA name.** The CLI never guesses a timezone. The server reads a naive
datetime as UTC, which silently shifts a local "12:00" by the user's UTC
offset. The CLI refuses ambiguity instead.

The two safe forms:

```bash
-s "2026-12-31T12:00:00Z"                                  # explicit UTC
-s "2026-12-31 12:00" --timezone Europe/London           # wall-clock + IANA zone
```

How a date is resolved, in priority order:

1. **Explicit offset in the string** (`Z`, `+01:00`), used as written.
2. **`--timezone <IANA name>`** on `posts:create` / `posts:list`.
3. **The saved config**: `postemi config:set timezone Europe/London`
   (also offered interactively during `postemi auth:login` on a TTY).
4. **None of the above and the date is naive → hard error, exit 1.** The
   error names the fixes. Do not retry the same naive date; add a
   timezone.

Rules and behaviors:

- Timezone values must be IANA names (`Europe/London`, `UTC`). **Numeric
  offsets (`+02:00`, `UTC+2`, `Etc/GMT+2`) are rejected as timezone values**.
  Never hand-compute DST; put an offset inside the date string only when
  you are certain of it, otherwise use the IANA name and let the CLI convert
  (DST-aware).
- Whenever a timezone is applied (steps 2 to 4), the CLI echoes the resolved
  UTC instant on stderr:
  `ℹ️  Interpreted "2026-12-24 18:00" as Europe/London (via --timezone) → 2026-12-24T18:00:00.000Z`
- A bare date (`"2026-12-31"`) means midnight in the resolved timezone.
- `posts:list --startDate/--endDate` accept the same shapes and the same
  `--timezone` flag; the defaults (30 days back / 30 days forward) never
  need a timezone.
- `postemi config:get` / `postemi config:get timezone` shows what is saved;
  settings survive `auth:logout`.
- `postemi posts:find-slot <integration-id>` returns `{"date": "..."}`, the
  next free slot on that channel's schedule; pass it straight back to
  `posts:create -s`.
- `-t now` publishes immediately and needs no `--date`.

### Media Upload Response

Upload returns JSON with path and metadata:
```json
{
  "path": "https://…/uploads/2026/08/abc123.jpg",
  "size": 123456,
  "type": "image/jpeg"
}
```

Extract path for use in posts:
```bash
RESULT=$(postemi upload image.jpg)
PATH=$(echo "$RESULT" | jq -r '.path')
postemi posts:create -c "Content" -s "2026-12-31T12:00:00Z" -m "$PATH" -i "integration-id"
```

### JSON Mode vs CLI Flags

**CLI flags** - Quick posts:
```bash
postemi posts:create -c "Content" -m "$(postemi upload img.jpg | jq -r '.path')" -s "2026-12-31T12:00:00Z" -i "$X_ID"
```

**JSON mode** - Complex posts with multiple platforms and settings:
```bash
postemi posts:create --json post.json
```

JSON mode supports:
- Multiple platforms with different content per platform
- Complex provider-specific settings
- Scheduled posts
- Posts with many comments
- Custom delay between comments

---

## Platform-Specific Examples

Every field below is taken from the server's validation DTOs. A field that is
not listed does not exist, and sending it is a `400`.

### X (Twitter): `x`
```bash
postemi posts:create \
  -c "Tweet content" \
  -s "2026-12-31T12:00:00Z" \
  --settings '{"who_can_reply_post":"everyone"}' \
  -i "$X_ID"
```
`who_can_reply_post` is **required**: `everyone` | `following` |
`mentionedUsers` | `subscribers` | `verified`. Optional: `community` (must
match `https://x.com/i/communities/<digits>`), `made_with_ai` (bool),
`paid_partnership` (bool).

### Facebook: `facebook`
```bash
IMG=$(postemi upload photo.jpg | jq -r '.path')
postemi posts:create \
  -c "Post text" \
  -s "2026-12-31T12:00:00Z" \
  --settings '{"post_type":"post"}' \
  -m "$IMG" \
  -i "$FB_ID"
```
All optional: `post_type` (`post` | `story`), `url`, `text_format_preset_id`
(a background for a **text-only** post; Pages only, ~130 characters max).

### Instagram: `instagram`
```bash
IMG=$(postemi upload image.jpg | jq -r '.path')

# Feed post
postemi posts:create -c "Caption #hashtag" -s "2026-12-31T12:00:00Z" \
  --settings '{"post_type":"post"}' -m "$IMG" -i "$IG_ID"

# Story
STORY=$(postemi upload story.jpg | jq -r '.path')
postemi posts:create -c "" -s "2026-12-31T12:00:00Z" \
  --settings '{"post_type":"story"}' -m "$STORY" -i "$IG_ID"
```
`post_type` is **required**: `post` | `story`. Optional: `collaborators` (array
of `{label}`), `audio` (`{id, title?, artist?, image?, audio_volume?,
video_volume?}`; get the `id` from the `audioSearch` tool), `is_trial_reel`,
`graduation_strategy` (`MANUAL` | `SS_PERFORMANCE`).

### Threads (`threads`) and Bluesky (`bluesky`)
```bash
postemi posts:create -c "Post text" -s "2026-12-31T12:00:00Z" -i "$THREADS_ID"
```
No provider settings. Omit `--settings` entirely.

## What Postemi does NOT do

State these plainly rather than attempting a workaround.

- **No AI video generation.** The `/generate-video` and `/video/function`
  routes were removed from the API entirely (2026-08-06). Do not tell a user
  Postemi can generate video, and do not call those routes: they 404.
- **No image or video generation of any kind.** Media comes from files the
  user already has, via `postemi upload`.
- **No channel deletion.** `DELETE /integrations/:id` was deliberately removed
  from the public API. Disconnecting a channel is a signed-in, admin action in
  the web app.
- **Nothing outside the channel table at the top of this file.**

---

## Optional skills: writing and growth

Two more Postemi skills are optional. They are not installed unless the user
chose them:

| Skill | What it adds | Install |
|---|---|---|
| writing (`postemi-writing` + `postemi-templates`) | post ideas, hooks, formatting, each network's writing rules, the composer's templates | `postemi skills add writing` |
| growth (`postemi-growth`) | choosing a niche, cadence per network, a 30-day plan, the weekly review | `postemi skills add growth` |

```bash
postemi skills list                          # core + optional, and where each is installed (JSON)
postemi skills add writing --json            # into every agent found (Claude Code, Codex, Cursor, Grok Build)
postemi skills add growth --agent claude --json
postemi skills remove growth --json
```

When the user asks for help writing posts or planning content and
`postemi skills list` shows the skill as missing, **offer** it: say what it
adds and ask. Run `postemi skills add` only after the user says yes; never
install it silently. Pass `--json` (or run without a terminal) so the CLI asks
no questions; a new agent session loads the skills.

---

## Supporting Resources

**This file is the command reference.** Everything the CLI accepts is
documented above; there is no second syntax guide to consult.

**Deep-dive documentation** (shipped in the npm package):
- [PROVIDER_SETTINGS.md](./PROVIDER_SETTINGS.md) - Settings schema for every supported channel
- [SUPPORTED_FILE_TYPES.md](./SUPPORTED_FILE_TYPES.md) - The eight accepted media types

**Ready-to-use `--json` payloads** (all verified against the current CLI):
- [examples/post-with-comments.json](./examples/post-with-comments.json) - Threading example
- [examples/thread-post.json](./examples/thread-post.json) - Multi-part thread
- [examples/multi-platform-post.json](./examples/multi-platform-post.json) - One post, several channels
- [examples/multi-platform-with-settings.json](./examples/multi-platform-with-settings.json) - Campaign example
- [examples/youtube-video.json](./examples/youtube-video.json) - YouTube with tags
- [examples/tiktok-video.json](./examples/tiktok-video.json) - TikTok with privacy

---

## Common Gotchas

1. **Not authenticated** - Ask the user to run `postemi auth:login` and approve it in the browser
2. **Invalid integration ID** - Run `integrations:list` to get current IDs
3. **Settings schema mismatch** - Check `integrations:settings` for required fields
4. **Media MUST be uploaded to Postemi first** - ⚠️ **CRITICAL (Rule 2):** Every value passed to `-m` or to an `image`/media field in JSON mode must be a `.path` returned by `postemi upload`. Raw local filenames (`image.jpg`) and external URLs (`https://...`) will be rejected. TikTok, Instagram, YouTube and most other providers only accept Postemi-verified URLs. No exceptions: even a "quick test post" needs the upload step.
5. **JSON escaping in shell** - Use single quotes for JSON: `--settings '{...}'`
6. **Date format** - ISO 8601 with an explicit offset (`"2026-12-31T12:00:00Z"`), or a naive datetime plus `--timezone <IANA name>`. A naive datetime with no timezone configured is a hard error. Required except with `-t now` or `--json`.
7. **Tool not found** - Check available tools in `integrations:settings` output
8. **Character limits** - Each platform has different limits, check `maxLength` in settings
9. **Required settings** - YouTube requires `title` and `type`; X requires `who_can_reply_post`; Instagram requires `post_type`; TikTok requires `privacy_level` and `content_posting_method`; Discord and Slack require `channel` (an id from their `channels` tool). Threads, Bluesky, LinkedIn and Telegram require nothing.
10. **Media MIME types** - CLI auto-detects from file extension, ensure correct extension
11. **Analytics returns `{"missing": true}`** - The post was published but the platform didn't return a post ID. Run `posts:missing <post-id>` to get available content, then `posts:connect <post-id> --release-id "<id>"` to link it. Analytics will work after connecting.

---

## Quick Reference

```bash
# ⚠️ AUTHENTICATE FIRST - required before any other command
postemi auth:status                                             # Check if authenticated
postemi auth:login                                              # OAuth2 device flow login
postemi auth:signup --email <address>                           # New account by e-mailed code; no free trial
postemi auth:logout                                             # Remove credentials

# Settings (survive logout)
postemi config:set timezone Europe/London         # Timezone for dates without an offset
postemi config:get                                  # Show saved settings as JSON

# Discovery (only after auth is confirmed)
postemi integrations:list                           # Get integration IDs
postemi integrations:list --group <group-id>        # Get integration IDs in a group
postemi integrations:groups                         # List groups (customers)
postemi integrations:settings <id>                  # Get settings schema
postemi integrations:trigger <id> <method> -d '{}'  # Fetch dynamic data

# Posting (date required unless -t now or --json; explicit offset or --timezone, never naive)
postemi posts:create -c "text" -s "2026-12-31T12:00:00Z" -i "id"                  # Simple (UTC)
postemi posts:create -c "Good morning!" -s "2026-12-31 08:00" --timezone Europe/London -i "id"  # Local wall-clock
postemi posts:create -c "text" -t now -i "id"                                     # Publish immediately
postemi posts:create -c "text" -s "2026-12-31T12:00:00Z" -t draft -i "id"        # Draft
postemi posts:create -c "text" -m "$(postemi upload img.jpg | jq -r '.path')" -s "2026-12-31T12:00:00Z" -i "id"  # With media (upload first, Rule 2)
postemi posts:create -c "main" -c "comment" -s "2026-12-31T12:00:00Z" -i "id"    # With comment
postemi posts:create -c "text" -s "2026-12-31T12:00:00Z" --settings '{}' -i "id" # Platform-specific
postemi posts:create --json file.json                                             # Complex

# Management
postemi posts:list                                  # List posts
postemi posts:find-slot <integration-id>            # Next free slot: {"date": "..."}
postemi posts:delete <id>                          # Delete one post (one channel)
postemi posts:delete-group <group>                 # Delete every channel of a group
postemi posts:status <id> --status draft           # Move to draft (stops workflow)
postemi posts:status <id> --status schedule        # Queue draft for publishing
postemi upload <file>                              # Upload media

# Analytics
postemi analytics:platform <id>                    # Platform analytics (7 days)
postemi analytics:platform <id> -d 30             # Platform analytics (30 days)
postemi analytics:post <id>                        # Post analytics (7 days)
postemi analytics:post <id> -d 30                 # Post analytics (30 days)
# If analytics:post returns {"missing": true}, resolve it:
postemi posts:missing <id>                         # List provider content
postemi posts:connect <id> --release-id "<rid>"    # Connect content to post

# Optional skills (ask the user first)
postemi skills list                                # Core + optional skills, where installed
postemi skills add writing|growth --json           # Install an optional skill

# Help
postemi --help                                     # Show help
postemi posts:create --help                        # Command help
```
