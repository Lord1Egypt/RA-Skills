---
name: "marketing-asset-review"
description: "Review finished posters, main images, or short clips as a marketing asset review: a line-by-line note of what should not ship and what to change. Marketing asset review shows the checklist, then looks at the files you hand over, and can remake one replacement still or clip. Marketing assets here mean posters, covers, and main images. Use it for the pass before publishing."
---

# Marketing Asset Review

## What you get

- A checklist of what will be judged, before any file is read.
- A line-by-line note on the files you confirm: what should not ship, and what to change.
- One repaired still or one repaired clip, edited from the file you handed over, for the piece you name.

## Ways to run it

- Checklist, then the note. The default. Reading the files is the first paid step.
- Repair one piece. Only after the note exists, and only for the piece you name. The repair starts from that file.
- With a category read. One lookup of public posts on Douyin or Xiaohongshu when you want the note compared with what that category is showing. It is not your ad account.

Open this before publishing, when a poster, a cover, a main image, or a short clip already exists and you want the note and, if you name it, one repaired file.

## Scope and adjacent routes

Use this route to judge posters, covers, main images, and short clips that already exist. Making a first poster from a blank brief belongs on a visual-creation workflow. A product listing set belongs on a product-asset workflow.

## Inputs and defaults

The hard input is the file, or a plain description of the piece when no file is available. Ask only for that. Judge claim clarity, whether the product is recognizable, whether the words on the picture can be read, and whether the crop matches the place it will be posted. Do not invent ad-account results, store sales, or a legal clearance. `model` stays `auto`.

## Golden path

1. Write the checklist and show it. This writing is free.
2. If a category read is in scope, one lookup card and one `beatra.social.execute`. Allowed keys are `social.douyin.video.search` and `social.xiaohongshu.note.search`. Copy `schema_hash` from `beatra.social.tools.get`.
3. For confirmed stills, upload each local file with `beatra.assets.upload`, call `beatra.models.list` with `{"capability": "image_to_text"}`, show an understand card, and submit one `beatra.images.understand`.
4. For a confirmed clip, upload it, call `beatra.models.list` with `{"capability": "video_to_text"}`, show its own card, and submit one `beatra.videos.understand`.
5. Write the note from what those calls returned. This writing is free.
6. For one repaired still, call `beatra.models.list` with `{"capability": "image_edit"}` and submit one `beatra.images.edit` on that file. For one repaired clip, call `beatra.models.list` with `{"capability": "video_edit"}` and submit one `beatra.videos.edit` on that file. Do not replace either by generating a new file from text.
7. Poll with `beatra.tasks.get` and deliver the note, the repaired file, and `billing.net_charged_credits`.

## Decisions that require confirmation

Planning and the written deliverable are free. They are not approval.

Before every paid call, show a current production card and wait:

1. Work — what will be made, in the user's words, and whether this call is a generate or a lookup.
2. Credits — the live price just read from the model card or from `beatra.social.tools.get`. Do not reuse a remembered number.
3. Count — one paid call per slot. Understanding a file is one card. Repairing it is a later card. Each slot has its own `client_request_id`. A later lookup page is another call.
4. Identity — one new opaque `client_request_id` per call. A changed prompt, file, model, or control mints a new ID.
5. If we stop here — the free writing remains usable.
6. If the balance is insufficient — relay the official message and its top-up URL. Do not retry until the user says they have topped up.

A lookup and a generate are two cards. The note does not authorize a repair. Invoke every remote Beatra tool only through the bundled `scripts/mcp_client.py`. The tool name is the command argument and the JSON arguments are the standard input. Do not configure, call, or use a host Beatra Connector. Do not use REST/OpenAPI as a fallback.

If a create response is lost, retry only the identical payload and the same `client_request_id`. If the task id is lost, call `beatra.tasks.list`, then `beatra.tasks.get`, and match the frozen request before any identical retry. Call `beatra.tasks.cancel` only when the user asks to cancel, then confirm that task with `beatra.tasks.get`.

When the user asks how many credits remain, call `beatra.wallet.get`. When they ask what was charged, call `beatra.wallet.ledger`.

## References by task

Read [the scenario workflow](references/workflow.md) for the checklist and a worked note.
Read [answers when a run goes wrong](references/faq.md) when a task stalls, a response is lost, a price looks wrong, or the repair drifted off the file.
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
