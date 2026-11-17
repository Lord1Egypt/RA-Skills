---
name: in_the_cards_lenormand
description: |-
  Interpret Lenormand card readings from freeform spreads or compatible Stargazer’s Oracle prompts, persist each interpretation as structured JSON plus human-readable Markdown, and generate polished A4 PDF, web, social-card, or long-image products. Uses a three-phase workflow: parse → interpret and save → generate. Supports six spread types, combination-first reading, bilingual Chinese/English output, natural-language retrieval, and regeneration of past readings.
  Triggers on: "牌间 / In the Cards / Stargazer 解读 / 帮我解读这个牌阵 / 雷诺曼解读 / Lenormand reading / Stargazer prompt / 帮我解牌 / 帮我解读 / interpret this spread / 生成解读 PDF / 列出最近的解读 / 把上次的解读 / 生成网页版 / 生成社交卡片 / 上次的解读 / 之前的解读 / 請為我解讀 / 幫我解讀 / 每日運勢 / 今日運勢 / 我想透過 Lenormand / 透過 Lenormand / 二選一 / Lenormand 卡牌占卜 / consult the Lenormand cards / compare them with Lenormand / daily fortune / read my Lenormand / deciding between two options".
version: 3.5.2
agent_created: true
---

# In the Cards · 牌间

**Lenormand Interpreter**

Interpret Lenormand card spreads, persist them as reusable data, and generate visual products — A4 PDF, web pages, social cards, or long images — by copying seed HTML files and filling in placeholders. Accepts freeform spreads and prompts from [Stargazer’s Oracle](https://lenor.star-oracle.app/).

## Architecture

```
Lenormand Prompt
(Stargazer-compatible)
    │
    ▼
[Phase 1] Parse → structured card data
    │
    ▼
[Phase 2] Interpret → save reading (JSON + MD) to output/readings/
    │
    ▼
[Phase 3] Generate products from saved reading
           ├── A4 PDF (default, Kami style)
           ├── Web Page (standalone interactive HTML)
           ├── Social Card (1080×1440 carousel, 3:4)
           └── Long Image (full-page PNG screenshot of web page)
```

Every reading is saved before product generation. Saved readings can be regenerated into any product type later.

## When to Use

**First-time reading:** User pastes a Lenormand spread or compatible Stargazer prompt and asks for interpretation.
→ Run Phase 1 → Phase 2 → Phase 3 (generate default A4 PDF).

**Product regeneration (post hoc):** User references a past reading and asks for a different product type.
E.g., "把上次的解读生成社交卡片" / "用 #3 解读生成网页版" / "列出最近的解读".
→ Skip Phase 1–2, load the saved reading JSON, run Phase 3 with the requested product type.

## Phase 1: Parse the Prompt

> **AGENT — REQUIRED BEFORE PARSING:**
> Execute these two file reads now, in order, before doing anything else:
> 1. Open and read `references/spread-parsing.md` in full
> 2. Open and read `references/lenormand-cards.md` in full
>
> Do NOT begin parsing the prompt until both files have been read and their contents are in your context. Using training knowledge as a substitute is not permitted.

Read `references/spread-parsing.md` for detailed parsing rules. Extract structured data:

1. **Strip universal instruction prefix** — the "You are a traditional Lenormand reader..." / "你是一位傳統 Lenormand 占卜師..." block before `---`
2. **Detect language** (ZH/EN) from `【問題】` / `Question:` / `Spread:`; fallback: CJK character ratio.
3. **Detect spread type**: `yesno-1` | `two` | `three` | `five` | `nine` | `choice`
4. **Extract fields**: question, date, cards with positions, verdict (yes/no), option A/B texts (choice)
5. **Resolve card names** against `references/lenormand-cards.md`
6. **Output** a structured data object

> **AGENT — PHASE 1 CHECKPOINT:**
> Before proceeding to Phase 2, emit the following block exactly as shown, filled with the parsed values. Do not continue until this block is visible in your output.

```
PHASE 1 COMPLETE
─────────────────────────────
spread_type  : {yesno-1|two|three|five|nine|choice}
language     : {zh|en}
question     : {extracted question text, or "daily fortune" if null}
date         : {YYYY-MM-DD}
cards        :
  {position_label}: {card_number}. {card_name_zh} / {card_name_en}
  ... (one line per card)
verdict      : {YES/NO/MAYBE, or N/A}
option_a     : {text, or N/A}
option_b     : {text, or N/A}
─────────────────────────────
Proceeding to Phase 2.
```

## Phase 2: Interpret & Save

> **AGENT — REQUIRED BEFORE INTERPRETING:**
> If `references/lenormand-cards.md` is not already in your current context from Phase 1, open and read it now before writing any interpretation.
> Also open and read `references/template-a4-pdf.md` — you will need its chapter structure and page balance rules for Phase 2b and Phase 3.

### 2a. Interpret the Cards

#### Core Reading Principles

- **Combination-first**: Never list individual card meanings in isolation. Read adjacent cards as overlapping pairs (1+2, 2+3, 3+4...) that modify each other. The meaning of a card shifts based on its neighbors.
- **Noun + Modifier model**: The first card is the subject (noun), the second card modifies it (adjective/verb/adverb). Rider + Clover = "lucky news arriving." Clover + Rider = "a fleeting visitor."
- **Use modifier types systematically**: Each card has a `modifier_type` in `references/lenormand-cards.md`. When interpreting A+B, apply B's modifier type to A's core meaning. Example: A=Heart (love), B=Mountain (blocking modifier) → "Love blocked or delayed."
- **Check for negative modifiers**: 8 cards (Clouds, Snake, Coffin, Scythe, Whip, Mountain, Mice, Cross) darken adjacent cards. When one of these is the second card in a pair, the tone shifts darker regardless of the first card's polarity.
- **Neutral tone**: Stay faithful to Lenormand's traditional meanings. Do not push toward positivity or negativity — the tone emerges from the cards themselves. Avoid empty reassurance and unfounded pessimism.
- **Honesty**: The value of a reading lies in honesty, not in making the querent feel good or afraid.
- **Center dominance**: In odd-numbered linear spreads, the center card is the core theme.
- **Full-length interpretation**: The saved interpretation should be written at **PDF-ready length** — each chapter aiming for 4-5 paragraphs + takeaway (for 3-card/5-card spreads) or equivalent depth. The interpretation JSON stores the *full* version. Social card generation will compress this saved content.

#### Card Knowledge

Load `references/lenormand-cards.md` for each card's complete meaning (core, extended, career, love, health, person in both EN/ZH), keywords, polarity, modifier type, timing, and the systematic combination methodology. The modifier type system tells the agent HOW each card changes its neighbor — use this to synthesize pair meanings, rather than improvising from isolated keywords. Card data is sourced from [lenormand-oracle](https://github.com/jintianbaihe/lenormand-oracle) (MIT License).

#### Spread-Specific Interpretation Frameworks

**1-Card Yes/No:**
- State the verdict clearly (YES/NO/MAYBE)
- Interpret the card's meaning applied to the question
- Note any subtle nuances the binary verdict might miss

**2-Card:**
- Read the two cards as a single combination (1+2)
- Give the overall meaning as one connected sentence

**3-Card / Daily:**
- Chain adjacent pairs: 1+2, then 2+3
- Synthesize all three into one connected message
- End with a practical takeaway or "今日提醒" (daily reminder)

**5-Card:**
- Identify the center card (position 3) as the core theme
- Chain pairs: 1+2, 2+3, 3+4, 4+5
- Read all 5 as one connected narrative trajectory
- End with practical guidance

**9-Card Box Spread (3×3):**
Interpret from three perspectives:
1. **Time Axis** (columns) — Left column (1,4,7) = Past, Center column (2,5,8) = Present, Right column (3,6,9) = Future
2. **Three Layers** (rows) — Top row (1,2,3) = Conscious, Middle row (4,5,6) = Reality, Bottom row (7,8,9) = Subconscious
3. **Cross Method** — Core (position 5), Cross arms (2,4,6,8) = direct influences, Corners (1,3,7,9) = background/hidden factors
4. **Key Combinations** — Highlight notable card pairs and clusters
5. **Overall Synthesis** — All 9 cards woven into a unified reading

**A-or-B Choice:**
- Chain-read Option A's 3 cards (1+2, 2+3)
- Chain-read Option B's 3 cards (1+2, 2+3)
- Compare the two trajectories side by side
- Offer a tendency or caution, but respect that the final choice belongs to the querent

#### Output Format

Structure the interpretation as clear chapter sections with titles in the detected language. Use the chapter structure defined in `references/template-a4-pdf.md` for your spread type.

### 2b. Save the Reading

**Phase 2b is mandatory and must complete before Phase 3 begins.** Persist the reading
in two parallel files under `output/readings/`:

**1. Structured JSON** — `{reading_id}.json`

Follow the schema defined in `references/reading-schema.md`. The JSON must contain:
- `version`: `"3.0"`
- `reading_id`: `"{date}-{topic_slug}"` (e.g., `2026-06-20-写作方向`)
- `meta`: language, spread_type, spread_label, question, date, generated_at, source, topic_slug
- `cards`: array of card objects with position, card_id, names, polarity, position_label
- `interpretation`: summary + chapters array, each chapter with id, title, short_title, and sections (paragraph / combination / takeaway)
- `verdict`: (yesno-1 only) verdict + verdict_zh
- `optionA` / `optionB`: (choice only) option texts + card arrays

**2. Human-readable Markdown** — `{reading_id}.md`

A readable copy including:
```markdown
# {question}
**{spread_label}** · {date}

{summary}

## 抽出牌面
| 位置 | 牌 |
|------|-----|
| {position_label} | {number}. {name_zh} |

{for each chapter:}
## {chapter_title}

{paragraphs}

> **{combo_label}**: {combo_content}

> 💡 {takeaway}
```

**3. Update the index** — append to `output/readings/index.json`:

```json
{
  "reading_id": "2026-06-20-写作方向",
  "language": "zh",
  "spread_type": "three",
  "question": "我的写作方向应该是什么？",
  "date": "2026-06-20",
  "generated_at": "2026-06-20T21:35:00+08:00",
  "topic_slug": "写作方向",
  "card_names": ["騎士", "幸運草", "書"],
  "products_generated": []
}
```

**Confirm before continuing**: Both `{reading_id}.json` and `{reading_id}.md` must exist
on disk and the index must be updated. Only then proceed to Phase 3.

> **AGENT — PHASE 2 CHECKPOINT:**
> Before proceeding to Phase 3, confirm the following. Emit this block filled with actual values.

```
PHASE 2 COMPLETE
─────────────────────────────
reading_id   : {reading_id}
json saved   : output/readings/{reading_id}.json — {EXISTS|FAILED}
md saved     : output/readings/{reading_id}.md — {EXISTS|FAILED}
index updated: output/readings/index.json — {EXISTS|FAILED}
chapters     : {N} chapters in interpretation
summary      : {first 80 characters of summary}...
─────────────────────────────
Proceeding to Phase 3.
```

If any field shows FAILED, stop and fix the save operation before continuing.

## Phase 3: Generate Products

> **Hard gate — do not begin Phase 3 until Phase 2b is confirmed complete.**
> Verify that `output/readings/{reading_id}.json` exists and `output/readings/index.json`
> has been updated. If either file is missing, complete Phase 2b first. Never generate
> products from in-memory interpretation data that has not been persisted.

Products are generated from the saved reading JSON. The user may request one or more product types.
If no product type is specified, default to **A4 PDF**.

### Seed-Based Workflow

Instead of building HTML from scratch, **copy the seed HTML file** from `assets/`, then fill in placeholders:

1. **Copy seed** to `output/` with the appropriate filename
2. **Replace `{{PLACEHOLDER}}` markers** with data from the saved reading JSON:
   - `{{TITLE}}`, `{{DATE}}`, `{{SPREAD_LABEL}}` etc. → from `meta`
   - `{{CARD_N_SVG}}` → read SVG from `cards/card-{NN}-{slug}.svg`, strip `<defs>…</defs>`, paste inline
   - `{{CHAPTER_TITLE}}` / `{{CHAPTER_CONTENT}}` → from `interpretation.chapters[]`
   - `{{SUMMARY}}` → from `interpretation.summary`
3. **Delete unused spread templates** from the seed (keep only the one matching `spread_type`)
4. **For chapters**: duplicate the `<!-- CHAPTER_LOOP_START -->` block for each chapter
5. **Render** with the appropriate script

| Product | Seed file | Render script | Output name |
|---------|-----------|---------------|-------------|
| Product | Seed file | Render script | Output name |
|---------|-----------|---------------|-------------|
| `a4-pdf` | `assets/seed-a4-pdf.html` | `scripts/generate-pdf.js` | `lenormand-{spread}-{topic}-{date}.pdf` |
| `web-page` | `assets/seed-web-page.html` | — (self-contained) | `lenormand-web-{topic}-{date}.html` |
| `social-card` | `assets/seed-social-card.html` | `scripts/render-social-cards.js` | `lenormand-xhs-{topic}-{date}-NN.png` |
| `long-image` | `assets/seed-web-page.html` | `scripts/render-long-image.js` | `lenormand-web-{topic}-{date}.png` |

### 3a. A4 PDF (Default)

**Step 1 — Copy the seed file**
```bash
cp assets/seed-a4-pdf.html output/lenormand-{spread_type}-{topic_slug}-{date}.html
```
Do NOT write a new HTML file from scratch. You must copy the seed.

**Step 2 — Fill all placeholders**
Open `output/lenormand-{spread_type}-{topic_slug}-{date}.html`.
Replace every `{{PLACEHOLDER}}` marker using str_replace or sed, sourcing all values from the saved reading JSON at `output/readings/{reading_id}.json`.
Required replacements:
- `{{TITLE}}` → `meta.question`
- `{{DATE}}` → `meta.date`
- `{{SPREAD_LABEL}}` → `meta.spread_label`
- `{{SUMMARY}}` → `interpretation.summary`
- `{{CARD_N_SVG}}` for each card → inline SVG from `cards/card-{NN}-{slug}.svg` (strip outer `<defs>…</defs>`, inline inner content only, no nested `<svg><svg>`)
- `{{CHAPTER_TITLE}}` / `{{CHAPTER_CONTENT}}` per chapter → from `interpretation.chapters[]`

**Step 3 — Delete unused spread templates**
Remove all spread template blocks from the HTML except the one matching `meta.spread_type`.

**Step 4 — Duplicate chapter blocks**
Find the `<!-- CHAPTER_LOOP_START -->` marker. For each chapter after the first, duplicate the chapter block. Chapters 2 and beyond must have `style="break-before: page;"` on their container element.

**Step 5 — Render to PDF**
```bash
node scripts/generate-pdf.js output/lenormand-{spread_type}-{topic_slug}-{date}.html
```

**Step 6 — Validate**
```bash
node scripts/validate.js output/lenormand-{spread_type}-{topic_slug}-{date}.html --type a4-pdf
```
Exit code must be 0. If non-zero, fix all reported failures and re-run Step 5 before continuing.

**Step 7 — Record in index**
```bash
node scripts/manage-readings.js record-product {reading_id} --type a4-pdf
```

### 3b. Web Page

**Step 1 — Copy the seed file**
```bash
cp assets/seed-web-page.html output/lenormand-web-{topic_slug}-{date}.html
```

**Step 2 — Fill all placeholders**
Same process as 3a Step 2. Source all values from `output/readings/{reading_id}.json`.

**Step 3 — Validate**
```bash
node scripts/validate.js output/lenormand-web-{topic_slug}-{date}.html --type web-page
```
Exit code must be 0. Fix any failures before continuing.

**Step 4 — Record in index**
```bash
node scripts/manage-readings.js record-product {reading_id} --type web-page
```

### 3c. Social Card (1080×1440)

**Step 1 — Load and compress interpretation**
Open `output/readings/{reading_id}.json`. For each chapter, produce a compressed version:
- Max ~3 content blocks per card page (e.g. 2 combos + takeaway, or 3 short paragraphs + takeaway)
- Shorten sentences, merge redundant points, cut filler
- Never truncate mid-sentence — drop the weakest points instead
- Estimated total block height per page must be ≤ 1100px at 30px font

**Step 2 — Copy the seed file**
```bash
cp assets/seed-social-card.html output/lenormand-xhs-{topic_slug}-{date}.html
```

**Step 3 — Fill all placeholders**
Same process as 3a Step 2, using compressed interpretation for chapter content.

**Step 4 — Render to PNGs**
```bash
node scripts/render-social-cards.js output/lenormand-xhs-{topic_slug}-{date}.html
```

**Step 5 — Validate**
```bash
node scripts/validate.js output/lenormand-xhs-{topic_slug}-{date}.html --type social-card
```
Exit code must be 0. Fix any failures (overflow, thin pages, card sizing) and re-run Step 4 before continuing.

**Step 6 — Record in index**
```bash
node scripts/manage-readings.js record-product {reading_id} --type social-card
```

### 3d. Long Image (Full-Page PNG)

Generates a full-page PNG screenshot of the web page version. Useful for sharing on social media, messaging apps, or as a long single-image reading.

**Workflow**: Generate web page first (Phase 3b), then screenshot it.

**Step 1 — Generate web page (ensure Phase 3b is complete)**
If the web page HTML does not already exist, run Phase 3b Steps 1–2.

**Step 2 — Render to PNG**
```bash
NODE_PATH=/Users/1mether/.workbuddy/binaries/node/workspace/node_modules \
  /Users/1mether/.workbuddy/binaries/node/versions/22.22.2/bin/node \
  {{SKILL_ROOT}}/scripts/render-long-image.js output/lenormand-web-{topic_slug}-{date}.html
```
The script automatically derives the output path (`{same_name}.png`).

**Step 3 — Verify output**
Check that the PNG file exists and has non-zero size:
```bash
ls -lh output/lenormand-web-{topic_slug}-{date}.png
```

**Step 4 — Record in index**
```bash
node scripts/manage-readings.js record-product {reading_id} --type long-image
```

> **Note**: The full-page PNG inherits the web page's viewport width (720px). The height is determined by the page content length. For best results, run on a reading with all chapters filled. CSS `@media print` and page-specific styles are NOT applied — the PNG uses the screen layout.

### Generating Multiple Products

User may request multiple product types at once: "生成 PDF 和网页版". Generate each as described above.

## Product Regeneration (Post Hoc)

When the user references a past reading for a new product:

1. **Identify the reading**. Common triggers:
   - "上次的解读" / "latest reading" → `node scripts/manage-readings.js latest`
   - "列出最近的解读" → `node scripts/manage-readings.js list --limit 5`
   - "用 #3 解读" / "第三张解读" → list then load by index
   - "用 6月20号的解读" → search by date

2. **Load the reading JSON** from `output/readings/{reading_id}.json`

3. **Ask which product type** (if not specified in the user's request).
   Default to A4 PDF if the user only says "生成产品" without a type.

4. **Run Phase 3** with the loaded reading and requested product type.

## Bundled Resources

| Resource | Purpose | When to Load |
|----------|---------|-------------|
| `references/lenormand-cards.md` | 36-card database with MIT-licensed meanings (EN+ZH), modifier types, timing, negative modifier list, and systematic combination methodology | Phase 2 (always needed) |
| `references/spread-parsing.md` | Prompt parsing rules for all 6 spread types | Phase 1 |
| `references/design-system.md` | Shared design tokens, fonts, colors, card slugs | Phase 3 reference |
| `references/template-a4-pdf.md` | A4 PDF chapter structure & page balance rules | Phase 3a reference |
| `references/reading-schema.md` | JSON schema for saved readings | Phase 2b (saving) |
| `assets/seed-a4-pdf.html` | Copy-and-fill A4 PDF HTML skeleton | Phase 3a (copy to output/) |
| `assets/seed-web-page.html` | Copy-and-fill web page HTML skeleton | Phase 3b (copy to output/) |
| `assets/seed-social-card.html` | Copy-and-fill social card HTML skeleton | Phase 3c (copy to output/) |
| `scripts/generate-pdf.js` | Puppeteer: HTML → A4 PDF | Phase 3a |
| `scripts/manage-readings.js` | CLI: list, find, update reading index | Phase 2b, post-hoc regen |
| `scripts/render-social-cards.js` | Puppeteer: social card HTML → 1080×1440 PNGs | Phase 3c |
| `scripts/render-long-image.js` | Puppeteer: web page HTML → full-page PNG | Phase 3d |
| `cards/*.svg` | Geometric Silence 36-card deck | Phase 3a, 3c (SVG card faces) |
| `cards/previews/*.png` | PNG previews of all 36 cards | Quick reference |

## Output Directory Structure

```
output/
├── readings/
│   ├── index.json                     # Reading manifest
│   ├── 2026-06-20-写作方向.json       # Structured reading data
│   └── 2026-06-20-写作方向.md         # Human-readable copy
├── lenormand-three-写作方向-2026-06-20.pdf    # A4 PDF product
├── lenormand-web-写作方向-2026-06-20.html     # Web page product
├── lenormand-xhs-写作方向-2026-06-20-01.png   # Social card product (page 1)
└── lenormand-web-写作方向-2026-06-20.png      # Long image (full-page PNG)
```

## Deliverable Validation

Validation is run automatically via `node scripts/validate.js` at the end of each product generation step. See Phase 3a–3c for usage. All checks must pass (exit code 0) before presenting any product to the user.

## Edge Cases & Notes

- **Missing universal prefix**: Treat entire text as spread body if no `---` delimiter
- **Daily reading**: Auto-detected by `每日運勢`; question is null, generate "daily fortune" context
- **9-card significator**: Mark in card data if position 5 is noted as Significator
- **Card ambiguity**: Resolve both Chinese (騎士) and English (Rider) case-insensitively
- **Freeform (non-Stargazer) input**: If the input doesn't follow Stargazer format (no `---` delimiter, no Stargazer ZH/EN markers), still run Phase 1 language detection — the CJK fallback in `spread-parsing.md` will determine the output language. All Phase 2–3 rules apply as normal.
- **Language consistency**: Detect language FIRST from the prompt itself (via markers or CJK fallback). Do NOT override with user profile language preference. If Chinese prompt → all text in Chinese. English → all English. The interpretation must match the prompt's language, not the user's chat language.
- **Duplicate generation**: If a product type already recorded in index, still regenerate (overwrite) but log a note
- **Social card chapter count**: If a reading has only 1 chapter (yesno-1, two), produce a cover-only card (single 1080×1440 image)
- **Web page immutability**: Web pages are standalone and self-contained — they don't link back to the reading data
- **Long image prerequisite**: `long-image` depends on the web page already being generated (Phase 3b). If the user requests long image without specifying web page, silently generate both (web page first, then the screenshot).
- **Puppeteer Chromium sandbox**: The renderer scripts keep Chromium's sandbox **on** by default (shared logic: `scripts/chromium-args.js`). `--no-sandbox` / `--disable-setuid-sandbox` are added only when running as root or when `PUPPETEER_NO_SANDBOX=1` is set. If `page.setContent()` / `page.goto()` fail with "Requesting main frame too early!" in an environment where the sandbox cannot run, rerun with `PUPPETEER_NO_SANDBOX=1` — do not hardcode the flags.
- **HTML escaping**: When filling `{{PLACEHOLDER}}` markers in any seed template, HTML-escape user-derived text (the question, names, free-text notes) and generated interpretation prose — `&`, `<`, `>`, `"` — before substitution. The only unescaped substitutions are the template's own structural fragments (card SVGs, chapter markup the template defines).
