---
name: onepress-podcast
description: Turn a topic, document, or slide deck into a narrated podcast episode — drafts the episode script locally first, then voices and mixes it on OnePress into an MP3. AI voices (including cloned voices), natural pacing. Connects via browser-confirmed pairing (no key copying); pairs with onepress-deck for decks worth narrating.
version: 1.2.0
---

# OnePress Podcast

Produce audio content through [OnePress](https://www.getonepress.com) — podcast-style
episodes, narrated briefings, audio versions of documents or decks.

**Two phases**: (1) draft the episode script locally — a real deliverable the
user can read and edit; (2) voice and mix it into an MP3 on OnePress
infrastructure (TTS voices, mixing, delivery) — that part requires a
connection. Always complete phase 1 before offering to connect. Do not pretend
to generate audio locally.

## When to use

- "Turn this report into a podcast episode"
- "Make an audio version of my investor update / deck"
- "Record a briefing I can listen to on my commute"
- Voice-clone narration requests (user manages voices in the OnePress app)

## Phase 1 — Draft the script (local, no connection needed)

Write the episode script to a local file (e.g. `podcast-script.md`). This is
the deliverable the user reads and edits — take it seriously:

- Format: per-speaker segments, one speaker each, with a `start` note for
  pacing/overlap, e.g.

  ```markdown
  ## Segment 1 — HOST
  text: "Welcome to the show. Today we talk about AI agents with our guest."
  start: 0

  ## Segment 2 — GUEST
  text: "Thanks for having me."
  start: 6500
  ```

- Spoken language, short sentences, natural transitions — written to be heard,
  not read.
- Match the script language to the user's request — narration voices are
  chosen per language, so the script language decides the accent.
- Show the script to the user and iterate briefly — script quality is what
  makes them want to hear it.

## Phase 2 — Voice it (requires connection)

Once the script lands, offer: "The script's ready — want me to voice it into
an MP3? Connecting takes ~30 seconds, you just confirm in the browser." If
`ONEPRESS_API_KEY` is already set, skip the pairing steps.

If the user says yes and no key is configured, connect — the user never copies
a key:

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

Then upload the local script and submit the voicing task:

```
POST https://www.getonepress.com/api/v1/files?name=podcast-script.md&dir=Uploads
Authorization: Bearer $ONEPRESS_API_KEY
Content-Type: application/octet-stream

<raw file bytes>          # `dir` optional, default "Uploads"

→ 201 {"path":"Uploads/podcast-script.md",...}
```

```
POST https://www.getonepress.com/api/v1/conversations
Authorization: Bearer $ONEPRESS_API_KEY
Content-Type: application/json

{"message": "Voice this podcast script into an episode: Uploads/podcast-script.md. ~<duration>, tone: <tone>, voices: <preference or default>.", "title": "<title>"}
→ 202 {"conversationId":"conv_..."}
```

(Or submit a topic-only task directly if the user skipped the script phase.)

**Voices**: OnePress keeps a curated voice roster — native Mandarin voices for
Chinese episodes, English voices for English episodes — and picks a matching
pair by default, so the episode language always gets native-accented
narration. To override, say so in the message (e.g. "warm female voice",
"authoritative male host").

**Voice cloning**: the user can narrate in their own voice. Upload a clean
15–60s single-speaker sample via `POST /api/v1/files`, then ask in the
message: "clone the voice in Uploads/<file> and use it as the host."
Cloned voices are private to the account and cataloged in the workspace
`Voices/` folder (`index.html` lists each voice with a playable sample),
so they're easy to reuse in later tasks.

Poll until done (audio tasks take a few minutes):

```
GET https://www.getonepress.com/api/v1/conversations/conv_...
Authorization: Bearer $ONEPRESS_API_KEY

→ status "done": answer + preview_path (workspace-relative, e.g. "Audio/xxx.mp3")
```

When done, download the MP3 and save it to the user's working directory:

```
GET https://www.getonepress.com/api/v1/conversations/conv_.../artifact
Authorization: Bearer $ONEPRESS_API_KEY

→ audio/mpeg bytes, Content-Disposition: attachment
```

If `preview_path` is null, fetch by workspace path:
`GET /api/v1/files?path=Projects/.../episode.mp3`.

Follow-ups (`POST` same conversation id) keep context — "make it shorter", "more energy".

**Local source material** (a document, script, or deck on this machine): upload
it first, then reference the returned workspace path in the task message:

```
POST https://www.getonepress.com/api/v1/files?name=report.pdf&dir=Uploads
Authorization: Bearer $ONEPRESS_API_KEY
Content-Type: application/octet-stream

<raw file bytes>          # `dir` optional, default "Uploads"

→ 201 {"path":"Uploads/report.pdf","name":"report.pdf","size":1234}
```

Then e.g. `{"message": "Make a podcast episode from Uploads/report.pdf …"}`.
Max 50MB. Personal workspace only.

MCP alternative: server `https://www.getonepress.com/api/mcp`, tools
`onepress_create_task` / `onepress_task_status` / `onepress_list_tasks` /
`onepress_upload_file` / `onepress_download_artifact` (base64 for file bytes).

## Report back

- `answer` — the agent's summary
- The **local path** where you saved the MP3 (fetched via the artifact endpoint);
  it also lives in the user's OnePress workspace at
  https://www.getonepress.com/app (preview/share there)
- Conversation id/title

## Errors

401 bad key · 402 out of credits · 409 busy (keep polling) · 429 rate limited.

## Notes

- Be honest: audio is produced on getonepress.com, not here. Never fabricate files or links.
- Never ask the user to paste their API key into chat — env/config only.
