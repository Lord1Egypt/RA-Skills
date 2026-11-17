# Browser tool workarounds — reliable recipes when native blocks fail

This file cures downstream agents from burning turns on tool patterns that are known to fail
or mislead. Use these recipes instead of retrying the failing path.

## browser_console — complex inline expressions are unreliable

**Failure mode:** multi-line JS, arrow-function IIFE, and even moderately complex expressions
routinely return `SyntaxError: Unexpected end of input` from `browser_console`.
After three identical failures the runtime raises `same_tool_failure_warning`, but you cannot
recover by re-issuing the same expression.

**What actually works:**
- `document.title`
- `2+2`
- Very short statements

**What does NOT work reliably:**
- `(() => { ... multi line ... })()`
- Array/object literals with method calls mixed together
- Nested functions or anything that looks like source the runtime splits before sending

## WCAG contrast verification — reliable recipe

1. **Write a tiny probe HTML** under the task arm dir (it self-documents the artifact and
   keeps the workspace honest). Include the relative-luminance formula inline.
2. **Navigate to `file:///…/probe.html`**.
3. **Read result from `document.getElementById('output').textContent`**, or via a short
   `browser_console` expression (`document.getElementById('output').textContent`).

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>contrast probe</title>
</head>
<body>
  <div id="output"></div>
  <script>
    const convert = (v) => v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
    const luminance = (rgb) => 0.2126 * convert(rgb[0]) + 0.7152 * convert(rgb[1]) + 0.0722 * convert(rgb[2]);
    const ratio = (a, b) => (Math.max(luminance(a), luminance(b)) + 0.05) / (Math.min(luminance(a), luminance(b)) + 0.05);
    const bg = [0xf8 / 0xff, 0xf8 / 0xff, 0xf8 / 0xff];
    const label = [0x22 / 0xff, 0x22 / 0xff, 0x22 / 0xff];
    const btnText = [1, 1, 1];
    const btnBg = [0x33 / 0xff, 0x33 / 0xff, 0x33 / 0xff];
    document.getElementById('output').textContent = JSON.stringify({ labelVsBg: ratio(label, bg), btnTextVsBtnBg: ratio(btnText, btnBg) });
  </script>
</body>
</html>
```

**Steps for the loop implementer (keelwright Phase 3):**
- Probe BEFORE the fix with the OLD colors → record the failing ratios.
- Fix CSS in the target file.
- Re-probe with the NEW colors → record the passing ratios.
- Both numbers belong in the treatment findings artifact (`treatment-findings.txt` or equivalent).

## Post-fix CSS verification via computed style

To confirm the rendered value actually matches the edited CSS file, navigate to the target
page and use a short console expression against `.selector` to read `cs.color` and
`backgroundColor`. Keep it one expression that returns a concise string or object: do not
nest functions or use multi-statement bodies.

## Pitfalls

- **Do not delete the probe artifact.** It is the machine evidence for the QA report.
- **Do not weaken the WCAG threshold.** The required floor is 4.5:1 for normal text.
  If a color cannot clear that bar, change it; do not patch the test.
- **probe.html is for one run only** — if colors change, rewrite the probe with the new values
  rather than hand-editing a script that already lives under the arm dir.
