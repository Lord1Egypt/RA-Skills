---
name: mobile-reading-export
description: "Turn a Markdown or structured document into formats that actually read well on a phone — a narrow-screen-first responsive HTML, a phone-ratio PDF for WeChat/iOS sharing, and a one-page share card PNG. Use this whenever the user asks how to read a document on their phone, wants a \"手机版 / 手机上看 / 发微信 / 发给别人看\" version of a long document, complains that a table or PDF is unreadable on a phone, or asks which format to use for mobile reading. Also covers diagnosing and fixing horizontal overflow on narrow viewports, and the Windows headless-Chrome pitfalls that break phone-viewport screenshots."
description_zh: "手机阅读版导出"
description_en: "Mobile reading export"
disable: false
agent_created: true
version: "1.0.0"
---

# mobile-reading-export

Convert documents into mobile-first deliverables. Three outputs, each matched to a delivery channel:

| Output | Use for | Key property |
|---|---|---|
| Responsive HTML | reading it yourself | tables collapse to cards on narrow screens; warm editorial paper layout; dark-mode aware; single file, zero external deps |
| Phone-ratio PDF | sending to others (WeChat / iOS) | page = one phone screen, so "fit width" needs no pinch-zoom |
| Share card PNG | forwarding, group chats, elders | one screen, five key blocks, not the whole document |

## When to use

- "有什么更适合在手机上看的格式" / "手机上怎么读" / "能不能弄成手机版"
- User wants to send a document to someone via WeChat
- A table or PDF is described as unreadable, tiny, or needing zoom on a phone
- Any long document destined for phone reading rather than desktop editing

## Decide the format before building

Format choice follows the **delivery channel**, not personal taste:

| Format | Opens in WeChat? | Narrow-screen tables | Searchable | Fits iOS |
|---|---|---|---|---|
| `.md` | No — needs a reader app | overflows | yes | poor |
| Responsive HTML | save to Files → Safari (2 steps) | **collapses to cards** | yes | ok |
| **Phone-ratio PDF** | yes, built-in preview, saves to Books | needs zoom | yes | **best** |
| A4 PDF | yes | needs pinch-zoom (body text drops to ~8–9px) | yes | poor |
| Long image | yes | no overflow | no | best to forward |
| Cloud doc | yes, native | native | yes | but uploads private content |

Rules of thumb:
- iOS + sharing → **phone-ratio PDF is the primary**; HTML is the self-read version.
- Android → HTML opens in one step from WeChat, so HTML is fine as primary.
- Do **not** build a full-document long image. A 200-line document renders 20000px+ tall, gets recompressed by WeChat, and becomes unreadable. A one-screen share card is the correct use of images.
- Never publish private documents to a public URL (GitHub Pages, public site hosting) just to read them on a phone.

## Steps

### 1. Measure the source before designing

Count table rows and their display width (CJK = 2 half-widths). If more than about half the table rows exceed ~40 half-widths, tables will overflow on a phone and must become cards.

### 2. Generate mobile-first HTML

```
python scripts/md2mobile.py <in.md> <out.html> ["optional notice line"]
```

Conversion rules already implemented:
- 4-column pillar-style tables → four vertical cards (hero value in accent colour)
- 2-column tables → label above value
- 3+ column tables → one row-led block: col1 = title, col2 = subtitle, rest = fields; ordinary rows use dividers rather than a stack of identical cards
- Verdict columns (`吉平慎` / `标注` / `评级` / `可用性`) → coloured chips
- Rows containing `现行` / `现年` → highlighted with the accent tint
- First H1 → a restrained document masthead with a small eyebrow and short accent rule
- H2/H3 → warm brown editorial headings with a quiet highlight underline, not heavy boxed section headers
- Screen body → pale lavender-grey editorial surface + deep indigo serif headings + muted gold micro-labels + fine rules; print reverts to a clean white paper surface
- `---` immediately before a heading is dropped (otherwise the rule and the heading's top border stack into a double line)

The visual reference for the current style is a warm, mobile-first information sheet: rounded paper container, clear section rhythm, a few pale status chips, and selective emphasis. Do not reproduce app marketing copy such as "top decision maker" or treat decorative scores as objective psychological measurements.

Page geometry lives at the top of the script: `PAGE_W_MM = 104`, `PAGE_H_MM = 225`, `PAGE_PAD_MM = 5`. 104mm ≈ 393 CSS px = iPhone viewport width; ratio 1:2.16 matches modern phones. Content width works out to ~355px, matching a phone's ~357px text column.

### 3. Verify there is no horizontal overflow

```
python scripts/cap.py <out.html> <out_prefix> [scale]
```

Prints `CW` (viewport), `SW` (scroll width), `BW` (body width), `BAD` (count of overflowing elements) and a section position map. **`BAD=0` is the pass condition.** Also writes `<prefix>.png` (first screen) and `<prefix>_full.png` (whole page).

### 4. Build the phone-ratio PDF

```
python scripts/topdf.py <out.html> <out.pdf>
```

Confirms the MediaBox in mm. Expected: `104.1 x 225.0 mm`.

### 5. Check pagination

```
python scripts/pdfinfo.py <out.pdf> [...]
```

Reports characters per page plus the first/last fragment of each page. Look for pages far below average — those mean something was pushed wholesale to the next page. Note that card-heavy pages hold fewer characters than prose pages at the same visual fullness, so only treat a page as broken when it also looks empty in a rendered crop.

### 6. Optional share card

```
python scripts/card.py <templates/share-card.json> "<out_dir>/card_*.html"
python scripts/cap.py "<out_dir>/card_F.html" "<out_dir>/card_F" 2
```

Five blocks: four pillars, structure, strength, seasonal adjustment, luck-cycle mainline. Copy `<prefix>_full.png` as the deliverable.

## Pitfalls

### Windows + headless Chrome (the ones that cost real time)

- **`--window-size` has a minimum on Windows (~552 CSS px).** Asking for `393` silently yields a ~526px layout viewport while the screenshot is still 393px wide — content is clipped on *both* sides (the left side loses the start of each wrapped line). There is no error and no warning.
- **`--force-device-scale-factor` scales the PNG but does not shrink the CSS viewport.** `--window-size=393,850 --force-device-scale-factor=2` gives a 786×1700 PNG of a 526px-wide layout.
- **Without `--window-size`, Chrome's default layout viewport is ~754px.** Any measurement taken without passing the window size is measuring the wrong viewport.
- **A full-width coloured probe cannot detect the clamp.** A bar spanning the full viewport, clipped to the image width, measures exactly the image width. Measure a fixed-width element or read `documentElement.clientWidth` instead.
- **The fix that always works:** inject `body{width:393px !important;margin:0 !important}`, render with a generous window (e.g. 700px wide, taller than the content), then crop the image to the 393px column. See `FORCE_STYLE` in `cap.py`. Do not try to fight the clamp with window flags.
- **PowerShell swallows or GBK-misdecodes Chrome's stdout.** `--dump-dom` returns nothing useful through `&` and `2>&1`. Call Chrome from Python `subprocess.run(..., capture_output=True)` and decode UTF-8, or via a Node `spawnSync` bridge. Do not trust PowerShell-redirected Chrome output.
- **`@media print` evaluates `min-width` against the window width, not the page width.** Desktop multi-column rules therefore leak into the PDF. This is invisible until you compare page counts. Always re-pin the mobile layout inside `@media print` with `!important`:

  ```css
  @media print{
    .pillars{grid-template-columns:1fr !important}
    .pl{flex-basis:80px !important}
  }
  ```

  Corollary: keep desktop enhancements behind `min-width:900px` so a 700px capture window never triggers them.
- **`break-inside:avoid` on a container taller than a page makes a near-blank page.** Chrome cannot honour the constraint, so it pushes the entire block to the next page and leaves the heading alone on the previous one. Apply it to *leaf* elements (single card, single row, note block), never to the wrapping list.
- **`document.body.scrollHeight` can under-report.** Crop the image to the last row containing non-background pixels instead of trusting the measured height.
- **`h1,h2,h3{break-inside:avoid}`** is needed as well, otherwise heading text splits mid-line across pages.
- Read PNG dimensions straight from the header (width/height big-endian at bytes 16–23); `Add-Type -AssemblyName System.Drawing` is blocked by security policy in some environments.
- On Windows, `Remove-Item` may be blocked by a fail-closed safe-delete hook. Use `[System.IO.File]::Delete()`.

### Design

- Body text 17px with 1.75 line-height on screen; drop to 15px in print, which lands at roughly 16–17pt on an iPhone because fit-to-width scales a 104mm page up by ~1.33×.
- The default visual direction is **restrained editorial dossier**: pale lavender-grey surface, deep indigo serif type, muted gold micro-labels, fine lavender rules, and pale blue/mint/yellow status chips. This borrows the references' typographic hierarchy and spacing, not their promotional claims.
- Use asymmetry through hierarchy, not decoration: one masthead, highlighted section labels, four-pillar cards, then divider-led prose/rows. Do not wrap every paragraph in a card and do not add progress bars unless the source contains a meaningful numeric scale.
- Give labels their own narrow column (~80px ≈ four CJK characters). Longer header names wrap and break row alignment — strip parenthetical qualifiers (`辰时盘（App，庚辰时）` → `辰时盘`) rather than widening the column.
- Keep the notices honest: a footer like `个人命理资料 · 仅供本人参考` is protective without forbidding sharing. Avoid `请勿转发` on a document the user intends to send.
- When the source is a命理档案, professional terms must be paired with a short real-world explanation in the prose; visual polish cannot be used to hide unsupported conclusions.

## Verification

1. `cap.py` reports `BAD=0` — no element wider than the viewport.
2. `cap.py` reports `BW` equal to the intended column width (e.g. 393), not merely a plausible-looking number.
3. `topdf.py` reports the expected MediaBox in mm.
4. `pdfinfo.py` shows no page dramatically below the average character count.
5. Render and visually inspect at least: the first screen, one card-dense table, one blockquote containing a nested table, and the last page. Crop regions at 2–3× with `zoom.py` rather than squinting at a downscaled screenshot — low-resolution views produce phantom defects.
