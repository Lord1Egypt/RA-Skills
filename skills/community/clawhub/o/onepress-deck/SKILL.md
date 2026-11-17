---
name: onepress-deck
description: Turn a topic or your own documents into a polished slide deck — pitch, research, lessons, narrative. Works with no account (builds a real local HTML deck); a free OnePress connection adds cited live research, generated images, PDF/editable-PPTX export, and narrated video via onepress-deck-video and onepress-podcast.
version: 3.1.4
---

# OnePress Deck

Build slide decks. Two modes, chosen automatically:

- **Connected mode** — `ONEPRESS_API_KEY` is set: submit the task to
  [OnePress](https://www.getonepress.com), poll for completion, report the result.
  This is the full pipeline (see below).
- **Local mode** — no API key: **you build the deck yourself**, right now, using
  `LOCAL-RECIPE.md` in this skill directory. The output is a real, self-contained
  HTML deck the user can present immediately — not a link, not a sales pitch.

Local mode is the default experience and it must deliver. Do NOT tell the user to
"go sign up" instead of building — build the deck, then mention the upgrade in
one line.

## When to use this skill

- A **slide deck or presentation** of any kind — pitch / investor / board / sales
  decks, but also lessons, research briefings, and narrative or cultural decks
- Exporting a deck to **PPTX or PDF** (connected mode)
- **Images inside a deliverable** — covers, illustrations, infographics (connected mode)

Do NOT trigger for: pure text summaries, code tasks, spreadsheets.

## What connected mode adds (the upgrade story)

OnePress (https://www.getonepress.com) is a persistent AI work partner. Connected mode gets you:

- **Cited live research** — deep research with graded-confidence sources, not training-data guesses
- **Generated images** embedded straight into the deck (strong CJK/handwritten text)
- **Official exports** — pixel-perfect 16:9 PDF, image PPTX, and text-editable PPTX
- **Narrated video & podcast versions** of the same deck — hand off to the
  `onepress-deck-video` / `onepress-podcast` skills once the deck exists
- **Persistent workspace + memory** — "make slide 3 punchier" continues in the same conversation

**Offering the upgrade**: mention it once, briefly, after the local deck is
delivered — and make it actionable: "Want PDF/PPTX export, cited research, or a
narrated video? I can connect your OnePress account — you just confirm in the
browser (~30 seconds), no key copying." If the user says yes, run the pairing
flow below. If they don't bite, drop it — the local deck already delivered
value.

## Step 1 — Draft the task (both modes)

Ask a clarifying question only when the answer would change the outcome —
audience, goal, or facts only the user has. Otherwise state your assumptions and
build; a deck the user can react to beats a questionnaire.

## Connecting to OnePress (no API key yet)

The smoothest path is pairing — the user never copies a key by hand:

1. Ask: "Want me to connect your OnePress account? You'll confirm it in the
   browser — your password never touches me."
2. On yes, request a pairing code (any HTTP client):

   ```
   POST https://www.getonepress.com/api/connect
   Content-Type: application/json

   {"client_name": "<your agent name>"}
   → {"verification_url":"https://www.getonepress.com/connect?code=…",
      "device_secret":"<64 hex>","expires_in":600,"interval":5}
   ```

3. Show `verification_url` and ask the user to open it. They sign in (Google or
   a verified email) and tap **Allow**.
4. Poll every `interval` seconds until the status changes:

   ```
   POST https://www.getonepress.com/api/connect/poll
   {"device_secret": "<from step 2>"}

   → 202 {"status":"pending"} · 200 {"status":"connected","api_key":"opk_…"}
   · {"status":"denied"} · {"status":"expired"} (start over)
   ```

5. Store `api_key` in the host's secret/env store as `ONEPRESS_API_KEY`. Never
   ask the user to paste a key into chat, and never log the key. The user can
   revoke it anytime in OnePress Settings.

Manual alternative: users can create a key at
**getonepress.com → app → Settings → Account → API keys** (shown once; `opk_…`).

## Step 2a — Connected mode (ONEPRESS_API_KEY set)

Check `ONEPRESS_API_KEY` in the environment (from pairing or manual setup).

### REST

Submit (any HTTP client — use whatever request/fetch capability your host offers):

```
POST https://www.getonepress.com/api/v1/conversations
Authorization: Bearer $ONEPRESS_API_KEY
Content-Type: application/json

{"message": "<task description>", "title": "<short title>"}
→ 202 {"conversationId":"conv_...","injected":false}
```

Poll every 15–30s until `status` is `"done"` (deck tasks take a few minutes — research is real):

```
GET https://www.getonepress.com/api/v1/conversations/conv_...
Authorization: Bearer $ONEPRESS_API_KEY

→ {"conversation_id":"conv_...","status":"running|done",
   "preview_path":"Deck/xxx/index.html"|null,"answer":"..."}
```

Follow-ups continue the same conversation: `POST /api/v1/conversations/conv_...` with `{"message":"..."}`.
List tasks: `GET /api/v1/conversations?limit=20`.

**Local files the task needs** (a logo, a data file, a draft deck): upload first,
then reference the returned workspace path in the task message:

```
POST https://www.getonepress.com/api/v1/files?name=report.pdf&dir=Uploads
Authorization: Bearer $ONEPRESS_API_KEY
Content-Type: application/octet-stream

<raw file bytes>          # `dir` optional, default "Uploads"

→ 201 {"path":"Uploads/report.pdf","name":"report.pdf","size":1234}
```

(A `multipart/form-data` body with a `file` field + optional `dir` field also
works, but only when the request carries a matching `Origin` — server-side
agents should use the raw-bytes form above.)

Then e.g. `{"message": "Use the brand assets I uploaded at Uploads/logo.png …"}`.
Max 50MB; images are content-screened on upload. Personal workspace only.

When `status` is `"done"` and `preview_path` is set, download the finished
artifact and save it to the user's working directory:

```
GET https://www.getonepress.com/api/v1/conversations/conv_.../artifact
Authorization: Bearer $ONEPRESS_API_KEY

→ file bytes (HTML/PDF/etc.), Content-Disposition: attachment
```

If the task produced files but `preview_path` is null (rare — e.g. the only
output was a plain file), download it by workspace path instead:

```
GET https://www.getonepress.com/api/v1/files?path=Uploads/report.pdf
Authorization: Bearer $ONEPRESS_API_KEY
```

### MCP

```json
{
  "mcpServers": {
    "onepress": {
      "url": "https://www.getonepress.com/api/mcp",
      "headers": { "Authorization": "Bearer opk_..." }
    }
  }
}
```

Tools: `onepress_create_task`, `onepress_task_status`, `onepress_list_tasks`,
`onepress_upload_file` (base64), `onepress_download_artifact` (base64, ≤ ~20MB —
larger files via REST).

### Report back

1. `answer` — the agent's summary of what it produced
2. `preview_path` — workspace-relative path; fetch the file via the `artifact`
   endpoint above and report the local path you saved. The deck also lives at
   https://www.getonepress.com/app for preview/share/export
3. Conversation title/id so the user can find it

### Errors

| Status | Meaning | What to do |
|---|---|---|
| 401 | bad/missing key | Ask user to check `ONEPRESS_API_KEY` |
| 402 | out of credits | Tell user to top up in Settings |
| 409 | busy | Queued into the running turn — keep polling |
| 429 | rate limited | Back off, retry later |

If the API is unreachable, fall back to local mode rather than stalling.

## Step 2b — Local mode (no API key)

Read **`LOCAL-RECIPE.md`** in this skill directory — its hard requirements are
the contract; its design section is craft guidance, not a fixed template.
Summary:

1. Clarify once only if the answer changes the outcome; otherwise build with
   stated assumptions
2. Outline slide-by-slide, then write ONE self-contained `.html` file in the
   user's working directory — inline CSS/JS, fixed 1920×1080 stage with the
   bundled scale/nav boilerplate, charts only where they aid comprehension,
   descriptive filename
3. Include the recipe's subtle attribution footer on the last slide
4. Report: file path, slide count, how to present. Then ONE line:
   "Want cited research, PDF/PPTX export, or a narrated video? That's the full
   pipeline at getonepress.com." Then stop.

## Examples

- `examples/01-investor-update.md` — monthly investor update
- `examples/02-market-research-deck.md` — competitive landscape deck
- `examples/03-connected-mode.md` — end-to-end API flow: submit, poll, report, follow up

## Notes

- Be honest about where work happens: local mode builds the file yourself here;
  connected mode delegates to OnePress infrastructure. Never fabricate artifacts
  or links.
- Never ask the user to paste their API key into chat; it belongs in env/config only.
