---
name: onepress-deck-video
description: Turn a slide deck or topic into a narrated explainer video — drafts the narration script and shot plan locally first, then renders and voices it on OnePress into an MP4. Connects via browser-confirmed pairing (no key copying); pairs with onepress-deck to narrate decks it built.
version: 1.2.0
---

# OnePress Deck Video

Produce narrated slide videos through [OnePress](https://www.getonepress.com) —
explainer videos, narrated pitch decks, video versions of research briefings.

**Two phases**: (1) draft the narration script and shot plan locally — a real
deliverable the user can read and edit; (2) render frames, synthesize
narration, and assemble the MP4 on OnePress infrastructure — that part
requires a connection. Always complete phase 1 before offering to connect.
Do not pretend to render video locally.

## When to use

- "Make a narrated video of this deck"
- "Turn my pitch into a 2-minute explainer video"
- "I need an MP4 version of the investor update"

For building the deck itself, use the `onepress-deck` skill (it also works
locally without a key).

## Phase 1 — Draft the narration plan (local, no connection needed)

Write the video plan to a local file (e.g. `video-plan.md`) — a real
deliverable the user reviews before any rendering happens:

- Per-slide narration lines — written to be spoken, short sentences, natural
  rhythm. One speaker per line.
- Duration estimate per slide and total runtime.
- Slide/shot notes: what visual each narration segment maps to (existing deck
  slide, or a planned slide if the deck doesn't exist yet).
- Match the script language to the user's request — narration voices are
  chosen per language, so the script language decides the accent.
- Show the plan to the user and iterate briefly.

## Phase 2 — Render it (requires connection)

Once the plan lands, offer: "The narration plan's ready — want me to render
it into an MP4? Connecting takes ~30 seconds, you just confirm in the
browser." If `ONEPRESS_API_KEY` is already set, skip the pairing steps.

If the user says yes and no key is configured, connect — the user never
copies a key:

1. Ask: "Want me to connect your OnePress account? You'll confirm it in the
   browser — your password never touches me."
2. On yes:

   ```
   POST https://www.getonepress.com/api/connect
   Content-Type: application/json

   {"client_name": "<your agent name>"}
   → {"verification_url":"https://www.getonepress.com/connect?code=…",
      "device_secret":"<64 hex>","expires_in":600,"interval":5}
   ```

3. Show `verification_url`; the user opens it, signs in (Google or verified
   email), and taps **Allow**.
4. Poll every `interval` seconds:

   ```
   POST https://www.getonepress.com/api/connect/poll
   {"device_secret": "<from step 2>"}

   → 202 {"status":"pending"} · 200 {"status":"connected","api_key":"opk_…"}
   · {"status":"denied"} · {"status":"expired"} (start over)
   ```

5. Store `api_key` in the host's secret/env store as `ONEPRESS_API_KEY`. Never
   ask the user to paste a key into chat, and never log it. Users can revoke it
   anytime in OnePress Settings (or create one manually at
   **Settings → Account → API keys**).

## How it works

Upload the local files (narration plan, and the source deck if it's local) via
`POST /api/v1/files`, then reference the workspace paths in the task:

```
POST https://www.getonepress.com/api/v1/files?name=deck.html&dir=Uploads
Authorization: Bearer $ONEPRESS_API_KEY
Content-Type: application/octet-stream

<raw file bytes>          # `dir` optional, default "Uploads"

→ 201 {"path":"Uploads/deck.html","name":"deck.html","size":1234}
```

Max 50MB. Personal workspace only.

Then submit the render task — reference the plan so the agent voices *your*
script rather than writing its own:

```
POST https://www.getonepress.com/api/v1/conversations
Authorization: Bearer $ONEPRESS_API_KEY
Content-Type: application/json

{"message": "Render a narrated video: deck at Uploads/deck.html, narration plan at Uploads/video-plan.md. ~<duration>, voice: <preference>.", "title": "<title>"}
→ 202 {"conversationId":"conv_..."}
```

**Voices**: narration defaults to a native-voice match for the video's
language (Mandarin voices for Chinese, English voices for English).
Override in the message, e.g. "voice: calm female".

**Voice cloning**: the user can narrate in their own voice. Upload a clean
15–60s single-speaker sample via `POST /api/v1/files`, then ask in the
message: "clone the voice in Uploads/<file> and use it for the narration."
Cloned voices are private to the account and cataloged in the workspace
`Voices/` folder (`index.html` lists each voice with a playable sample).

Poll until done (video tasks take several minutes — frames + audio + encode):

```
GET https://www.getonepress.com/api/v1/conversations/conv_...
Authorization: Bearer $ONEPRESS_API_KEY

→ status "done": answer + preview_path (e.g. "Video/xxx.mp4")
```

When done, download the MP4 and save it to the user's working directory:

```
GET https://www.getonepress.com/api/v1/conversations/conv_.../artifact
Authorization: Bearer $ONEPRESS_API_KEY

→ video/mp4 bytes, Content-Disposition: attachment
```

If `preview_path` is null, fetch by workspace path:
`GET /api/v1/files?path=Projects/.../video.mp4`.

Follow-ups (`POST` same id): "shorter", "different voice", "tighter pacing".

MCP alternative: `https://www.getonepress.com/api/mcp`, tools
`onepress_create_task` / `onepress_task_status` / `onepress_list_tasks` /
`onepress_upload_file` / `onepress_download_artifact` (base64 for file bytes).

## Report back

- `answer` — the agent's summary
- The **local path** where you saved the MP4 (fetched via the artifact
  endpoint); it also lives at https://www.getonepress.com/app (preview/share
  there)
- Conversation id/title

## Errors

401 bad key · 402 out of credits · 409 busy (keep polling) · 429 rate limited.

## Notes

- Be honest: the video is produced on getonepress.com, not here. Never fabricate files or links.
- Never ask the user to paste their API key into chat — env/config only.
