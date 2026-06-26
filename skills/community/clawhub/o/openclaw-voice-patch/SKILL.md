---
name: openclaw-voice-patch
description: Patch OpenClaw Control UI to add hold-for-continuous voice input (single button: short click = auto-send, hold 3s = continuous mode). Use when OpenClaw voice input needs patching, after OpenClaw updates (patches are overwritten by every update and must be re-applied), or when asked about voice input fixes. If the agent cannot access the OpenClaw installation files (permission denied or outside workspace), it will ask the user to copy the files into the workspace for patching, then copy them back.
---

# OpenClaw Voice Input Patch

Adds smart voice input to the Control UI chat — same one mic button, but with hold-to-activate.

## What This Does

**Before:** One mic button. Speak → text appears → must press Enter manually.

**After:** Same one mic button — but smarter, with hold-to-activate:
- **Short click** → Auto-send: mic activates, speak, on pause text is sent automatically, mic turns off. If you say nothing for ~3 seconds, the mic auto-stops (browser SpeechRecognition timeout) — acts as a natural "misclick" safeguard.
- **Hold 3 seconds** → Continuous mode: mic stays on after each message. After every speech pause, text is sent and recognition restarts. Click again to stop.
- **Live interim transcript** shown above the input field while either mode is active.
- Tooltip adapts: `"Voice (hold 3s for continuous)"` when idle, `"Stop voice auto"` or `"Stop voice continuous"` when recording.

**Note:** If the browser shows "microphone denied" errors, the `microphone=(self)` Permissions-Policy fix is also needed. This was merged into OpenClaw on April 18, 2026 — if you're on version 2026.4.18+, it's already included. On older versions, see the Troubleshooting section.

## Step 1: Find the file

There is exactly one file to patch. It's always at:
```
.../openclaw/dist/control-ui/assets/index-<hash>.js
```

The hash in the filename changes with every OpenClaw version. Find it with:

**Linux / Mac:**
```bash
find / -path "*/openclaw/dist/control-ui/assets/index-*.js" 2>/dev/null | head -1
```

**Windows (PowerShell):**
```powershell
Get-ChildItem -Path C:\ -Recurse -Filter "index-*.js" -ErrorAction SilentlyContinue | Where-Object { $_.FullName -match "openclaw\\dist\\control-ui\\assets" } | Select-Object -First 1 -ExpandProperty FullName
```

**Quick alternative:** Run `npm root -g` to find the global node_modules path, then look inside for `openclaw/dist/control-ui/assets/index-*.js`.

If you (the AI agent) cannot find or access the file, tell the user:

> "I couldn't access the OpenClaw Control UI file. Can you help? Either:
> 1. Copy the file into my workspace so I can patch it, then copy it back after. Run this in your terminal:
>    `cp /path/to/openclaw/dist/control-ui/assets/index-*.js ~/.openclaw/workspace-allgemein/`
> 2. Or give me write access:
>    `sudo chown -R $(whoami) /path/to/openclaw/dist/`"

Keep it simple. Don't over-explain.

## Step 2: Back up

```bash
cp <path-to-index-file> <path-to-index-file>.bak
```

## Step 3: Verify compatibility

Before patching, confirm these patterns exist in the file. If any are missing, the OpenClaw version has changed — do NOT proceed. Instead, inspect the file and adapt, or wait for an updated version of this skill.

| Pattern | What it is |
|---|---|
| `function NC(e)` | Speech recognition start function |
| `sttRecording` | Recording state variable |
| `N.micOff` | Mic-off icon reference |
| `jC()` | Speech recognition availability check |

## Step 4: Add sttRecordingCont state variable

**Find** this exact text:

```
sttRecording:!1,sttInterimText
```

**Replace** with:

```
sttRecording:!1,sttRecordingCont:!1,sttInterimText
```

This appears exactly once in the file.

**Verify:** Search for `sttRecordingCont:!1` — must appear exactly once.

## Step 5: Show interim text for both recording states

**Find** this exact text:

```
${X.sttRecording&&X.sttInterimText?i`<div class="agent-chat__stt-interim">${X.sttInterimText}</div>`:h}
```

**Replace** with:

```
${(X.sttRecording||X.sttRecordingCont)&&X.sttInterimText?i`<div class="agent-chat__stt-interim">${X.sttInterimText}</div>`:h}
```

This appears exactly once in the file.

**Verify:** Search for `(X.sttRecording||X.sttRecordingCont)` — must appear in the line containing `stt-interim`.

## Step 6: Replace single mic button with hold-for-continuous button

This is the most complex patch. Replace the ENTIRE mic button block with a single button that supports both short-click (auto-send) and hold-3s (continuous) modes.

### 6.1 Find the block

Search for the text `Stop recording` or `Voice input` in the file. This is inside the mic button template.

The block to replace starts at `${jC()?i`` and ends at ``:h}` — both on the same line as `Stop recording`/`Voice input`, or on the lines immediately surrounding it.

It contains exactly ONE `<button>` element with:
- `class` containing `agent-chat__input-btn`
- `@click` handler referencing `X.sttRecording` and `NC({`
- `title` with `Stop recording` / `Voice input`
- `N.micOff` and `N.mic` for the icon

### 6.2 Replace the entire block

**Select everything from `${jC()?i`` through ``:h}` inclusive and replace it with:**

```
${jC()?i`
                  <button
                    class="agent-chat__input-btn ${(X.sttRecording||X.sttRecordingCont)?`agent-chat__input-btn--recording`:``}"
                    @mousedown=${(t)=>{if(X.sttRecording||X.sttRecordingCont)return;t.preventDefault();X._holdTimer=setTimeout(()=>{X._holdTimer=null;X._holdTriggered=!0;NC({onTranscript:(t,n)=>{if(n){let n=_(),r=n&&!n.endsWith(` `)?` `:``;e.onDraftChange(n+r+t),X.sttInterimText=``,e.onSend()}else X.sttInterimText=t;g()},onStart:()=>{X.sttRecordingCont=!0;window.__sttCont=MC;g()},onEnd:()=>{if(X.sttRecordingCont){let r=window.__sttCont;if(r){try{r.start()}catch(e){}}X.sttInterimText=``,g()}else{X.sttInterimText=``,g()}},onError:()=>{X.sttRecordingCont=!1,X.sttInterimText=``,g()}})&&(X.sttRecordingCont=!0,g())},3000)}}
                    @mouseup=${(t)=>{if(X._holdTimer){clearTimeout(X._holdTimer);X._holdTimer=null;if(!X._holdTriggered){NC({onTranscript:(t,n)=>{if(n){let n=_(),r=n&&!n.endsWith(` `)?` `:``;e.onDraftChange(n+r+t),X.sttInterimText=``,e.onSend(),PC(),X.sttRecording=!1}else X.sttInterimText=t;g()},onStart:()=>{X.sttRecording=!0;if(MC)MC.continuous=!1;g()},onEnd:()=>{X.sttRecording=!1,X.sttInterimText=``,g();const d=_();if(d&&d.trim())e.onSend()},onError:()=>{X.sttRecording=!1,X.sttInterimText=``,g()}})&&(X.sttRecording=!0,g())}}X._holdTriggered=!1}}
                    @click=${()=>{if(X.sttRecordingCont){PC(),X.sttRecordingCont=!1,window.__sttCont=null,X.sttInterimText=``,g()}}}
                    title=${X.sttRecordingCont?`Stop voice continuous`:(X.sttRecording?`Stop voice auto`:`Voice (hold 3s for continuous)`)}
                    ?disabled=${!e.connected}
                  >
                    ${(X.sttRecording||X.sttRecordingCont)?N.micOff:N.mic}
                  </button>
                `:h}
```

**Do NOT** replace individual pieces. Replace the ENTIRE block as a single unit.

**Note for the `edit` tool:** Escape `<` → `\u003c`, `>` → `\u003e`, `&` → `\u0026` in the replacement text.

### 6.3 How it works

**mousedown** starts a 3-second timer:
- If **mouseup before 3s** → timer cancelled, short click → auto-send mode starts (one-shot, `continuous=false`, auto-send + auto-stop on final transcript or silence)
- If **timer fires after 3s** → continuous mode starts (mic stays on, `onEnd` restarts recognition via `window.__sttCont.start()`, text auto-sent after each pause)

**click** (separate from mousedown/mouseup): If already in continuous mode, stops it (`PC()` + clear `window.__sttCont`).

**Auto-send mode** also auto-stops if the user says nothing for ~3 seconds — the browser's SpeechRecognition fires `onEnd` after silence when `continuous=false`, which acts as a natural "misclick" safeguard.

### 6.4 Verify

Search the file for ALL of these strings — every single one must be present:

- [ ] `sttRecordingCont` — appears multiple times
- [ ] `_holdTimer` — hold timer variable
- [ ] `_holdTriggered` — hold flag
- [ ] `Voice (hold 3s for continuous)` — idle tooltip
- [ ] `Stop voice auto` — auto-send active tooltip
- [ ] `Stop voice continuous` — continuous active tooltip
- [ ] `window.__sttCont` — continuous restart mechanism
- [ ] `MC.continuous=!1` — one-shot mode flag

If any are missing, restore from backup and retry from step 6.2.

## Step 7: Restart and verify

Tell the user:

1. **Restart the gateway** (e.g. `openclaw gateway restart`)
2. **Hard-refresh the browser** with Ctrl+Shift+R (normal refresh is NOT sufficient — the browser caches the old JS file)

After the user has done both, verify:
1. One mic button with tooltip "Voice (hold 3s for continuous)"
2. Short click → speak → pause → message sent automatically → mic off
3. Short click → say nothing → mic auto-stops after ~3 seconds
4. Hold button 3 seconds → continuous mode activates (tooltip changes to "Stop voice continuous")
5. In continuous mode: speak → pause → message sent → mic stays on → speak again → sent → ...
6. Click button in continuous mode → mic stops
7. Live transcript appears above input field while mic is active

## Rollback

If anything goes wrong: `cp <path-to-index-file>.bak <path-to-index-file>` and tell the user to restart the gateway.

## Troubleshooting

| Problem | Likely Cause | Fix |
|---|---|---|
| No mic button at all | Browser doesn't support Web Speech API | Use Chrome or Edge |
| Button appears but does nothing on click | Step 6 not applied or partial | Restore backup, re-apply Step 6 |
| Short click starts mic but doesn't auto-send | `e.onSend()` missing in @mouseup handler | Restore backup, re-apply Step 6 |
| Short click mic stays on after pause | `PC()` or `sttRecording=!1` missing | Restore backup, re-apply Step 6 |
| Hold 3s doesn't start continuous mode | `_holdTimer` / `_holdTriggered` not working | Restore backup, re-apply Step 6 |
| Continuous mode stops after silence | `onEnd` restart logic not working | Check `window.__sttCont` and `__sttCont.start()` in Step 6 replacement |
| Live transcript not showing | Step 5 not applied | Apply Step 5 |
| "Microphone denied" in browser | Permissions-Policy blocks mic | Fix `microphone=()` → `microphone=(self)` in the HTTP utils file (included in OpenClaw 2026.4.18+) |
| After OpenClaw update | Patches overwritten | Re-apply ALL steps (filename hash changes!) |