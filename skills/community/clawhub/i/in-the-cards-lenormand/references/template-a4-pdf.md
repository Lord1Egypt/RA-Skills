# A4 PDF Template — Kami Style (v3.3)

> **Canonical seed file:** `assets/seed-a4-pdf.html`. Copy it, fill in placeholders, render with `scripts/generate-pdf.js`.

This reference documents the chapter structure, page balance rules, and spread-specific details for the A4 PDF product.

```html
<!DOCTYPE html>
<html lang="{zh-CN|en}">
<head>
<meta charset="UTF-8">
<title>Lenormand Reading — {question_summary}</title>
<meta name="generator" content="In the Cards">
<!-- CSS: font-face + @page + base styles -->
</head>
<body>

<!-- 1. Cover + Card Grid (single page) -->
<section class="cover">
  <!-- cover text: label, title, date -->
  <div class="cover-top">...</div>
  <!-- card grid layout inline -->
  <div class="cover-cards">...</div>
  <!-- cover footer -->
  <div class="cover-bottom">...</div>
</section>

<!-- 2. Interpretation Chapters (flow continuously, separated by section rules) -->
<section class="chapter">
  <h2>{chapter_title}</h2>
  <p>...</p>
  <blockquote class="combination">...</blockquote>
  ...
</section>

</body>
</html>
```

### @page Rules

```css
@page {
  size: A4;
  margin: 20mm 22mm 22mm 22mm;
  background: var(--parchment);

  @top-right {
    content: string(section-title);
    font-family: var(--serif);
    font-size: 8pt;
    color: var(--stone);
  }

  @bottom-center {
    content: counter(page) "  ·  Lenormand Reading";
    font-family: var(--serif);
    font-size: 9pt;
    color: var(--stone);
  }
}

@page:first {
  @top-right { content: ""; }
  @bottom-center { content: ""; }
}

/* If cover+cards overflows, subsequent pages get full header/footer */
@page:nth(1) {
  @top-right { content: ""; }
  @bottom-center { content: ""; }
}
```

---

## Cover Page Template

```html
<section class="cover">
  <div class="cover-top">
    <p class="cover-label">{spread_type_display}</p>
    <h1 class="cover-title">{question_text}</h1>
    <p class="cover-date">{date_display}</p>
  </div>
  <div class="cover-bottom">
    <p class="cover-meta">Lenormand Reading · In the Cards</p>
    <p class="cover-cards-preview">{card_names_list}</p>
  </div>
</section>
```

Cover CSS:
```css
.cover {
  string-set: section-title "";
  break-after: page;
}
.cover-top {
  margin-bottom: 8mm;
}
.cover-label {
  font-size: 10pt;
  color: var(--brand);
  letter-spacing: 2pt;
  text-transform: uppercase;
  margin-bottom: 8mm;
}
.cover-title {
  font-size: 28pt;
  font-weight: 500;
  color: var(--near-black);
  line-height: 1.3;
  max-width: 85%;
  border-left: 4pt solid var(--brand);
  padding-left: 12mm;
}
.cover-date {
  font-size: 11pt;
  color: var(--stone);
  margin-top: 6mm;
}
/* Card grid inside cover — constrained, compact */
.cover-cards {
  margin: 10mm 0 8mm 0;
}
.cover-cards h2 {
  font-size: 13pt;
  font-weight: 500;
  color: var(--brand);
  text-align: center;
  margin-bottom: 5mm;
  border-bottom: 1pt solid var(--border);
  padding-bottom: 2mm;
  display: inline-block;
}
.cover-bottom {
  border-top: 1pt solid var(--border);
  padding-top: 6mm;
}
.cover-meta {
  font-size: 9pt;
  color: var(--stone);
}
.cover-cards-preview {
  font-size: 14pt;
  color: var(--dark-warm);
  margin-top: 3mm;
  letter-spacing: 1pt;
}
```

---

## Card Grid Page Templates

### Card Rendering Modes

Two card rendering modes are supported. Default to **Text Mode** unless the user explicitly asks for visual cards, or the `cards/` SVG assets are referenced.

#### Mode 1: Text Card (Default)

Simple text blocks with polarity-colored backgrounds. No images, no external dependencies.

```html
<div class="card card-{polarity}">
  <span class="card-num">{number}</span>
  <span class="card-name">{name_zh}</span>
</div>
```

Card polarity colors:
```
positive → background: #E1F5EE, text: #085041
negative → background: #FAECE7, text: #6B2F1A
neutral  → background: #EEEDFE, text: #3C3489
```

#### Mode 2: Geometric Silence SVG Card

Inline SVG card faces from the `cards/` directory. Each SVG is a self-contained 1024×1536 Geometric Silence card with cream background, sage structural lines, rose accent, registration crosses, grid system, and bottom label.

```html
<!-- Inline the SVG directly from cards/card-{nn}-{slug}.svg -->
<svg class="card-svg" viewBox="0 0 1024 1536" width="...">
  <!-- paste full SVG content here -->
</svg>
```

Available at: `cards/card-01-rider.svg` through `cards/card-36-cross.svg`.

If the user wants visual cards, read the relevant SVG files and embed them inline. For layout sizing:

| Spread | SVG width | SVG height |
|--------|-----------|------------|
| Yes/No (1 card) | 130px | 195px |
| Two-card | 110px | 165px |
| Three-card | 112px | 168px |

**When PNG output is required** (via pdftoppm / poppler rasterization), SVG strokes thinner than ~1.5 on a 1024 viewBox will appear nearly invisible after PDF→PNG conversion due to anti-aliasing of sub-pixel lines. Remedies:
- Increase card display size (e.g. 180–200px width for 3-card spread)
- Bump symbol stroke-widths to 1.5–1.8
- Bump center dot radii to 4–5
- Set `gap: 0` + `justify-content: space-evenly` to fit larger cards in row layout
- Use a 2× viewport (1588×2246) when generating the PDF via Puppeteer for higher SVG rasterization fidelity
| Five-card | 85px | 128px |
| Box (9-card) | 80px | 120px |
| A-or-B (3+3) | 95px | 143px |

Center card (position 3 in 5-card, position 5 in box) gets `outline: 2pt solid var(--brand)` with `outline-offset: 2pt`.

```css
.card-svg {
  /* No border, no box-shadow — the SVG card face is self-contained */
}
.card-svg-center {
  outline: 2pt solid var(--brand);
  outline-offset: 2pt;
}
```

**SVG ID collision warning**: All 36 card SVGs share the same `<pattern>` defs (`id="g"`, `id="sg"`). When embedding multiple cards inline in the same HTML document, DO NOT include each SVG's `<defs>` block — duplicate IDs will cause Firefox/Puppeteer rendering issues. Instead, add a single hidden SVG with the defs at the top of `<body>`:

```html
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <defs>
    <pattern id="g" width="72" height="72" patternUnits="userSpaceOnUse">
      <path d="M72 0L72 72M0 72L72 72" fill="none" stroke="#7A8B7A" stroke-width="0.3" opacity=".12"/>
    </pattern>
    <pattern id="sg" width="18" height="18" patternUnits="userSpaceOnUse">
      <path d="M18 0L18 18M0 18L18 18" fill="none" stroke="#7A8B7A" stroke-width="0.2" opacity=".06"/>
    </pattern>
  </defs>
</svg>
```

Then strip `<defs>…</defs>` from each inline card SVG, keeping only the visual elements.

### Card CSS (Text Mode)

```css
/* Card grid is rendered inside .cover-cards — no page break */
.card {
  text-align: center;
  break-inside: avoid;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 4pt;
  padding: 6pt;
}
.card-positive { background: #E1F5EE; color: #085041; }
.card-negative { background: #FAECE7; color: #6B2F1A; }
.card-neutral  { background: #EEEDFE; color: #3C3489; }
.card-num {
  font-size: 20pt;
  font-weight: 600;
  margin-bottom: 1.5mm;
}
.card-name {
  font-size: 9pt;
  font-weight: 500;
}

/* Spread-specific card sizes for layout balance */
.spread-yesno .card { width: 100px; height: 130px; }
.spread-yesno .card-num { font-size: 28pt; }
.spread-two   .card { width: 100px; height: 130px; }
.spread-three .card { width: 90px;  height: 120px; }
.spread-five  .card { width: 75px;  height: 100px; }
.spread-five  .card-num { font-size: 16pt; }
.spread-box   .card { width: 75px;  height: 100px; }
.spread-box   .card-num { font-size: 16pt; }
```

### Spread Layout: 1-Card Yes/No

Rendered inside `.cover-cards`:

```html
<div class="cover-cards">
  <h2>Yes / No Reading</h2>
  <div class="spread-layout spread-yesno">
    <div class="card card-{polarity}">
      <span class="card-num">{number}</span>
      <span class="card-name">{name_zh}</span>
    </div>
    <div class="verdict-badge verdict-{verdict}">
      {verdict_text}
    </div>
  </div>
</div>
```

```css
.spread-yesno {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0 0 10mm 0;
}
.verdict-badge {
  margin-top: 6mm;
  padding: 2mm 8mm;
  border-radius: 4pt;
  font-size: 18pt;
  font-weight: 500;
  letter-spacing: 3pt;
}
.verdict-yes    { background: #E1F5EE; color: #085041; }
.verdict-no     { background: #FAECE7; color: #6B2F1A; }
.verdict-maybe  { background: #EEEDFE; color: #3C3489; }
```

### Spread Layout: 2-Card

Rendered inside `.cover-cards`:

```html
<div class="cover-cards">
  <h2>Two-Card Pair</h2>
  <div class="spread-layout spread-two">
    <div class="card card-{polarity}"><span class="card-num">{num1}</span><span class="card-name">{name_zh}</span></div>
    <div class="card-arrow">+</div>
    <div class="card card-{polarity}"><span class="card-num">{num2}</span><span class="card-name">{name_zh}</span></div>
  </div>
</div>
```

```css
.spread-two {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8mm;
  padding: 0 0 10mm 0;
}
.card-arrow {
  font-size: 24pt;
  color: var(--brand);
  font-family: var(--serif);
}
/* Position labels below card spreads */
.spread-labels {
  display: flex;
  justify-content: center;
  gap: 5mm;
  margin-top: 2mm;
}
.spread-labels span {
  width: 90px;
  text-align: center;
  font-size: 9pt;
  color: var(--stone);
}
```

### Spread Layout: 3-Card

Rendered inside `.cover-cards`:

```html
<div class="cover-cards">
  <h2>Three-Card Linear Spread</h2>
  <div class="spread-layout spread-three">
    <div class="card card-{polarity}"><span class="card-num">{num1}</span><span class="card-name">{name_zh}</span></div>
    <div class="card-arrow">→</div>
    <div class="card card-{polarity}"><span class="card-num">{num2}</span><span class="card-name">{name_zh}</span></div>
    <div class="card-arrow">→</div>
    <div class="card card-{polarity}"><span class="card-num">{num3}</span><span class="card-name">{name_zh}</span></div>
  </div>
  <div class="spread-labels">
    <span>1</span><span></span><span>2</span><span></span><span>3</span>
  </div>
</div>
```

```css
.spread-three {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 5mm;
  padding: 0 0 4mm 0;
}
```

### Spread Layout: 5-Card

Rendered inside `.cover-cards`:

```html
<div class="cover-cards">
  <h2>Five-Card Linear Spread</h2>
  <p class="spread-note">Center card (position 3) = core theme</p>
  <div class="spread-layout spread-five">
    <div class="card card-{polarity}"><span class="card-num">{num1}</span><span class="card-name">{name_zh}</span></div>
    <div class="card-arrow">→</div>
    <div class="card card-{polarity}"><span class="card-num">{num2}</span><span class="card-name">{name_zh}</span></div>
    <div class="card-arrow">→</div>
    <div class="card card-center card-{polarity}"><span class="card-num">{num3}</span><span class="card-name">{name_zh}</span></div>
    <div class="card-arrow">→</div>
    <div class="card card-{polarity}"><span class="card-num">{num4}</span><span class="card-name">{name_zh}</span></div>
    <div class="card-arrow">→</div>
    <div class="card card-{polarity}"><span class="card-num">{num5}</span><span class="card-name">{name_zh}</span></div>
  </div>
</div>
```

```css
.spread-five {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 3mm;
  padding: 0 0 4mm 0;
}
.card-center {
  border: 3pt solid var(--brand);
}
.spread-note {
  text-align: center;
  font-size: 9pt;
  color: var(--stone);
  margin-bottom: 4mm;
}
```

### Spread Layout: 9-Card Box Spread (3×3)

Rendered inside `.cover-cards`:

```html
<div class="cover-cards">
  <h2>3×3 Box Spread · 九宮格牌陣</h2>

  <!-- Column labels -->
  <div class="box-column-labels">
    <span class="col-label col-past">{past_label}</span>
    <span class="col-label col-present">{present_label}</span>
    <span class="col-label col-future">{future_label}</span>
  </div>

  <!-- 3×3 grid -->
  <div class="spread-layout spread-box">
    <div class="box-row">
      <div class="card card-{polarity}"><span class="card-num">{n1}</span><span class="card-name">{name_zh}</span></div>
      <div class="card card-{polarity}"><span class="card-num">{n2}</span><span class="card-name">{name_zh}</span></div>
      <div class="card card-{polarity}"><span class="card-num">{n3}</span><span class="card-name">{name_zh}</span></div>
    </div>
    <div class="box-row">
      <div class="card card-{polarity}"><span class="card-num">{n4}</span><span class="card-name">{name_zh}</span></div>
      <div class="card card-center card-{polarity}"><span class="card-num">{n5}</span><span class="card-name">{name_zh}</span></div>
      <div class="card card-{polarity}"><span class="card-num">{n6}</span><span class="card-name">{name_zh}</span></div>
    </div>
    <div class="box-row">
      <div class="card card-{polarity}"><span class="card-num">{n7}</span><span class="card-name">{name_zh}</span></div>
      <div class="card card-{polarity}"><span class="card-num">{n8}</span><span class="card-name">{name_zh}</span></div>
      <div class="card card-{polarity}"><span class="card-num">{n9}</span><span class="card-name">{name_zh}</span></div>
    </div>
  </div>
</div>
```

```css
.spread-box { margin: 4mm 0 6mm 0; }
.box-row {
  display: flex;
  justify-content: center;
  gap: 4mm;
  margin-bottom: 4mm;
}
.box-column-labels {
  display: flex;
  justify-content: center;
  gap: 4mm;
  margin-bottom: 2mm;
  font-size: 10pt;
  color: var(--brand);
  font-weight: 500;
}
.col-label { width: 75px; text-align: center; }
.card-center {
  border: 3pt solid var(--brand);
}
```

### Spread Layout: A-or-B (Choice)

Rendered inside `.cover-cards`:

```html
<div class="cover-cards">
  <h2>A-or-B Choice · 二選一</h2>

  <div class="choice-option">
    <h3 class="choice-label label-a">A. {optionA_text}</h3>
    <div class="spread-layout spread-three">
      <div class="card card-{polarity}"><span class="card-num">{a_num1}</span><span class="card-name">{name_zh}</span></div>
      <div class="card-arrow">→</div>
      <div class="card card-{polarity}"><span class="card-num">{a_num2}</span><span class="card-name">{name_zh}</span></div>
      <div class="card-arrow">→</div>
      <div class="card card-{polarity}"><span class="card-num">{a_num3}</span><span class="card-name">{name_zh}</span></div>
    </div>
  </div>

  <div class="choice-divider"><span>VS</span></div>

  <div class="choice-option">
    <h3 class="choice-label label-b">B. {optionB_text}</h3>
    <div class="spread-layout spread-three">
      <div class="card card-{polarity}"><span class="card-num">{b_num1}</span><span class="card-name">{name_zh}</span></div>
      <div class="card-arrow">→</div>
      <div class="card card-{polarity}"><span class="card-num">{b_num2}</span><span class="card-name">{name_zh}</span></div>
      <div class="card-arrow">→</div>
      <div class="card card-{polarity}"><span class="card-num">{b_num3}</span><span class="card-name">{name_zh}</span></div>
    </div>
  </div>
</div>
```

```css
.choice-option { margin-bottom: 6mm; }
.choice-label {
  text-align: center;
  font-size: 12pt;
  margin-bottom: 3mm;
}
.label-a { color: #0C447C; } /* ink-blue variant */
.label-b { color: #6B2F1A; } /* terracotta variant */
.choice-divider {
  text-align: center;
  margin: 6mm 0;
  position: relative;
}
.choice-divider span {
  display: inline-block;
  padding: 2mm 6mm;
  background: var(--border);
  border-radius: 4pt;
  font-size: 14pt;
  font-weight: 500;
  color: var(--stone);
  letter-spacing: 2pt;
}
```

---

## Interpretation Body Pages

### Chapter Template

Each analysis dimension gets its own chapter section.

```html
<section class="chapter">
  <h2 data-short="{chapter_short_title}">{chapter_title}</h2>

  <!-- Interpretation paragraphs -->
  <p>{body_text_paragraph_1}</p>
  <p>{body_text_paragraph_2}</p>

  <!-- Card combination callout -->
  <blockquote class="combination">
    <p class="combo-label">{card1_name} + {card2_name}</p>
    <p>{combination_meaning}</p>
  </blockquote>

  <!-- Key takeaway -->
  <div class="takeaway">
    <p>{key_insight}</p>
  </div>
</section>
```

### Chapter CSS

```css
/* Chapters flow continuously; first h2 is flush, subsequent h2s have generous top margin */
.chapter h2 {
  string-set: section-title attr(data-short);
  font-size: 16pt;
  font-weight: 500;
  color: var(--brand);
  margin-top: 10mm;
  margin-bottom: 4mm;
  border-bottom: 1pt solid var(--border);
  padding-bottom: 2mm;
}
/* First chapter after cover has no extra top space */
.chapter:first-of-type h2 { margin-top: 0; }
.chapter p {
  font-size: 10.5pt;
  line-height: 1.55;
  letter-spacing: 0.3pt;
  color: var(--near-black);
  margin-bottom: 3mm;
  text-align: justify;
}
.combination {
  margin: 4mm 0;
  padding: 3mm 5mm;
  background: var(--border-soft);
  border-left: 3pt solid var(--brand);
  border-radius: 0 4pt 4pt 0;
}
.combo-label {
  font-size: 10pt;
  font-weight: 500;
  color: var(--brand);
  margin-bottom: 1mm;
}
.takeaway {
  margin-top: 6mm;
  padding: 4mm 6mm;
  background: var(--brand);
  color: #f5f4ed;
  border-radius: 4pt;
  font-size: 11pt;
  line-height: 1.5;
}
.takeaway p { color: inherit; }
```

---

## Interpretation Chapter Structure by Spread Type

**Page break rule:** Each chapter (h2 section) should start on its own page via `style="break-before: page"`. This ensures clean page boundaries — every analytical perspective opens a fresh page, and no chapter heading is orphaned at the bottom of a preceding page. The cover + card grid already has `break-after: page`, so the first interpretation chapter begins naturally on page 2.

Add to each chapter section:
```html
<section class="chapter" style="break-before: page;">
```

If a chapter would occupy less than 50% of its page when standing alone, either expand it or merge it with the preceding chapter (removing the break-before) to share a page. But prefer expansion over merging — each analytical perspective deserves its own space.

### 1-Card Yes/No
Single chapter:
- **Verdict & Nuance**: Overall judgment + card meaning applied to question + subtle nuances

### 2-Card
Single chapter:
- **Combined Meaning**: Card 1+2 as a single sentence, overall meaning, practical guidance

### 3-Card
Three chapters:
1. **組合解讀 · Chain Reading** — Pair 1+2, then 2+3, then all three together
2. **整體意義 · Overall Meaning** — Synthesized message of the three cards
3. **提醒與建議 · Guidance** — Practical takeaway

### 5-Card
Three chapters:
1. **核心主題 · Core Theme** — Center card (position 3) as the heart of the matter
2. **組合鏈讀 · Chain Reading** — Pairs: 1+2, 2+3, 3+4, 4+5
3. **整體走向 · Overall Trajectory** — All 5 as one connected narrative + guidance

### 9-Card Box Spread
Five chapters:
1. **時間軸 · Time Axis** — Past (col 1: 1,4,7), Present (col 2: 2,5,8), Future (col 3: 3,6,9)
2. **三層意識 · Three Layers** — Conscious (row 1: 1,2,3), Reality (row 2: 4,5,6), Subconscious (row 3: 7,8,9)
3. **十字法 · Cross Method** — Core (pos 5), Cross arms (pos 2,4,6,8), Corners (pos 1,3,7,9)
4. **關鍵組合 · Key Combinations** — Notable card pairs and clusters
5. **整體解讀 · Overall Synthesis** — All 9 cards woven together

### A-or-B Choice
Three chapters:
1. **A 選項 · Option A** — Cards 1+2, 2+3 chain for Option A
2. **B 選項 · Option B** — Cards 1+2, 2+3 chain for Option B
3. **比較與傾向 · Comparison** — Side-by-side analysis + tendency + final reminder

---

## Page Balance Rules

Every interpretation page must be well-balanced. Before finalizing the HTML, run through this checklist:

### Rule 1: No page more than 50% blank

A4 printable area is approximately 170mm × 257mm. After accounting for the cover+cards page, each interpretation page must have text/content filling at least 50% of the printable area.

**How to check**: Estimate the total height of all content (paragraphs, blockquotes, headings) on each page. If a page's content occupies less than half the available vertical space, it fails this rule.

**Fix**: Expand the thin chapter(s) with additional reflection paragraphs or extended takeaways until each page is at least 50% filled.

### Rule 2: Page breaks at chapter headings (h2) — preferred

The cleanest approach is to give each analytical perspective its own page. Add `style="break-before: page"` to every chapter section. This ensures:
- Each analytical angle starts fresh at the top of a page
- No chapter heading is ever orphaned at a page bottom
- The reader can flip through the reading like chapters in a book

**Exception**: If a chapter on its own would occupy less than 50% of a page, either:
- Expand the chapter to fill 50%+ (preferred), or
- Remove the break-before so it shares a page with the next chapter, merging two thin sections

### Rule 3: Never split content mid-paragraph

Page breaks should NEVER split a paragraph mid-sentence. They should fall at:
- Chapter headings (h2) — ideal; always safe
- Between paragraphs — acceptable
- After a blockquote or takeaway box — acceptable

**NEVER split**:
- A paragraph across two pages (mid-sentence split is forbidden)
- A combination blockquote across two pages
- A takeaway box across two pages

Using break-before on every chapter (Rule 2) naturally avoids all of these — each chapter starts clean and its content cannot be split.

### Spread-specific guidance

- **Yes/No and 2-card** spreads: single chapters. Ensure the chapter fills at least 50% of its page.
- **3-card spreads**: 3 chapters. Each chapter should stand alone on a page. 提醒與建議 may need expansion.
- **5-card spreads**: 3 chapters. Each chapter should stand alone. 整體走向 may need expansion.
- **9-card Box spreads**: 5 chapters. Ample content. Each analytical perspective naturally fills 50%+ alone.
- **A-or-B Choice spreads**: 3 chapters. The 比較與傾向 comparison chapter often needs expansion to stand alone.

---
