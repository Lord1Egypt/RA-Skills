---
name: phone-call
description: Make phone calls through the macOS Phone/FaceTime app and let an OpenClaw agent speak into the call via local TTS.
homepage: https://support.apple.com/guide/phoneapp/make-or-receive-calls-phn28c9d643a/mac
metadata:
  {
    "openclaw":
      {
        "emoji": "📞",
        "os": ["darwin"],
        "requires": { "apps": ["Phone", "FaceTime"], "bins": ["osascript"] },
        "install":
          [
            {
              "id": "iphone-calls",
              "kind": "manual",
              "label": "Enable iPhone Calls: iPhone Settings > Cellular/Phone > Calls on Other Devices, and macOS FaceTime/Phone signed into the same Apple ID",
            },
            {
              "id": "accessibility",
              "kind": "manual",
              "label": "Grant Accessibility permission to the terminal/OpenClaw process that runs the skill",
            },
          ],
      },
  }
---

# Phone Call Skill 📞

Use the macOS Phone/FaceTime stack to start phone calls from an OpenClaw agent. The skill can also speak text into/near the active call using local TTS (`sag`/ElevenLabs when configured, otherwise macOS `say`).

This is useful when you want calls to go out through the MacBook/iPhone Continuity path instead of Twilio/Telnyx/Plivo.

## When to Use

✅ Use this skill when:

- The user asks to call/anrufen/telefonieren from a Mac.
- The user provides a phone number in international/E.164 format.
- An OpenClaw agent should speak a generated sentence into a Mac Phone call.
- You need a local MacBook calling fallback when a cloud telephony provider is unavailable.

❌ Do not use this skill when:

- The user wants SMS/iMessage → use the messaging/iMessage skill.
- The user wants a public telephony bot with inbound calls → use OpenClaw `voice-call` with Twilio/Telnyx/Plivo.
- No explicit permission/number was provided for a live outbound call.

## Setup / Activation

1. **Install the skill**

   ```bash
   clawhub install phone-call
   ```

   Or update an existing install:

   ```bash
   clawhub update phone-call
   ```

2. **Enable iPhone calls on Apple devices**

   - iPhone: Settings → Cellular/Phone → Calls on Other Devices → enable the Mac.
   - Mac: sign into the same Apple ID; open Phone or FaceTime once.
   - Keep iPhone and Mac reachable via Continuity/Wi‑Fi/Bluetooth as required by Apple.

3. **Grant macOS permissions once**

   The process that runs OpenClaw must be allowed to control the UI:

   - System Settings → Privacy & Security → Accessibility → enable Terminal / Warp / OpenClaw runner.
   - System Settings → Privacy & Security → Automation → allow the runner to control System Events and Phone/FaceTime if prompted.

4. **Optional: higher-quality TTS**

   `scripts/speak.sh` uses ElevenLabs `sag` only when an API key is available; otherwise it falls back to `say`.

   ```bash
   export ELEVENLABS_API_KEY="..."
   export PHONE_CALL_TTS_MODEL="eleven_flash_v2_5"
   # optional: export PHONE_CALL_TTS_VOICE="Roger"
   ```

## Commands

### Make a Call

```bash
scripts/call.sh +491234567890
```

Dry run without placing a call:

```bash
scripts/call.sh --dry-run +491234567890
```

Useful options:

```bash
scripts/call.sh --scheme tel +491234567890
scripts/call.sh --scheme tel-phoneapp +491234567890
scripts/call.sh --scheme facetime-audio +491234567890
scripts/call.sh --timeout 15 +491234567890
scripts/call.sh --no-confirm +491234567890
```

### Speak During a Call

```bash
scripts/speak.sh "Ciao, hier ist Luigi. Ich spreche jetzt über das MacBook."
```

`speak.sh` also accepts stdin:

```bash
echo "Kurzer Test über das MacBook." | scripts/speak.sh
```

### Agent Call Wrapper

Start a call, speak an intro, then speak every line from stdin:

```bash
scripts/call-agent.sh +491234567890 --intro "Hallo, ich bin dein OpenClaw Agent."
```

Pipe generated agent text into an already running call:

```bash
printf 'Erster Satz.\nZweiter Satz.\n' | scripts/call-agent.sh --no-call +491234567890
```

## How It Works

- `scripts/call.sh` validates E.164 numbers, opens a macOS phone URL (`tel:` by default), then searches visible Phone/FaceTime/System dialogs for German/English confirmation buttons (`Anrufen`, `Call`, `Fortfahren`, etc.).
- If no confirmation button appears, it continues successfully because recent macOS versions may start the call directly after the user has granted permission.
- `scripts/speak.sh` plays TTS through the active Mac output device. In a normal MacBook/iPhone Continuity call this can be heard through the call path when the call uses Mac audio.
- `scripts/call-agent.sh` combines both pieces for agents: call first, then speak an intro and/or piped text.

## Number Formatting

Use international E.164 format:

- Germany: `+49` + area code/mobile prefix without leading `0`
- Austria: `+43` + area code without leading `0`
- Switzerland: `+41` + area code without leading `0`

Examples:

- Mobile DE: `+4915112345678`
- Landline Berlin: `+493012345678`

## Environment Variables

- `PHONE_CALL_URL_SCHEME` — default URL scheme (`tel`, `tel-phoneapp`, `facetime-audio`, `telephony`). Default: `tel`.
- `PHONE_CALL_CONFIRM_TIMEOUT` — seconds to search/click confirmation UI. Default: `10`.
- `PHONE_CALL_SETTLE_SECONDS` — pause after starting a call before intro speech. Default: `2`.
- `PHONE_CALL_TTS_MODEL` — ElevenLabs model for `sag`. Default: `eleven_flash_v2_5`.
- `PHONE_CALL_TTS_VOICE` — optional ElevenLabs voice name/id.
- `PHONE_CALL_SAY_RATE` — macOS `say` words per minute fallback. Default: `185`.

## Troubleshooting

**Call opens the wrong app (for example Warp):**

- macOS LaunchServices may have reassigned `tel:`. Set `PHONE_CALL_URL_SCHEME=tel-phoneapp` and retry:

  ```bash
  PHONE_CALL_URL_SCHEME=tel-phoneapp scripts/call.sh +491234567890
  ```

**Confirmation is not clicked:**

- Re-check Accessibility/Automation permissions for the actual process running the skill (Terminal, Warp, OpenClaw, or the gateway service).
- Retry with a longer timeout:

  ```bash
  scripts/call.sh --timeout 20 +491234567890
  ```

**No speech in the call:**

- Confirm the Mac call is using Mac audio, not only the iPhone handset.
- Test local playback:

  ```bash
  scripts/speak.sh "Audio test"
  ```

- Select the intended output device in macOS Control Center/Sound settings.
- For clean two-way telephony audio, prefer the official OpenClaw `voice-call` plugin with realtime media, or add virtual audio routing (for example BlackHole) plus STT.

**ElevenLabs fails:**

- Set `ELEVENLABS_API_KEY`/`ELEVENLABS_API_KEY_FILE`, or let the helper fall back to macOS `say`.

## Safety Notes

- Do not place live calls without explicit user permission and a confirmed number.
- The call may be visible on the Mac screen and in Phone/FaceTime recents.
- This skill controls local UI; macOS permissions are required and should not be bypassed.
