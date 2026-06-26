# Creating Great Videos with Pagerunner

**Load this doc when** you're recording a tab for a bug repro, feature demo, onboarding tutorial, or any other asset where the *quality* of the recording matters. If you just need the tool signatures, REFERENCE.md → [Video Recording](REFERENCE.md#video-recording-7-tools) is enough.

Pagerunner's recording pipeline (v0.8.0+) is not a naive screen grab. It captures at 10 fps, renders at 30 fps with motion interpolation, and can post-process with auto-zoom, cursor choreography, markers, window chrome, and SRT subtitles. The output is meant to compete with Screen Studio — but only if you *drive the session like a director*. This doc is the director's guide.

---

## Prerequisites

- `ffmpeg` on PATH (required).
- `ImageMagick` (`convert`) for burned-in text overlays (optional but recommended).
- A stable profile (don't record from `profile: "personal"` if you have private tabs open — use an agent profile).

Check with:

```bash
pagerunner status    # shows config + recording dependencies
```

---

## The Three Scenarios

Pick one before recording — each demands a different choreography.

| Scenario | Goal | Pacing | Markers | Zoom |
|---|---|---|---|---|
| **Bug repro** | Reproduce a defect so a maintainer can act on it | Slow, deliberate | One marker per key step + one on failure | Zoom to error |
| **Feature demo** | Make a reviewer / customer *feel* the feature | Punchy, cuts fast | Markers name the beats ("Step 1: paste link") | Zoom to interactive elements |
| **Onboarding tutorial** | Teach a first-time user a workflow end-to-end | Patient, readable | Dense markers, every screen gets one | Zoom to the control being introduced |

If you're not sure which you're making, **stop and decide**. The worst videos are the ones that try to be all three.

---

## Principle: The Cursor is the Narrator

The Pagerunner renderer tracks the cursor with a physics-based spring. That means:

- **Every `click` / `fill` / `scroll` teleports the cursor to a new target.** If two calls fire in rapid succession, the cursor whips across the screen.
- The cursor has a glow and a click ripple — viewers' eyes will follow it.

The implication: **don't fire 12 actions back-to-back**. Sequence them so the cursor draws a readable path.

```javascript
// ❌ Bad — cursor zigzags, viewer loses the thread
await fill(s, t, "#email", "jane@acme.com");
await click(s, t, ".submit");
await fill(s, t, "#reason", "beta access");

// ✅ Good — insert a short pause after each step so the spring settles,
// and let the renderer auto-zoom between frames
await fill(s, t, "#email", "jane@acme.com");
await wait_for(s, t, { ms: 400 });
await fill(s, t, "#reason", "beta access");
await wait_for(s, t, { ms: 400 });
await click(s, t, ".submit");
```

A 300–500 ms `wait_for({ ms })` between actions reads naturally in the final 30 fps output. In interpolation mode it feels like a confident operator, not a script.

---

## Principle: Markers Are Captions, Not Logs

`add_marker(session_id, label, note?)` writes a timestamped entry that becomes:

1. A burned-in text overlay (if you render with overlays enabled).
2. An entry in the SRT subtitle file.
3. A seek-able chapter point in `get_recording`.

So markers aren't debug breadcrumbs — they're the voice-over track. Write them for the viewer, not for yourself.

```javascript
// ❌ Too engineer-y, nothing about *why*
await add_marker(s, "click_submit");

// ✅ Tells the viewer what's happening and why it matters
await add_marker(s, "Submit the request — the backend fans out to all reviewers");
```

**Cadence:**
- Bug repro: marker on arrival at a screen, marker on every action, marker at the moment of failure with a `note` describing what you expected vs. what happened.
- Feature demo: one marker per beat, ≤ 40 characters, written like a slide title.
- Tutorial: every screen gets a marker; every interaction that a viewer would need to replicate also gets one.

**Always add a final marker** describing the outcome. It's the conclusion slide.

---

## Principle: Zoom Is Not Free

`render_recording` can apply a 1.8× zoom into the click/fill target during post-processing. It's glossy but it **costs attention** — the viewer loses spatial context every time it fires.

Rules of thumb:

- **Zoom on fine-grained UI** (buttons, form fields, inline error text). Skip zoom on broad navigations (clicking a big card) — auto-zoom will over-crop.
- **Don't chain zooms.** If two consecutive actions are in the same area, disable zoom on the second: `render_recording` accepts per-action zoom overrides via the `options.zoom_exceptions` array.
- **Let the zoom breathe.** The spring takes ~400 ms to settle. Immediately scrolling or clicking after a zoom creates a jarring double-motion.

---

## Quick Start — Record a Bug Repro

```javascript
const sessionId = await open_session({ profile: "agent-work" });
const [tab] = await list_tabs(sessionId);
const tabId = tab.target_id;

// 1. Start recording BEFORE the reproduction steps
await start_recording(sessionId, tabId, "bug-invoice-zero-total");
await add_marker(sessionId, "Open the invoices page");

await navigate(sessionId, tabId, "https://app.example.com/invoices");
await wait_for(sessionId, tabId, { selector: ".invoice-list", ms: 5000 });

await add_marker(sessionId, "Click 'Create invoice'");
await click(sessionId, tabId, ".btn-new-invoice");
await wait_for(sessionId, tabId, { selector: "#amount", ms: 5000 });

await add_marker(sessionId, "Enter the amount");
await fill(sessionId, tabId, "#amount", "250.00");
await wait_for(sessionId, tabId, { ms: 500 });

await add_marker(sessionId, "Submit — bug: total shows $0.00 on the next screen");
await click(sessionId, tabId, "button[type=submit]");
await wait_for(sessionId, tabId, { selector: ".invoice-summary", ms: 5000 });

await add_marker(sessionId, "Expected: $250.00 · Actual: $0.00");

// 2. Stop
const { recording_id } = await stop_recording(sessionId);

// 3. Render with conservative settings (no flashy zoom; viewer needs context)
await render_recording(recording_id, {
  overlay: { position: "bottom", font_size: 28, bg_color: "#000000CC" },
  zoom: { enabled: false },
  motion_interpolation: true,
  window_chrome: true
});
```

The resulting MP4 is attach-to-a-Jira-ticket ready.

---

## Quick Start — Record a Feature Demo

Feature demos sell. Treat them like ads.

```javascript
await start_recording(sessionId, tabId, "feature-bulk-export");
await add_marker(sessionId, "Bulk export · any view, one click");

await navigate(sessionId, tabId, "https://app.example.com/contacts");
await wait_for(sessionId, tabId, { selector: ".contact-row", ms: 5000 });
await wait_for(sessionId, tabId, { ms: 800 });   // let the page breathe

await add_marker(sessionId, "Step 1 · filter to active customers");
await click(sessionId, tabId, "#filter-status");
await wait_for(sessionId, tabId, { ms: 300 });
await select(sessionId, tabId, "#filter-status", "active");
await wait_for(sessionId, tabId, { ms: 600 });

await add_marker(sessionId, "Step 2 · one click to export");
await click(sessionId, tabId, ".btn-export");
await wait_for(sessionId, tabId, { selector: ".toast-success", ms: 5000 });

await add_marker(sessionId, "Done · CSV delivered to your inbox");

const { recording_id } = await stop_recording(sessionId);

// Demo render: lean into the polish
await render_recording(recording_id, {
  overlay: { position: "top", font_size: 48, font: "Inter-Bold", text_color: "white", bg_color: "#0F172AE6" },
  zoom: { enabled: true, factor: 1.8, smoothness: "smooth" },
  motion_interpolation: true,
  window_chrome: true,
  cursor: { glow: true, ripple: true }
});
```

Rules for demos:

- Final file should be ≤ 45 seconds. Cut anything that isn't a beat.
- First marker is your headline. It burns in from frame zero.
- Last marker is your CTA / outcome.
- Always render with `window_chrome` on — it makes the screenshot feel like a product, not a screencap.

---

## Quick Start — Record an Onboarding Tutorial

Tutorials are the patient cousin of demos. Viewers need time to follow along.

```javascript
await start_recording(sessionId, tabId, "tutorial-first-report");

// Introduce the landing screen with a beat of silence
await navigate(sessionId, tabId, "https://app.example.com");
await wait_for(sessionId, tabId, { selector: ".dashboard", ms: 5000 });
await add_marker(sessionId, "This is the dashboard. Reports live under 'Analytics'.");
await wait_for(sessionId, tabId, { ms: 1500 });     // hold

await add_marker(sessionId, "Click 'Analytics' in the sidebar");
await click(sessionId, tabId, "a[href='/analytics']");
await wait_for(sessionId, tabId, { selector: ".analytics-home", ms: 5000 });
await wait_for(sessionId, tabId, { ms: 1000 });

await add_marker(sessionId, "Pick a template — we'll use 'Weekly Summary'");
await click(sessionId, tabId, "[data-template=weekly-summary]");
await wait_for(sessionId, tabId, { selector: "#report-editor", ms: 5000 });
await wait_for(sessionId, tabId, { ms: 1200 });

await add_marker(sessionId, "Name it, then hit Save");
await fill(sessionId, tabId, "#report-name", "Q2 Ops Weekly");
await wait_for(sessionId, tabId, { ms: 500 });
await click(sessionId, tabId, ".btn-save");
await wait_for(sessionId, tabId, { selector: ".toast-saved", ms: 5000 });

await add_marker(sessionId, "Saved · find it under 'My Reports' any time");

await stop_recording(sessionId);
```

Render tutorials with:

- `overlay.position: "bottom"` — users read left-to-right, top-to-bottom, and the narration should feel like a caption.
- `motion_interpolation: true` + longer `wait_for` gaps (1000–1500 ms) — gives the viewer time to orient.
- `zoom.enabled: true` with `factor: 1.6` (less than demo mode) — enough to highlight, not enough to disorient.

---

## Auto-Record Mode

For long agent runs you don't want to baby-sit, enable auto-record in `~/.pagerunner/config.toml`:

```toml
[recording]
auto_record = true
fps = 10
output_fps = 30
retention_days = 7     # delete recordings older than a week

[overlay]
position = "bottom"
font_size = 36
text_color = "white"
bg_color = "#000000AA"
```

Every session with recording-enabled tabs gets captured. `list_recordings` is your archive. This is the right setting for:

- CI-run agents (evidence trail for failed runs).
- Compliance-heavy workflows where "show the video" is the proof.
- Long-horizon autonomous tasks where a failure six hours in needs a replay.

Pair with `retention_days` — disk fills faster than you think.

---

## Render Options Cheat Sheet

`render_recording(recording_id, options)` accepts a nested object. The ones you'll reach for most:

```javascript
{
  overlay: {
    position: "top" | "bottom",    // where markers appear
    font: "Inter" | "SF Pro" | ... ,
    font_size: 28 – 48,             // 28 for long copy, 48 for title cards
    text_color: "white",
    bg_color: "#000000AA"           // semi-transparent pill behind text
  },
  zoom: {
    enabled: true,
    factor: 1.4 – 1.8,              // 1.4 subtle, 1.8 cinematic
    smoothness: "snappy" | "smooth" // snappy = 250ms ease, smooth = 600ms spring
  },
  motion_interpolation: true,       // 10 → 30 fps; turn off for screencap authenticity
  window_chrome: true,              // rounded corners + gradient backdrop
  cursor: {
    glow: true,
    ripple: true                    // click ripples
  },
  srt: true                         // emit a .srt alongside the .mp4
}
```

If you don't pass `options`, the renderer applies a sensible default profile. For polished output, *always* pass one — defaults are conservative.

---

## Pre-flight Checklist

Before `start_recording`, verify:

- [ ] Am I on an **agent profile**, not a personal one? (Check tabs you don't want in the recording.)
- [ ] Did I `navigate` + `wait_for` to a *known good state* first? Starting mid-load makes the opening frames feel broken.
- [ ] Have I decided on the scenario (bug repro / demo / tutorial)?
- [ ] Have I drafted the marker script? Writing it ahead of time is 10× easier than improvising.
- [ ] Is the viewport at a sensible size? Tiny windows look cramped; giant ones feel unfocused. 1280×800 is a good default.

---

## Post-Flight Checklist

After render:

- [ ] Does the first second make sense with no audio? (Markers should burn in from frame zero if the overlay handler is on.)
- [ ] Is there more than 2 s of dead time anywhere? Cut it (`render_recording` accepts `trim` ranges).
- [ ] Is the cursor visible against every backdrop? Dark UIs + dark cursor = invisible — adjust `cursor.glow`.
- [ ] Is the final frame a coherent "outcome" view? Viewers rewind to whatever's on screen at the end.

---

## When Recording Goes Wrong

| Symptom | Fix |
|---|---|
| ffmpeg error on `stop_recording` | Check `pagerunner status` — ffmpeg missing or old. Need ≥ 6.0. |
| Cursor jumps off-screen during zoom | Action target wasn't in viewport. `scroll` to the element first, then act. |
| Markers don't burn in | `ImageMagick` missing. `brew install imagemagick` and re-render. |
| Auto-zoom snaps to the wrong element | Pagerunner zooms to the last interaction's target. Avoid interleaved `evaluate` calls that leave the cursor elsewhere. |
| Recording is a static screen | Tab navigated in a different target than `start_recording` tracked. Confirm `target_id` match. |

See [DEBUGGING.md](DEBUGGING.md) for general troubleshooting.

---

## What Recording Is *Not* For

- **High-fidelity screen capture of fast gameplay-like content.** 10 fps capture is enough for web UI; it's not enough for anything animated at 60 fps.
- **Audio.** Pagerunner captures video only. Pair with a separate voice-over tool (e.g. ElevenLabs) and mux in post if needed.
- **Multi-tab panoramas.** Each recording tracks one tab. Record each, composite externally.

---

## Related Docs

- [REFERENCE.md § Video Recording](REFERENCE.md#video-recording-7-tools) — tool signatures.
- [ADVANCED.md § Retention and Cleanup](ADVANCED.md#retention-and-cleanup) — disk management for auto-record.
- [EXAMPLES.md](EXAMPLES.md) — end-to-end workflows; recording fits cleanly into several of them.
