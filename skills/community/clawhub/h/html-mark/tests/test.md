# Manual smoke test

Run through this checklist after any change to `html-mark.js`. Should take ~3 minutes.

## Setup

1. Create a minimal test page:

```bash
cat > /tmp/mm-test.html <<'EOF'
<!doctype html>
<html><head><meta charset="utf-8"><title>MM Test</title>
<style>
  body { font: 15px/1.6 system-ui; padding: 40px; background: #fefaf3; }
  .card { background: white; padding: 20px; border-radius: 12px;
          box-shadow: 0 4px 16px rgba(0,0,0,.05); margin-bottom: 20px; }
  h1 { font-size: 28px; margin: 0 0 20px; }
  button { padding: 8px 14px; border-radius: 8px; border: 1px solid #ccc;
           background: white; cursor: pointer; }
</style></head><body>
<h1>HTML Mark test page</h1>
<div class="card" data-mm-label="Plan card · Pro">
  <h3>Pro plan</h3><p>For growing brands shipping to AI agents.</p>
  <button id="cta-pro">Start Pro</button>
</div>
<div class="card" data-mm-label="Plan card · Mini">
  <h3>Mini plan</h3><p>For solo brands testing the waters.</p>
  <button>Start Mini</button>
</div>
</body></html>
EOF
```

2. Inject the runtime:

```bash
sed -i '' '/<\/body>/i\
<script>\
'"$(cat ~/.claude/skills/html-mark/html-mark.js)"'\
</script>
' /tmp/mm-test.html
```

3. Open in browser:

```bash
open /tmp/mm-test.html
```

## Checklist

### Visual baseline (mark mode OFF)
- [ ] Dark glass toggle pill at top-right (`● Mark`, gray dot)
- [ ] No panel visible
- [ ] No cursor change

### Toggle ON
- [ ] Click toggle → text becomes `● Marking`, dot lights up coral (with glow), text turns honey color
- [ ] Cursor → crosshair anywhere on page
- [ ] Glass panel appears bottom-right with empty state hint
- [ ] Pressing `M` toggles off / on identically

### Drop pin
- [ ] Click the `Start Pro` button → coral pin drops at click point (with scale bounce)
- [ ] Note popup opens immediately to the right of the pin
- [ ] Popup header shows `#1 · Button`, right side shows `Start Pro`
- [ ] Textarea is auto-focused, ready to type
- [ ] Hint row shows `↵ save · ⇧↵ newline · Esc close`

### Save note
- [ ] Type "make this bigger" → press `Enter` → popup closes
- [ ] Pin gets a small coral light dot on top-right corner
- [ ] Panel list item now bold-shows "make this bigger" + meta line `Button · Start Pro`
- [ ] Item num is coral-gradient (not the default dark) — indicates "has note"

### Multi-element pin
- [ ] Click on `Plan card · Mini` → pin #2 appears
- [ ] Press Esc to close note popup (pin keeps no note)
- [ ] Panel shows pin #2 with `No note · click to add` placeholder, num remains dark

### Hover sync
- [ ] Hover panel item #1 → pin #1 scales up + the `Start Pro` button gets coral outline
- [ ] Mouse leave → outline and scale revert

### Edit existing note
- [ ] Click pin #2 (or panel item #2) → popup re-opens
- [ ] Type "remove this plan" + Enter → list item #2 updates, num turns coral

### Panel drag + collapse
- [ ] Drag panel header → panel follows cursor
- [ ] Click `−` icon → panel collapses to single-row badge (still draggable)
- [ ] Click `+` icon → expanded again

### Backspace undo
- [ ] Press `Backspace` (not in any textarea) → last pin (#2) is removed
- [ ] Pin #1 stays, num remains 1

### Copy formats
- [ ] Select `Markdown` in dropdown → click `Copy all` → toast `✓ 1 annotation copied as MD`
- [ ] Paste into a text editor — should be Markdown with `**1.**`, `<sub>` meta line, `# Annotations —` header
- [ ] Switch to `JSON` → Copy all → toast says `JSON`. Paste → valid JSON with `context`, `annotations: [{id, note, label, text, selector}]`
- [ ] Switch to `Plain` → Copy all → simple numbered list with `@ <context>` footer

### Esc exits
- [ ] Press `Esc` → mark mode turns off, panel hides, cursor restores
- [ ] Pins remain visible until next toggle-on or manual clear

### Clean up
- [ ] Press `M` to re-enter mark mode → click `Clear` → all pins + panel reset

## Edge cases worth probing

- Scroll the page before clicking — pin should land precisely under cursor (not affected by scroll offset).
- Click on the `Plan card` background (not the button or h3) — pin label should be `[data-mm-label] · Plan card · Pro` thanks to the `data-mm-label` attribute.
- Drag the panel off-screen — clamping should keep it ≥4px inside the viewport.
- Hold `Shift+Enter` inside the note textarea — should insert a newline (not save).
- Open the same page twice in two tabs — each has independent state.

## Failure modes to file as bugs

If any of these happen, it's a regression:

- Pin offset from click point by more than 2px
- Note popup hidden behind viewport edge (no auto-flip)
- Hover outline persists after mouse leaves item
- `M` triggers toggle while typing into a focused input/textarea
- Clipboard write throws but no error toast appears
