---
name: llc-phone
description: >-
  Low-latency inbound and outbound AI phone calls via the OpenAI Realtime API
  and Twilio, covering pre-warm and pre-accept patterns, IVR and receptionist
  flows, customer-service routing, VAD tuning, function calling, prompt
  caching, and implementation caveats.
user-invocable: true
homepage: https://promethean-dynamic.com
metadata: {"openclaw":{"emoji":"📞","homepage":"https://promethean-dynamic.com","requires":{"env":["OPENAI_API_KEY","TWILIO_ACCOUNT_SID","TWILIO_AUTH_TOKEN","TWILIO_PHONE_NUMBER"]},"primaryEnv":"OPENAI_API_KEY"}}
---

# Lowest Latency Calls

Architecture, configuration, and reference for the OpenAI Realtime API + Twilio phone system.

**To PLACE calls, manage prospects, and run campaigns**: pair this skill with your own outbound dialer / campaign layer. This skill is about the real-time call infrastructure itself.

## DO NOT CHANGE (confirmed working, breaks if altered)

The call flow, session config format, and audio path below were debugged through many iterations. Do not restructure without reading this entire skill.

### Session config — FLAT format only
```javascript
// CORRECT:
{ type: "session.update", session: {
    modalities: ["text", "audio"], voice: "cedar",
    turn_detection: { type: "semantic_vad", eagerness: "high", create_response: true, interrupt_response: true },
    input_audio_format: "g711_ulaw", output_audio_format: "g711_ulaw",
}}
// WRONG (API rejects): session: { type: "realtime", audio: { input: { format: ... } } }
```

### Outbound call flow — caller-first
Callee picks up, says hello, THEN the agent responds. No forced greeting. Semantic VAD with `create_response: true` handles it automatically.

### Audio path — direct passthrough
Audio deltas from OpenAI are already base64 g711_ulaw. Forward directly to Twilio. No PCM conversion, no gain control, no resampling.

### Greeting trigger
`conversation.item.create` (user message) + `response.create`. NOT `response.create` with instructions. Trigger on `session.updated`, NOT `session.created`.

### Twilio webhook
Must point to `/twiml`. Verify: check Twilio API, not assumptions.

## SAFE TO TUNE

- **Prompt size**: smaller = faster inference. Reference outbound prompt is ~478 tokens.
- **VAD eagerness**: `"high"` first turn, `"medium"` after. Configurable.
- **Tool loading**: lean tools first turn, full set after first `response.done`.
- **Voice**: cedar is a solid default for all scenarios. Can change per scenario.
- **Inference priming**: text-only `response.create` during pre-warm warms pipeline without audio.
- **Twilio edge**: configure to colocate with your deployment region and OpenAI region for lowest RTT.

## Debugging Checklist

Before adding patches when calls fail:
1. Is the websocket server process running? (`systemctl status <your-service>`, `pm2 status`, or your equivalent)
2. Single owner on the websocket port? `lsof -i :<PORT>`
3. Twilio webhook URL correct? Check the Twilio API, not local config files.
4. Check your server log (whatever path you configured — stdout, file, or journald)
5. OpenAI outage? Check status.openai.com
6. Session config accepted? Look for `session.updated` in logs. `error` after `session.created` = wrong config format.

Do not pile patches. If it worked before and doesn't now, check infrastructure first.

## Restart Procedure (pattern)

Whatever process supervisor you use, the correct sequence is:

```
stop the websocket server
→ kill any orphaned listeners on the websocket port (lsof -i :<PORT> -t | xargs kill)
→ start the websocket server
```

Always stop → kill orphans → start. A bare restart can leave a stale listener holding the port.

## Restore from Snapshot (pattern)

Keep a known-good copy of `sessionManager.ts` (the file most affected by tuning) in a snapshots directory alongside the source. To restore:

```
copy snapshots/sessionManager-TUNED-<date>.ts → src/sessionManager.ts
restart using the procedure above
```

## Key Files (relative to the websocket-server project)

| What | Path |
|---|---|
| sessionManager.ts | `websocket-server/src/sessionManager.ts` |
| server.ts | `websocket-server/src/server.ts` |
| Snapshots | `websocket-server/snapshots/` |
| Service unit | your process supervisor unit file (systemd user unit, pm2 ecosystem file, etc.) |
| Logs | wherever you configured (stdout + journald, `/var/log/...`, pm2 logs, etc.) |
| .env | `websocket-server/.env` (contains `PORT`) |

## Reference Documents

All reference docs in `{baseDir}/docs/`:

| File | Content |
|---|---|
| `{baseDir}/docs/01-overview.md` | Model landscape, changelog |
| `{baseDir}/docs/02-session-config.md` | session.update reference + defaults |
| `{baseDir}/docs/03-prewarm-outbound.md` | Pre-warm: buffer, fallback, edge cases |
| `{baseDir}/docs/04-inbound-modes.md` | AI IVR, Receptionist, CSR with DB |
| `{baseDir}/docs/05-async-tools.md` | Async tool calling |
| `{baseDir}/docs/06-latency-tuning.md` | All latency levers |
| `{baseDir}/docs/07-twilio-integration.md` | PCMU format, edge, AMD, stream events |
| `{baseDir}/docs/08-known-issues.md` | Bugs, workarounds, watch-later |
| `{baseDir}/docs/09-openclaw-config.md` | Config + install/publish |

Load the relevant doc before answering architecture or config questions.

## Key Facts (always available without file load)

- Model: `gpt-realtime-1.5` (flagship), `gpt-realtime-mini` (cost-sensitive)
- WebSocket: `wss://api.openai.com/v1/realtime?model=gpt-realtime-1.5`
- Audio: mu-law / PCMU at 8 kHz mono, base64 encoded
- Turn detection: `semantic_vad` with `eagerness: "high"` is the tested default
- Pre-warm timeout: 10 seconds (fallback to cold connect)

## Lessons

1. Session config: flat format only. Nested is rejected.
2. Trigger greeting on `session.updated`, not `session.created`.
3. Semantic VAD works without prior audio response.
4. Verify infrastructure before debugging behavior.
5. Audio is already PCMU. No conversion needed.
6. Prompt size directly affects per-turn latency.
7. When patches pile up: stop, read docs, rewrite from baseline.
