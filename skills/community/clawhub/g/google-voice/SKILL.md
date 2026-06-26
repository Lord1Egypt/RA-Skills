---
name: google-voice
description: Google Voice web-client automation and MCP integration from HAR captures. Use when reverse-engineering voice.google.com.har or call_voice.google.com.har, listing/reading/exporting received Google Voice SMS threads/records from messages URLs or itemId values, sending Google Voice text messages with explicit approval, starting outbound Google Voice calls with explicit approval, injecting approved TTS/local audio into calls, recording call audio, or configuring/using the bundled Google Voice HAR MCP server in OpenClaw.
---

# Google Voice

Use the bundled MCP server for Google Voice web-client calls derived from ~/Downloads/har/voice.google.com.har.

## Safety

- Do not expose HAR cookies, authorization headers, phone numbers, message contents, or anti-abuse tokens.
- Sending SMS and starting outbound calls are external actions. Get explicit user approval for recipient(s)/number and exact message or call intent before acting.
- Prefer browser auth mode so credentials remain inside the logged-in browser session.


## Text messaging support

This skill supports both receiving/reading/exporting Google Voice text message records and sending Google Voice SMS via the HAR-derived MCP tool. Reading/exporting is safe when the user requests their own records. Sending is an external action: confirm the exact recipient(s) and exact message text before calling `gv_send_sms`.

## Pull SMS records from messages URL or itemId

Use the bundled CLI when the user provides a Google Voice messages URL like `https://voice.google.com/u/2/messages?itemId=t.%2B17025038136` or any raw `itemId`/thread id:

    GV_API_KEY='<local-web-api-key>' GV_AUTH_MODE=browser GV_CDP_URL=http://127.0.0.1:19222 node skills/google-voice/scripts/google-voice-sms-records.js --url 'https://voice.google.com/u/2/messages?itemId=t.%2B17025038136' --limit 500 --out /tmp/gv-sms-records.json

Equivalent raw itemId form, with explicit logged-in Google account index when needed:

    node skills/google-voice/scripts/google-voice-sms-records.js --itemId 't.+17025038136' --authuser 1 --format md

For `/u/N` URLs, the script infers `x-goog-authuser=N` unless `GV_AUTHUSER` or `--authuser` is set. It prefers an already-open `voice.google.com/u/N` tab and opens that account-specific URL when no suitable tab exists. It calls `/voice/v1/voiceclient/api2thread/get` in the authenticated browser session and returns normalized records with `id`, `timestampMs`, ISO `timestamp`, `from`, `type`, and `text`. Add `--raw` only when debugging and do not expose raw payloads or SMS contents beyond the user-authorized context.

## Outbound call support

The `call_voice.google.com.har` capture did not expose a stable call-placement API. Use browser/CDP UI automation against the logged-in Google Voice session instead:

    GV_CDP_URL=http://127.0.0.1:19222 node skills/google-voice/scripts/google-voice-start-call.js --number '+1234567890' --authuser 0 --dry-run

After explicit approval for the exact number/call intent, remove `--dry-run` to click the final call button:

    GV_CDP_URL=http://127.0.0.1:19222 node skills/google-voice/scripts/google-voice-start-call.js --number '+1234567890' --authuser 0

For HAR notes, read `references/call-har-endpoints.md`.

### Optional audio-injection call mode

The sanitized local `google-voice-caller` workflow is now integrated here as an optional mode for TTS/local-audio injection and recording. It uses Puppeteer with a private cookie export and never stores cookies in the skill:

    GV_COOKIE_PATH=/private/google_voice_cookies.json skills/google-voice/scripts/google-voice-call-audio.sh --number '+1234567890' --text 'approved message' --duration 60 --authuser 0 --dry-run

After explicit approval for the exact number and exact message/audio, remove `--dry-run`. Use `--audio /path/file.wav` instead of `--text` to inject a local audio file. Dependencies: `puppeteer-core`, Chromium, `ffmpeg`, and `edge-tts` for `--text`.

Prefer the CDP `google-voice-start-call.js` mode for simple manual/live calls because it reuses the logged-in visible browser and avoids cookie exports. Use audio-injection mode only when the user explicitly wants agent-spoken audio or call recording.

## MCP server

Server script:

    node /home/umbrel/.openclaw/workspace-realestate-ops/skills/google-voice/scripts/google-voice-mcp.js

Equivalent source copy:

    node /home/umbrel/.openclaw/workspace-realestate-ops/mcp/google-voice-mcp/server.js

Set `GV_API_KEY` locally from the current Google Voice web session/HAR before calls. Do not write or commit the key.

Default auth mode is browser/CDP:

    GV_API_KEY='<local-web-api-key>' GV_AUTH_MODE=browser GV_CDP_URL=http://127.0.0.1:19222 node skills/google-voice/scripts/google-voice-mcp.js

GWS OAuth mode is available for experiments:

    GV_AUTH_MODE=gws node skills/google-voice/scripts/google-voice-mcp.js

This uses gws auth export locally to refresh an OAuth bearer token. Google Voice web endpoints may still reject it because the captured HAR used browser cookies, not bearer auth. Header auth mode is also available but less safe with GV_COOKIE or GV_AUTHORIZATION.

## Tools exposed

- gv_list_threads: list Google Voice thread summaries.
- gv_get_thread: read a thread by threadId, for example t.22395.
- gv_send_sms: send Google Voice SMS/text messages. Use only after explicit approval for exact recipient(s) and exact message text.
- gv_raw_call: debugging tool for HAR-derived endpoint/body calls.
- Outbound calls: use `scripts/google-voice-start-call.js` for browser/CDP live calls, or `scripts/google-voice-call-audio.sh` for sanitized Puppeteer TTS/audio injection and recording. Call placement is browser UI automation, not a stable HAR RPC yet.

## HAR reverse engineering

To re-summarize endpoints without dumping secrets:

    python3 skills/google-voice/scripts/analyze_voice_har.py ~/Downloads/har/voice.google.com.har

For SMS endpoint notes, read `references/har-endpoints.md`. For call HAR notes, read `references/call-har-endpoints.md`.

## Operating pattern

1. Verify a Google Voice tab/session exists in the user browser, or open https://voice.google.com/ manually/browser tool.
2. Start MCP server in browser mode.
3. List/read threads with MCP tools.
4. For text sends, ask for exact recipient(s) and exact message, then call `gv_send_sms` only after approval.
5. For outbound calls, ask for exact number and call intent. Use `google-voice-start-call.js --dry-run` for live/browser calls, or `google-voice-call-audio.sh --dry-run` for TTS/audio injection. Remove `--dry-run` only after approval.
6. If an API call fails, inspect references and use `gv_raw_call` sparingly.
