# Example — Basic: inject html-mark into one HTML file

The most common scenario. You have a static HTML prototype on disk (a Figma export, a Claude-generated mockup, a landing page draft) and want to start an annotated review.

## Prompt

```
Add html-mark to /Users/me/work/proto.html
```

or simply:

```
Mark up ~/Downloads/landing-v2.html for review
```

## What the skill does

1. Reads `~/.claude/skills/html-mark/html-mark.js` (the self-contained runtime).
2. Locates the closing `</body>` tag in the target file.
3. Wraps the runtime in `<script>…</script>` and inserts it right before `</body>`.
4. Returns a one-line confirmation with a clickable file link.

The HTML stays single-file, so you can email or AirDrop it and the reviewer needs nothing else.

## Verification

Open the file in any modern browser, then:

| Step | Expected result |
|---|---|
| Look at top-right | Dark glass pill `● Mark` with a small gray dot |
| Click the pill (or press `M`) | Dot turns into glowing coral, text becomes `● Marking` (honey color), cursor → crosshair, glass annotation panel appears bottom-right |
| Click any element | Coral pin drops in (with bounce animation), glass note popup opens next to it |
| Type "make this bigger" + `Enter` | Popup closes, pin gets a small coral dot in the corner indicating "has note" |
| Hover the panel list item | Pin scales up, target element gets coral outline |
| Click "Copy all" | Toast `✓ 1 annotation copied as MD`, clipboard contains a Markdown block |

## Copied output sample

```markdown
# Annotations — Landing v2 (/Downloads/landing-v2.html)

**1.** make this bigger
   <sub>h1 · "Where AI agents shop" · `h1`</sub>
```

Paste into Notion / Linear / a Lark doc and it renders as a numbered annotation list with subtle DOM hints below each note.

## Tips

- For elements that don't have an `id` (e.g. a generic `<div>`), add `data-mm-label="Plan card: Pro"` and the pin will use that label verbatim.
- Press `Backspace` while mark mode is on to undo the last pin.
- Drag the panel header to move it; click `−` to collapse it to a single-row badge when reviewing the bottom of the page.
