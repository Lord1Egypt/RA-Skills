# Review Note Style Guide (V2)

## General Tone

- **Concise and direct** — No decorative language, no marketing-speak
- **Function-oriented** — Every sentence exists to help the user improve
- **Honest about errors** — Sugar-coating doesn't help learning; be blunt about what went wrong
- **Chinese as primary language** — English terms, vocabulary, and passage quotes preserved as-is

## V2 Design System

The review notes use a modern card-based design with CSS Variables, Lucide SVG icons, and a purple gradient hero header. All icons come from Lucide (CDN: `unpkg.com/lucide@latest`), no emoji in the HTML.

### CSS Class Reference

| V2 Class | Purpose | Notes |
|----------|---------|-------|
| `.container` | Main content wrapper | `max-width: 960px` |
| `.hero` | Purple gradient header | Contains `.book-tag`, `h1`, `.subtitle`, `.stats-row` |
| `.hero-nav` | Top-right nav buttons | Links to index + bilingual page |
| `.book-tag` | Source tag (e.g. "剑6 · Test 1 · Passage 1") | Inside `.hero` |
| `.stats-row` > `.stat-item` | Score stats in hero | `.stat-value` + `.stat-label` |
| `.time-badge` | Time spent badge | Inside `.subtitle` |
| `.card` | Generic content card | White bg, rounded corners, shadow |
| `.card-title` | Card header with icon | `.icon-box` + text |
| `.status-chip.good` | Progress highlight | Green icon, success theme |
| `.status-chip.warn` | Alert / core problem | Amber icon, warning theme |
| `.error-item` | Error analysis card | Red left border, contains sub-components |
| `.q-header` | Question header row | `.q-num` + `.badge` tags |
| `.badge-fill` | Blue info badge | Question type tag |
| `.badge-type` | Gray badge | Sub-type tag |
| `.answer-compare` | Answer comparison row | `.ans-box.mine` + `.ans-box.correct` |
| `.quote-block` | Passage quote | Gray bg, `.quote-label` header |
| `.analysis-block` | Error cause analysis | `.section-label` + `<ul>` |
| `.lesson-box` | Lesson learned | Purple-tinted bg |
| `.data-table` | Data tables (vocab, synonyms) | Dark header (`#1e1b4b`), rounded |
| `.overview-table` | Answer overview table | Accent-colored header |
| `.problem-table` | Problem summary table | Red header |
| `.freq-stars` | IELTS frequency stars | Lucide `<i data-lucide="star">` with `.empty` class |
| `.takeaway` | Action items card | Purple gradient bg, white text |
| `.result-correct` | Correct answer indicator | Green text + check icon |
| `.result-wrong` | Wrong answer indicator | Red text + x icon |

### Key CSS Variables

```css
:root {
  --bg: #f0f2f5;        /* Page background */
  --card: #ffffff;       /* Card background */
  --text: #1d1d1f;       /* Primary text */
  --text-secondary: #6b7280;  /* Secondary text */
  --accent: #4f46e5;     /* Brand purple */
  --accent-light: #eef2ff;    /* Light purple bg */
  --success: #059669;    /* Green (correct) */
  --danger: #dc2626;     /* Red (wrong) */
  --warning: #d97706;    /* Amber (alert) */
  --info: #2563eb;       /* Blue (info) */
  --border: #e5e7eb;     /* Border color */
  --radius: 16px;        /* Card radius */
  --radius-sm: 10px;     /* Small radius */
}
```

### Icon Usage

All icons use Lucide SVG via `<i data-lucide="icon-name"></i>`. Common icons:
- `home` — Index link
- `book-open` — Bilingual page link / passage quote
- `clock` — Time spent
- `trending-up` — Progress highlight
- `alert-triangle` — Core problem alert
- `x-circle` — Error section header
- `x` — Wrong answer
- `check` — Correct answer
- `brain` — Error analysis
- `lightbulb` — Lesson learned
- `repeat` — Synonym section
- `book-marked` — Vocabulary section
- `alert-circle` — Problem summary
- `zap` — Action items
- `star` — IELTS frequency rating (`.freq-stars`)

## Section-by-Section Guidelines

### Hero Header
- Purple gradient with `.book-tag`, title, subtitle with time badge
- `.stats-row` shows score breakdown (总分 / 填空 / 判断 / 匹配)
- `.hero-nav` top-right with links to index and bilingual page

### Progress & Alert Chips
- `.status-chip.good` — Always find at least 1 positive point, even in a bad score
- `.status-chip.warn` — ONE sentence identifying the biggest scoring pattern
- Be specific: "T/F/NG 前 4 道全对" is good; "有进步" is bad
- Bad example: "阅读理解能力有待提升" ← too vague
- Good example: "3道判断题全错，均为 NG 误判为 FALSE——没区分「没提到」和「相反」" ← specific and actionable

### Error Analysis Blocks (`.error-item`)
- `.q-header` with question number and type badges
- `.answer-compare` showing user's wrong answer vs correct answer
- `.quote-block` with passage quote and location label
- `.analysis-block` with error cause bullets
- `.lesson-box` with single-sentence takeaway
- Error cause should reference the error taxonomy category

### Correct Answer Brief Analysis
For correct answers on non-trivial questions (especially T/F/NG), include within the answer overview table or as a brief note. Keep to 2-3 lines showing the synonym mapping. Purpose: reinforce synonym recognition.

### Synonym Table (`.data-table`)
- Only include synonyms relevant to the questions (not every synonym in the passage)
- Columns: 原文表达 | 题目表达 | 出处
- Include the question number for cross-reference

### Vocabulary Table (`.data-table`)
- Include phonetic transcription (IPA) after the word
- Part of speech before the definition
- IELTS frequency rating is mandatory — use `.freq-stars` with Lucide star icons
- "真题出现" column tracks which real tests the word has appeared in
- Skip low-frequency specialist terms unless they caused an error

### Problem Summary (`.problem-table`)
- Red header table
- Columns: 问题类型 | 具体表现 | 对应错题 | 改进方法

### Takeaway Card (`.takeaway`)
- Purple gradient background, white text
- Numbered action items with `<strong>` in gold (`#fde68a`)
- Include synonym additions as `<code>` items

### Fill-in-the-blank Readback Checklist
When fill-in errors exist, include as a `.status-chip.warn`:
1. 语法检查 — 放回去读一遍
2. 词性检查 — 空格前后决定词性
3. 语义检查 — 答案和题目主题匹配
4. 字数检查 — 不超过限制

### Per-question-type Progress Trend
When 3+ passages of the same question type exist, include a trend table inside a `.status-chip.good`:
- Bold the current passage row
- Add ↑/↑↑/↓ indicators
- After the table, 2-3 sentences of specific analysis

### Test Scorecard (Full Test)
- Generated when user completes all 3 passages
- Use `.data-table` format
- Format: P1/P2/P3 scores, 总计/40, 总用时, 雅思分数
- Band score from `references/score-band-table.md`

### Cumulative Progress Table
- Generated when 2+ full tests exist
- Rows ordered chronologically
- After the table: accuracy trend, speed analysis, strategy advice, per-passage pattern

## Naming Convention

### Review notes
`剑X-TestX-PassageX-TopicKeyword复盘.html`

Examples:
- `剑4-Test3-Passage1-街头青年信贷复盘.html`
- `剑6-Test1-Passage1-澳洲体育成功复盘.html`

### Bilingual pages
`剑X-TestX-PassageX-TopicKeyword双语对照.html`

Examples:
- `剑5-Test4-Passage3-光对动植物影响双语对照.html`
- `剑6-Test1-Passage1-澳洲体育成功双语对照.html`

## Formatting Rules

- Use the V2 CSS classes documented above (NOT the deprecated V1 classes)
- Icons use Lucide SVG (`<i data-lucide="..."></i>`), not emoji
- Tables use `.data-table`, `.overview-table`, or `.problem-table` styling
- Keep `break-inside: avoid` on cards and error items for clean PDF output
- All pages load Lucide from CDN at the end of `<body>`:
  ```html
  <script src="https://unpkg.com/lucide@latest"></script>
  <script>lucide.createIcons();</script>
  ```

### Deprecated V1 Classes (DO NOT USE)

These classes belong to the old V1 template and should NOT appear in new reviews:

| Deprecated Class | V2 Replacement |
|-----------------|----------------|
| `.correct` | `.result-correct` |
| `.wrong` | `.result-wrong` |
| `.tag-yes` / `.tag-no` / `.tag-ng` | `.badge` with appropriate styling |
| `.alert-box` | `.status-chip.warn` |
| `.good-box` | `.status-chip.good` |
| `h1/h2/h3` section headers | `.card-title` with `.icon-box` |
| `blockquote` for quotes | `.quote-block` with `.quote-label` |
| `max-width: 800px` | `max-width: 960px` via `.container` |
| `#4A90D9` hardcoded blue | `var(--accent)` CSS variable |
