---
name: "multi-platform-rewrite"
description: "Rewrite one finished article, script, or post into versions for Douyin, Xiaohongshu, WeChat Channels, TikTok, and Reels, each with a cover, plus an optional short clip for the feeds that take them. This multi-platform rewrite keeps the same offer and changes the hook, length, and picture for each feed. Use it when one source should go out on several platforms the same day, including a reuse pass over a piece you already published."
---

# Multi-platform Rewrite

## What you get

- One rewritten version per platform you name, among Douyin, Xiaohongshu, WeChat Channels, TikTok, and Reels. Each version changes the hook, the length, and one sentence of context, and is labeled with its platform.
- One cover per version, built at that platform's ratio, not cropped out of another cover.
- One short spoken clip per video feed you name, made from that feed's cover, with the spoken hook on the picture.

## Ways to run it

- Copy set and clips. The default. Rewritten text, native covers, and one clip for each video feed.
- Copy set. Strike the clips on the card.
- With a live read. One lookup before the rewrite, to see how that topic is being posted on a platform we can read.

Open this when a finished piece should go out the same day on more than one feed. Say the platforms if you know them. Otherwise the default is Douyin, Xiaohongshu, and WeChat Channels.

## Scope and adjacent routes

Use this route when a finished piece should be adapted, not when the piece still has to be invented. A first short-video script belongs on a script workflow. A WeChat article with an operating plan belongs on an article workflow.

## Inputs and defaults

The hard input is the source text. Ask only for that. Default to Douyin, Xiaohongshu, and WeChat Channels, and `model` `auto` only for a still that has no source picture. Douyin, WeChat Channels, TikTok, and Reels get a 9:16 cover and a clip. Xiaohongshu gets a 3:4 cover and the note, and a clip only when the user asks for one. WeChat versions get copy and pictures. Do not invent WeChat metrics. Keep the offer, the face, and the claim inside the center of every frame.

## Golden path

1. Rewrite each selected platform. Add one sentence of context that was not in the source. Show the labeled set. This writing is free.
2. If a live read is in scope, use `beatra.social.tools.search` and `beatra.social.tools.get`, copy `schema_hash`, show a lookup card, and call `beatra.social.execute` once. Allowed keys are `social.douyin.video.search`, `social.douyin.video.comments.list`, `social.xiaohongshu.note.search`, `social.xiaohongshu.note.comments.list`, `social.tiktok.video.search`, and `social.twitter.tweet.search.recent`.
3. For each cover, `beatra.images.transform` after `{"capability": "image_to_image"}` from the source picture or from the first accepted cover, at that platform's ratio. `beatra.images.generate` after `{"capability": "text_to_image"}` only when there is no picture to carry. One `beatra.images.edit` repairs a cover whose claim came back unreadable.
4. Pick one ready voice with `beatra.voices.list`. One `beatra.speech.synthesize` after `{"capability": "text_to_speech"}` per clip. One shared instrumental `beatra.music.generate` after `{"capability": "text_to_music"}` when a clip is in the set.
5. Materials card, then the video card: one `beatra.videos.animate` after `{"capability": "image_to_video"}` per clip, from that cover, hook as `driving_audio`.
6. One `beatra.videos.compose` per clip keeps that hook's sound, ducks the shared bed, and burns the on-screen line. Poll with `beatra.tasks.get` and deliver each labeled version plus `billing.net_charged_credits`.

## Decisions that require confirmation

Planning and the written deliverable are free. They are not approval.

Before every paid call, show a current production card and wait:

1. Work — what will be made, in the user's words, and whether this call is a generate or a lookup.
2. Credits — the live price just read from the model card or from `beatra.social.tools.get`. Do not reuse a remembered number.
3. Count — one paid call per slot. The materials card may list every cover, line, and the bed; each slot has its own `client_request_id`. A later lookup page is another call. Video calls wait for their own card.
4. Identity — one new opaque `client_request_id` per call. A changed prompt, file, model, or control mints a new ID.
5. If we stop here — the free writing remains usable.
6. If the balance is insufficient — relay the official message and its top-up URL. Do not retry until the user says they have topped up.

A lookup and a generate are two cards. Approved covers and lines do not authorize a clip. Invoke every remote Beatra tool only through the bundled `scripts/mcp_client.py`. The tool name is the command argument and the JSON arguments are the standard input. Do not configure, call, or use a host Beatra Connector. Do not use REST/OpenAPI as a fallback.

If a create response is lost, retry only the identical payload and the same `client_request_id`. If the task id is lost, call `beatra.tasks.list`, then `beatra.tasks.get`, and match the frozen request before any identical retry. Call `beatra.tasks.cancel` only when the user asks to cancel, then confirm that task with `beatra.tasks.get`.

When the user asks how many credits remain, call `beatra.wallet.get`. When they ask what was charged, call `beatra.wallet.ledger`.

## References by task

Read [the scenario workflow](references/workflow.md) for the ratios, the payloads, and a worked set.
Read [answers when a run goes wrong](references/faq.md) when a task stalls, a response is lost, a price looks wrong, or a cover came back wrong.
Read [installation and authentication](references/installation-and-auth.md) when the connection is not ready.
Read [installation registration](references/installation-registration.md) for first-use registration.
Read [Bundled MCP Client diagnostics](references/mcp-connection.md) when a call fails before a task exists.
Read [tasks and results](references/tasks-and-results.md) when a task is queued, running, or missing.
Read [billing, errors, and recovery](references/billing-errors-and-recovery.md) when a charge, a refund, or a lost response needs the shared rules.
Read [uninstall and disconnect](references/uninstall-and-disconnect.md) when the user wants to stop and remove the connection.

## Updates and security

This Skill runs only the files installed with it and leaves them unchanged while
it runs; it never downloads or executes other code. It talks to Beatra's official
services over HTTPS, and a file you choose to upload goes only to the one-time
upload address Beatra issues for it.

Once a day at most, the bundled client reads Beatra's public version list. When
the store or tool you installed from has a newer version, it prints one line with
the command that updates it there. Updating stays your choice, through that store
or tool. See [updates and security](references/updates-and-security.md).
