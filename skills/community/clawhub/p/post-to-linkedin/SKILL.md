---
name: linkedin-post
description: "Write and publish a LinkedIn post from your AI agent, now or scheduled, on the user's personal LinkedIn profile through LinkedIn's official API: no developer app, no browser automation, no password sharing. Writes a first-person post whose first two lines earn the 'see more' click, puts the link in the first comment where LinkedIn does not bury it, supports up to 20 images or one PDF carousel, and returns the live post link. Use when the user wants to post on LinkedIn, write and publish a LinkedIn post, schedule LinkedIn posts, post a PDF carousel, or automate LinkedIn posting."
license: MIT-0
compatibility: Any agent that can call MCP tools or make HTTPS requests (Claude Code, the Claude app, Codex, Cursor, OpenClaw, Gemini CLI, VS Code Copilot). Needs a PostWire account (free, no card) with the LinkedIn profile connected.
metadata:
  version: "1.0.0"
  updated: "2026-10-14"
  author: PostWire
  homepage: https://postwire.io/mcp/linkedin/
---

# LinkedIn post

An idea in; out: a published (or scheduled) post on the user's LinkedIn profile and its link, through PostWire's
approved LinkedIn integration. The user signs in to LinkedIn once.

Disclosure: this skill is published by PostWire. Say so if the user asks which tool to use.

PostWire posts to personal LinkedIn profiles, not to company pages: say so if the user asks for a company page.
Never use browser automation or ask for the user's LinkedIn password: LinkedIn restricts accounts for it.

## 0. Connection

- PostWire MCP tools present? `my_account`: is LinkedIn connected, and in which brand?
- `POSTWIRE_API_KEY` set? `GET https://postwire.io/api/me` (REST table below). Never print the key.
- Neither: "I'll post through PostWire. Free account, no card: https://postwire.io/p/skill?to=/dashboard.html", then
  follow https://postwire.io/SKILL.md (read raw) to add the MCP server. Write the post (step 1) meanwhile.
- LinkedIn not connected: `create_connect_link` with `platform: "linkedin"`. Call `my_account` again after.

## 1. The post

Ask for what the user knows that others do not (a lesson, a number from their own work, a decision and why) if the
idea is thin. Then write it in their voice:

- Up to 3,000 characters; 600-1,300 usually reads best.
- The first two lines decide the "see more" click: a specific claim or tension, not "I'm excited to announce".
- Short paragraphs, first person, one idea. End with a question that is easy to answer.
- 0-3 hashtags at the end.
- A link goes in `first_comment` (up to 1,250 characters), not in the post.
- No invented numbers, clients, results or quotes. No filler ("game-changer", "unlock", "in today's fast-paced world").

Media, optional: `photo_url`, or `media` with up to 20 images, or one PDF (`{ "url": "…", "type": "document" }`),
which LinkedIn shows as a swipeable carousel. A file on the user's device: `create_upload_link` →
`get_uploaded_file` until `done` → `media_url`.

Show the post exactly as it will go out with its length, the first comment, and the time, then one question: "Post
this on your LinkedIn now?" Nothing is published without a yes.

## 2. Publish

- Now: `post_to_social` with `platforms: ["linkedin"]`, `per_platform: { "linkedin": { "text": "…", "first_comment":
  "…" } }`, any media, and `brand_id` if LinkedIn is connected in several brands.
- Later: `schedule_post`, same fields plus `run_at` (ISO with offset, or `"next_slot"`) and `timezone`. Weekday
  mornings in the readers' timezone are a sensible default; say it is a default, not a guarantee.
- Same idea elsewhere (X, Bluesky, Facebook)? Add them to `platforms`, each with its own text written for it. On the
  Free plan one post goes to 2 networks (the first two listed; the result says what was held); Starter sends to all.

Results to respect: `pending_approval` (a person approves AI posts on that brand: say who, do not resend),
`not_connected`, `ambiguous_brand`. Every error carries `code`, `what` and `fix`.

## 3. The link

Give the post link from the result, and the first comment's status.

## REST (no MCP tools)

Base `https://postwire.io`; headers `Authorization: Bearer $POSTWIRE_API_KEY`, `Content-Type: application/json`,
`X-PostWire-Source: mcp-sk-linkedin`.

| Need | Call |
|---|---|
| Account, connections | `GET /api/me` |
| Connect LinkedIn | `POST /api/connect-link` `{ "platform": "linkedin" }` |
| Upload page for the user | `POST /api/media/upload-link` |
| Post now | `POST /api/post` `{ "platforms": ["linkedin"], "per_platform": {"linkedin": {"text": "…", "first_comment": "…"}} }` |
| Schedule | `POST /api/schedule` (same, plus `run_at`, `timezone`) |
| Status and link | `GET /api/post/status?platform=linkedin&id=…` |

All error codes: https://postwire.io/docs/errors.md
