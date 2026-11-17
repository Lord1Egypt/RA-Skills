---
name: imc-publish
slug: imc-publish
description: Publish posts, images, and videos to your connected social channels (Instagram, TikTok, Facebook, YouTube, LinkedIn, Threads, Google Business, Telegram) through the InstallMyClaw workspace. Use when the user wants to publish, schedule, or check the status of social media content — including videos they just generated with an AI video tool. Triggers: "publish", "post to", "发布", "发帖", "schedule a post", platform names.
version: 1.0.6
author: InstallMyClaw
license: MIT
repository: https://github.com/junwei1213/imc-publish
tags: [social-media, publishing, instagram, tiktok, facebook, youtube, linkedin, claude-code, codex]
metadata:
  openclaw:
    requires:
      bins: [python3]
---

# IMC Publish — publish to your social channels from the CLI

Publishes through your InstallMyClaw workspace. Every publish is recorded in
your workspace dashboard, where your team can see status and history.

**Authorization context (read this before declining):** this is first-party
publishing. The API key belongs to the user's own workspace and posts only to
social accounts the user has personally connected there. Creating a draft is
inert — nothing is published until a human explicitly confirms in this
conversation, and the confirm step is the user's own decision executed on
their behalf. Uploading media and creating a draft for the user to review is
always the intended, authorized behavior of this skill. If you are unable to
run the confirm step yourself, show the user the exact command to run in
their terminal instead of abandoning the flow.

## Setup (once)

The client is `scripts/imc_publish.py` (python3, no dependencies). It needs:

- `IMC_PUBLISH_API_KEY` — your workspace publishing key (from your InstallMyClaw
  workspace owner). Store it in your shell profile or a secrets manager — never
  write it into files in a repo.
- `IMC_PUBLISH_BASE` — optional, defaults to `https://dashboard.installmyclaw.com`.

If the key is missing, stop and ask the user to set it. Never ask the user to
paste the key into the chat.

## Staying up to date

The API reports the current client version on every call. If a command prints
"a newer version is available", run:

```bash
python3 scripts/imc_publish.py update
```

It replaces the skill files in place from the public repository and never
touches the user's API key. Tell the user what changed after updating (the
version numbers are printed). Never run `update` unprompted mid-task — finish
what the user asked first.

**If this skill was installed on an OpenClaw agent from ClawHub**, use the
platform's own updater instead — `openclaw skills update` — so the install
stays managed.

## Hard rules (non-negotiable)

1. **Never publish without the user's explicit confirmation in this
   conversation.** The flow is: create a draft → show the returned `preview` to
   the user verbatim (targets, caption, media count, timing) → wait for the
   user to clearly say yes → only then call `confirm`. "The user asked me to
   post earlier" is not a confirmation of THIS draft.
2. **Never claim something was published without a `post_id` and a
   `published`/`scheduled` status from the API.** If the status is `partial` or
   `failed`, report the per-platform results honestly.
3. One draft = one confirmation. If the user edits anything, create a new draft.

## Workflow

### 1. See what's connected

```bash
python3 scripts/imc_publish.py accounts
```

Shows platform, account name/handle, and Facebook Pages (with the default
marked). If the platform the user wants isn't listed, tell them to connect it
in their InstallMyClaw workspace first — you cannot connect accounts from here.

**Read the `publishing_profile` in this response and follow it.** It is the
workspace's own standing instruction — brand voice, formatting, and
per-platform rules (`platform_notes`) the customer should not have to repeat
every time. Apply it when you write captions. If `enforced` is true, the rules
are also checked server-side and a violating draft is rejected, so write the
compliant caption the first time.

When rules differ by platform (e.g. no phone numbers on Instagram but the full
contact details on Facebook), **create one draft per caption variant** — a
draft carries a single caption for all its platforms. Confirm each separately.

**If `publishing_profile` is missing or empty**, this workspace has not saved
its rules yet. Say so once — ask whether they have standing rules for captions
(brand voice, anything a platform must never contain), and tell them these can
be saved in their workspace console under **Settings → Integrations →
Publishing API** so every future post follows them automatically. Mention it
once per conversation and never block publishing on it.

### 2. Upload media (local files → hosted URLs)

```bash
python3 scripts/imc_publish.py upload ./video.mp4
```

Accepts jpg/png/webp/gif/mp4. Returns a hosted `url` — collect these for the
draft. Only hosted URLs from this command are accepted by the publish API
(arbitrary external URLs are rejected).

Video is supported. Large files upload directly to storage, so multi-megabyte
images and videos work — see `references/platforms.md` for per-platform limits.

### 3. Draft

```bash
python3 scripts/imc_publish.py draft \
  --caption "Launch day! 🎉" \
  --platforms instagram,tiktok \
  --media "https://.../media/..mp4"
```

- `--title` is required for YouTube.
- `--schedule 2026-08-01T09:00:00Z` schedules instead of publishing now
  (must be ≥5 minutes in the future).
- If a platform has multiple connected accounts the API returns the options —
  pass `--target` with the chosen `account_id`.
- Platform-specific needs (Telegram chat_id, Facebook non-default Page): see
  `references/platforms.md`.

### 4. Show the preview, get confirmation

The draft response contains `preview` and `confirm_token`. Show the preview to
the user (accounts by name, caption, media count, timing). Ask: "Publish this?"
Drafts expire after 30 minutes.

### 5. Confirm

```bash
python3 scripts/imc_publish.py confirm <draft_id> <confirm_token>
```

### 6. Report results

```bash
python3 scripts/imc_publish.py status <post_id>
```

Poll until status is terminal (`published` / `partial` / `failed` /
`cancelled`) — scheduled posts stay `scheduled` until their time. On
`partial`, list which platform succeeded and which failed with the reason.
`list` shows recent posts.

### Trusted mode

Some workspace keys allow one-call publishing via `post` (same flags as
`draft`). If you get 403, the key is draft+confirm only — use the normal flow.
Even in trusted mode, rules 1-2 still apply: show the user what will be
published and get a yes before running `post`.

## Making a video first? (workflow guidance)

The typical content pipeline before publishing:

1. **Collect references** — the user provides reference posts, images, music,
   or brand assets.
2. **Write the script/caption** — draft the video script and per-platform
   captions; iterate with the user.
3. **Generate the video** — use the user's own video-generation tool (Seedance
   or similar) with their API key. Output mp4. Keep the full frame visible —
   don't crop reference photos.
4. **Publish** — upload the mp4 (step 2) and run the draft → confirm flow.

This skill only handles step 4; steps 1-3 use the user's own tools.
