# Skill ↔ Script Handoff Playbook

> Reusable lessons from building `ins-style-img-bulk-gen` against `huny-img` + `add_ins_overlay.py`.
> Use this when designing any skill that delegates work to a sub-skill or external API.

---

## The 5 Failure Modes We Hit

| # | Failure | Symptom | Diagnosis | Fix |
|---|---------|---------|-----------|-----|
| 1 | Parallel dispatch to rate-limited API | 3 of 4 image jobs return `RequestLimitExceeded.JobNumExceed` | Read the sub-skill's SKILL.md for concurrency hints; run a probe with 2 parallel calls and watch for limit errors | Dispatch **sequentially** when the sub-skill's API is single-threaded; pass `--poll-interval` / `--timeout` to control cadence |
| 2 | `.ttc` font loaded without `index` → fallback to 1-bit default | Chinese text renders as tofu rectangles | `python3 -c "from PIL import ImageFont; f = ImageFont.truetype('/path/font.ttc', 30); f.getmask('中').getbbox() == None"` | Always pass `index=0` (or specific index for bold/italic variants) when loading `.ttc` |
| 3 | CJK font missing decorative glyphs (❤ ★ ♡ →) | Hollow-X tofu box appears in the title | Render the suspect char to a 200×200 PNG with the chosen font and look at it; don't trust `getmask().getbbox()` (it's non-None for tofu too) | Route decorative Unicode through a **dedicated symbol font** (`Arial Unicode MS` is the cross-platform safety net) |
| 4 | Shadow rendered at top-left of text instead of bottom-right | White text looks "flat" against the gray mask; no depth | Render a single character with shadow, save the image, inspect — pixel diff between expected (dx=+3, dy=+3) and actual position | Inside the shadow layer, use `(margin + dx, margin + dy)` as the text origin, **not** `(margin - bbox[0] + dx, ...)` — the latter double-counts the bbox offset |
| 5 | `textwrap.wrap(width=N)` overflows on CJK + box height underestimated | Long lines extend past the gray mask; last line gets clipped | `dummy_draw.textlength(long_line, font=font)` and compare against `box_w - 2×padding` | Wrap by **measured pixel width** (`textlength` per char); measure per-line `textbbox` height and sum + `line_extra_gap` |

---

## Pre-Flight Checklist for Any New Skill

Before shipping a skill that wraps another tool, walk through this:

### 1. Survey the sub-skill's API limits
```bash
# Read the sub-skill's SKILL.md / README — note any rate limits, concurrency caps, file size limits
# Probe: submit 2 jobs in parallel and watch for errors
```

### 2. Survey platform dependencies
```bash
# What fonts/libraries/binaries does the sub-skill need?
# Is the dependency available on macOS, Linux, Windows?
# Run a probe script that loads the dependency and confirms it works.
```

### 3. Build a minimal end-to-end smoke test FIRST
```bash
# Before composing fancy prompts / layouts, run ONE round-trip and inspect output
# Open the generated image. Look for:
#   - Text rendering correctly (not tofu)
#   - Layout proportions sensible
#   - Output dimensions match expectations
```

### 4. Add visual diagnostics for non-deterministic bugs
- Shadow rendering?  Save an isolated test image with known content, eyeball it
- Font coverage?  Render every glyph you'll use to a strip image and inspect
- Text overflow?  Measure `textlength` and assert against a known bound

### 5. Write a regression test for every fix
- Use `unittest` or `pytest` (whichever is available)
- One test per bug class
- Run them in CI or as a pre-commit hook

---

## Diagnostic Commands

### Detect Chinese tofu (font fallback)
```python
from PIL import ImageFont, Image, ImageDraw
f = ImageFont.truetype('/path/font.ttf', 50)
img = Image.new('L', f.getmask('中').size)
img.putdata(f.getmask('中'))
# If extrema is (0, 0), the font has no '中' glyph → tofu fallback
print(img.getextrema())
```

### Detect decorative symbol tofu
```python
# Same as above but with '❤' or other decorative chars
# If Pillow has any font at all, it will return SOMETHING for the char
# (even a hollow-X box). Trust nothing — render and look.
img = Image.new('RGB', (200, 150), 'white')
ImageDraw.Draw(img).text((10, 10), '❤', font=f, fill='black')
img.save('/tmp/heart_test.png')  # Then eyeball this file
```

### Verify shadow direction
```python
from PIL import Image, ImageDraw, ImageFont, ImageFilter
img = Image.new('RGBA', (300, 200), (105, 105, 105, 255))
shadow = Image.new('RGBA', (300, 200), (0, 0, 0, 0))
ImageDraw.Draw(shadow).text((50, 50), 'A', font=font, fill=(0, 0, 0, 120))
shadow = shadow.filter(ImageFilter.GaussianBlur(2))
img.alpha_composite(shadow, (3, 3))  # The shadow offset goes HERE
ImageDraw.Draw(img).text((50, 50), 'A', font=font, fill='white')
img.save('/tmp/shadow_test.png')  # Eyeball: is shadow at bottom-right?
```

### Verify CJK text wrap fits within mask
```python
from PIL import ImageFont, ImageDraw
font = ImageFont.truetype('...', 50)
d = ImageDraw.Draw(Image.new('RGB', (1, 1)))
max_w = 800  # mask width
for line in wrapped_lines:
    assert d.textlength(line, font=font) <= max_w, f"Overflow: {line!r}"
```

---

## Pillow-Specific Gotchas

| Gotcha | What happens | Workaround |
|--------|-------------|------------|
| `.ttc` requires `index=` | `IOError`, silent fallback to default font | Always pass `index=0` |
| `textbbox` returns the bbox **at the given (x, y)** | Using bbox[0]/bbox[1] in offset math produces a double-offset bug | Use `(0, 0)` as anchor when measuring pure dimensions; add offset only at final composition |
| `ImageDraw.text` does not auto-fallback across fonts | One missing glyph = tofu, even if another font in the system has it | Implement `_pick_font_for_char` (CJK vs decorative) at script level |
| `getmask(ch).getbbox()` is non-None even for tofu | `if getbbox(): ...` looks like valid coverage check but lies | Render the actual glyph to PNG and inspect — never trust programmatic checks alone |
| `textwrap.wrap(width=N)` counts chars, not pixels | CJK chars are 2× wider than ASCII; width=N overflows by ~2× | Wrap by measured `textlength` instead |
| `multiline_textbbox` lies about height when fonts differ across runs | Underestimates total height → mask too short → last line clipped | Measure per-line `textbbox` and sum + line gap |

---

## Cross-Platform Font Safety Net

For any skill that does Chinese / Japanese / Korean rendering, **always include Arial Unicode MS** in the font candidate list. It's pre-installed on macOS (`/Library/Fonts/Arial Unicode.ttf`) and Windows (`C:\Windows\Fonts\Arialuni.ttf`), covers nearly all Unicode (CJK + decorative symbols + Latin), and is the most reliable fallback when nothing else works.

For Linux, the equivalent is `Noto Sans CJK` (install via `apt install fonts-noto-cjk`).

---

## Communication Pattern Between Skills

When you delegate to a sub-skill, the flow should be:

1. **Survey** — read sub-skill's SKILL.md, identify limits / dependencies / expected output format
2. **Probe** — run a minimal test before composing complex inputs
3. **Dispatch** — sequentially if rate-limited, with retries if jobs can fail independently
4. **Inspect** — always look at the output. Don't trust "no error returned" as success
5. **Archive** — copy outputs to a known location with a timestamp
6. **Post-process** — overlay / crop / compose with scripts you control
7. **Verify** — open final output, eyeball it, run regression tests

If you skip step 1 or 2, you'll hit bug #1, #2, or #3 in the table above.

---

## When Things Break

Add to this playbook every time you hit a new failure mode. The goal is that the next skill you build starts with a smaller surprise budget.
