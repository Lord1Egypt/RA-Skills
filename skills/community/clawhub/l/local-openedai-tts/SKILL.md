---
name: local-openedai-tts
description: Configure an OpenClaw instance to use a local OpenAI-compatible TTS backend (for example openedai-speech) with cloned voices. Use when users ask to wire local TTS, set OpenClaw to use local speech synthesis, verify voice/model mapping, generate test clips, troubleshoot wrong voice/model selection, or expose the local TTS endpoint to LAN/Tailscale.
---

# Local OpenAI-Compatible TTS for OpenClaw

Configure OpenClaw to send TTS requests to a local OpenAI-compatible endpoint, then verify end-to-end delivery.

## Quick workflow

1. Set OpenAI base URL to local endpoint.
2. Configure OpenClaw messages TTS provider/model/voice.
3. Verify TTS config with `openclaw config get`.
4. Generate a direct API sample clip to confirm voice mapping.
5. Send sample via channel plugin (Telegram/WhatsApp/etc.) if requested.
6. If remote access is requested, expose the TTS service port (not necessarily the OpenClaw gateway).

## 1) Configure OpenClaw to use local TTS backend

Use CLI config commands only.

```bash
openclaw config set env.vars.OPENAI_BASE_URL http://127.0.0.1:19000/v1
openclaw config set messages.tts.provider openai
openclaw config set messages.tts.openai.model tts-1-hd
openclaw config set messages.tts.openai.voice me
```

Verify:

```bash
openclaw config get env.vars.OPENAI_BASE_URL
openclaw config get messages.tts
```

## 2) Verify cloned voice exists on backend

If using openedai-speech + XTTS voice mapping, cloned voices are commonly available only on `tts-1-hd`.

Check voice map inside container:

```bash
sudo docker exec openedai-speech sh -lc 'sed -n "1,220p" /app/config/voice_to_speaker.yaml'
```

If `voice: me` fails with `KeyError`, check whether:
- wrong model is used (`tts-1` instead of `tts-1-hd`), or
- voice key missing from `voice_to_speaker.yaml`.

## 3) Generate a deterministic test clip (direct API)

Use direct POST to validate backend behavior independent of chat surface rendering.

```bash
curl -sS -X POST http://127.0.0.1:8880/v1/audio/speech \
  -H 'Content-Type: application/json' \
  -d '{
    "model":"tts-1-hd",
    "voice":"me",
    "input":"Quick cloned voice check.",
    "speed":1.25,
    "response_format":"mp3"
  }' \
  --output /tmp/clone-test.mp3

file /tmp/clone-test.mp3
```

Expected: MP3 audio file (not JSON error text).

## 4) Important limitation: speed pinning in OpenClaw config

`messages.tts.openai.speed` may be rejected by current OpenClaw schema. If so:
- keep model/voice in OpenClaw config,
- set speed per request when generating clips directly,
- or enforce speed with a local proxy layer in front of backend.

Do not claim speed is globally pinned unless schema accepts it.

## 5) Expose service correctly (LAN/Tailscale)

Distinguish between:
- **OpenClaw gateway exposure** (`gateway.bind`, `gateway.tailscale.*`), and
- **TTS backend exposure** (container/service port such as `19000` or `8880`).

If user asks to expose local TTS only, do not change gateway bind/mode unless explicitly requested.

For TTS backend reachability:
1. Confirm listener/bind:
   ```bash
   ss -ltnp | grep ':19000\|:8880'
   ```
2. If bound to `127.0.0.1`, rebind service/container to `0.0.0.0` or tailnet interface.
3. Restrict access via firewall/Tailscale ACLs.

## 6) Channel delivery troubleshooting

If webchat does not play voice attachments:
- send as regular file attachment to supported channel (e.g., Telegram),
- verify target id explicitly,
- confirm local file still exists before sending.

If file missing, regenerate clip and resend.

## Command safety

- Use `openclaw config set/get` (never edit `openclaw.json` directly).
- Avoid unrelated gateway changes when task is strictly TTS service exposure.
- For external sends, use channel tools and explicit target ids.
