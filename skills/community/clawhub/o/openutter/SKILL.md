---
name: open-utter
description: Headless Google Meet bot that joins meetings and captures live captions as transcripts.
homepage: https://github.com/sumansid/openutter
metadata: { "openclaw": { "emoji": "🦦", "requires": { "bins": ["node"] } } }
---

# OpenUtter

## STOP — Ask the user before doing anything

**When the user asks to join a meeting, you MUST do these steps IN ORDER. Do NOT skip ahead.**

**Step A:** Read the file `~/.openutter/auth-meta.json` (it may not exist — that's fine).

**Step B:** Ask the user how they want to join. Do NOT launch the bot yet.

If auth-meta.json exists and has an `email` field, ask:

> "How would you like to join the meeting?
> 1. Join as **user@gmail.com** (authenticated — no host approval needed)
> 2. Join as **OpenUtter Bot** (guest — host must admit)
> 3. Join with a custom name (guest)"

If auth-meta.json does NOT exist, ask:

> "What name should the bot use to join the meeting?"

Default to "OpenUtter Bot" if the user doesn't have a preference.

**Step C:** WAIT for the user to answer. Only then launch the bot with the right flags.

- User chose authenticated → use `--auth`
- User chose guest → use `--anon --bot-name "Their Name"` (always ask for a name)

**The bot will refuse to start without `--auth` or `--anon`.
When using `--anon`, `--bot-name` is also required.**

---

A meeting bot that joins Google Meet meetings via Playwright browser automation
and captures live captions as a real-time transcript.

## Prerequisites

- `playwright-core` (ships with openclaw)
- Chromium browser: `npx playwright-core install chromium`

## Join a Meeting

**IMPORTANT: Always run these commands with `background:true`** — the bot is a long-running
process that stays in the meeting. Do not wait for it to complete; background it immediately
and poll for status updates.

### Launch command

```bash
exec background:true command:"npx tsx skills/openutter/scripts/utter-join.ts https://meet.google.com/abc-defg-hij --auth|--anon --channel <current-channel> --target <current-chat-id>"
```

**IMPORTANT:** Always pass `--channel` and `--target` from the current conversation context.
The bot uses these to send screenshots and status images directly to the user's chat.

Options (required — bot will error without one):

- `--auth` — join using saved Google account (~/.openutter/auth.json)
- `--anon --bot-name "Name"` — join as a guest with this display name (both required together)

Other options:

- `--headed` — show the browser window (for debugging)
- `--camera` — join with camera on (default: off)
- `--mic` — join with microphone on (default: off)
- `--duration 60m` — auto-leave after duration (supports ms/s/m/h)

## Live Caption Transcript

Captions are automatically captured whenever the bot is in a meeting. After joining,
the bot enables Google Meet's built-in live captions and captures the text via a
MutationObserver. Captions are deduplicated (Meet updates word-by-word) and flushed
to a transcript file every 5 seconds.

**Transcript location:** `~/.openclaw/workspace/openutter/transcripts/<meeting-id>-<YYYY-MM-DD>.txt`

**Format:**
```
[14:30:05] Alice: Hey everyone, let's get started
[14:30:12] Bob: Sounds good, I have the updates ready
[14:30:25] Alice: Great, go ahead
```

When the meeting ends, the bot prints `[OPENUTTER_TRANSCRIPT] <path>` with the transcript file path.

## Get Transcript (what are they saying?)

**When the user asks "what are they saying?", "what's happening?", "summarize the meeting",
or anything about meeting content — run this script. Do NOT use utter-screenshot.ts for this.**

```bash
exec command:"npx tsx skills/openutter/scripts/utter-transcript.ts"
```

Use `--last 20` to get only the last 20 lines (for long meetings).

Read the output and summarize it for the user in natural language.

## Take a Screenshot (visual context only)

If the user asks to **see** the meeting (e.g. "send me a screenshot", "what does it look like"):

```bash
exec command:"npx tsx skills/openutter/scripts/utter-screenshot.ts"
```

Send the screenshot image to the user via `message`. Do NOT read the screenshot yourself.

## How It Works

1. **Join**: Launches headless Chromium, navigates to the Meet URL, enters the bot name, clicks "Ask to join", and waits for the host to admit it.

2. **Caption capture**: After joining, the bot clicks the CC button to enable Google Meet's live captions, then injects a MutationObserver to capture caption text from the DOM. Captions are deduplicated (partial word-by-word updates are ignored) and flushed to a transcript file every 5 seconds.

## Authentication (Optional)

By default the bot joins as a guest and needs host admission. To join as an authenticated
Google user (no admission needed), run the auth script once:

```bash
npx tsx skills/openutter/scripts/utter-auth.ts
```

This opens a headed browser — sign into Google, then press Enter. The session is saved to
`~/.openutter/auth.json` and automatically loaded on future joins. Re-run if the session expires.

## Files

- `~/.openutter/auth.json` — saved Google session (cookies + localStorage, from utter-auth.ts)
- `~/.openutter/chrome-profile/` — persistent Chromium profile (used when no auth.json)
- `~/.openutter/config.json` — bot configuration (optional)
- `~/.openclaw/workspace/openutter/transcripts/` — live caption transcripts
- `~/.openclaw/workspace/openutter/on-demand-screenshot.png` — on-demand screenshot from a running meeting
- `~/.openclaw/workspace/openutter/debug-join-failed.png` — screenshot on join failure
- `~/.openclaw/workspace/openutter/debug-admit-failed.png` — screenshot on admission failure
- `~/.openclaw/workspace/openutter/joined-meeting.png` — confirmation screenshot after joining

## Headless VM Tips

- Chrome flags `--use-fake-ui-for-media-stream` and `--use-fake-device-for-media-stream` are set automatically, so no real camera/mic hardware is needed.
- No X11/Wayland display is required — runs fully headless.
- Use `--duration` to auto-leave after a set time.

## Agent Behavior — MANDATORY

After launching the bot with `exec background:true`, you MUST poll the process
to check for success/failure and send screenshots back to the user.

### Step 1: Poll for output

After starting the background exec, poll the process every 10–15 seconds:

```
process action:poll
```

### Step 2: Parse markers and send images using the message tool

The bot prints machine-readable markers. When you see them, you MUST use the
`message` tool to send the screenshot image to the user.

**On success** — bot prints `[OPENUTTER_SUCCESS_IMAGE] <path>`:

```
message action:"send" media:"./openutter/joined-meeting.png" content:"Successfully joined the meeting!"
```

**On screenshot request** — bot prints `[OPENUTTER_SCREENSHOT] <path>`:

```
message action:"send" media:"./openutter/on-demand-screenshot.png" content:"Here's the current meeting view"
```

**On failure** — bot prints `[OPENUTTER_DEBUG_IMAGE] <path>` (or exits non-zero):

```
message action:"send" media:"./openutter/debug-join-failed.png" content:"Could not join the meeting. Here is what the bot saw"
```

**CRITICAL: ALWAYS use the `message` tool with `media:"./openutter/<filename>.png"` to send screenshots.**
Use relative paths only (starting with `./`). Never use absolute paths or ~ paths.
NEVER just describe what happened in text. The user MUST receive the actual image.

**When the user asks "send me screenshot" or "what do you see"**, run
`utter-screenshot.ts`, then use the `message` tool with `media:"./openutter/on-demand-screenshot.png"`.

### Step 3: When user asks about meeting content

**CRITICAL: When the user asks what's happening, what someone said, or anything about
meeting content — run `utter-transcript.ts`. NEVER use `utter-screenshot.ts` for this.**

```bash
exec command:"npx tsx skills/openutter/scripts/utter-transcript.ts"
```

Read the output and summarize it for the user. Use `--last 20` for long meetings.

**On meeting end** — bot prints `[OPENUTTER_TRANSCRIPT] <path>`:
Run `utter-transcript.ts` and provide a summary to the user.

### When to use which script

| User asks...                              | Use this script          |
|-------------------------------------------|--------------------------|
| "what are they saying?"                   | `utter-transcript.ts`    |
| "what's happening in the meeting?"        | `utter-transcript.ts`    |
| "summarize the meeting"                   | `utter-transcript.ts`    |
| "what did they talk about?"               | `utter-transcript.ts`    |
| "send me a screenshot"                    | `utter-screenshot.ts`    |
| "what does the meeting look like?"        | `utter-screenshot.ts`    |

**NEVER read or analyze screenshot images to understand meeting content.**

### Screenshot files

- `~/.openclaw/workspace/openutter/joined-meeting.png` — confirmation screenshot after joining
- `~/.openclaw/workspace/openutter/debug-join-failed.png` — join button not found
- `~/.openclaw/workspace/openutter/debug-admit-failed.png` — not admitted / blocked / timed out

## Troubleshooting

- **Join button not found**: Google Meet UI changes occasionally. The debug screenshot shows what the bot saw — send it to the user.
- **Not admitted**: The bot joins as a guest and needs host approval. Ask the host to admit "OpenUtter Bot". If timed out, the debug screenshot is sent automatically.
- **No captions captured**: The CC button selector may change with Meet updates. If the transcript is empty, captions may not have been enabled. Try `--headed` to verify the CC button is clicked.
- **Headless blocked**: The bot uses stealth patches to bypass headless detection. If Google Meet blocks it, try `--headed` for debugging.
