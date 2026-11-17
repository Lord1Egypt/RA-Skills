---
name: make-knowledge-cards
version: 1.0.0
author: WorkBuddy User
description: "Convert pasted articles, local Markdown/TXT files, or PDF documents into 5-8 concise knowledge cards. Each card captures one key concept with a title, core knowledge summary, brief explanation, and an example or self-test question. Trigger when the user asks to make knowledge cards, create study cards, summarize into cards, or provides an article or PDF for card-based learning. Do NOT use for web scraping, Anki export, or graphical interfaces."
agent_created: true
---

# Make Knowledge Cards

## Overview

Transform articles, pasted text, local Markdown/TXT files, or PDF documents
into structured knowledge cards for efficient review and self-testing. Each
card isolates a single knowledge point with enough context to understand and
recall it independently.

## When to Use

- User pastes an article and asks to generate knowledge cards
- User provides a local `.md`, `.txt`, or `.pdf` file path for card generation
- User explicitly requests "knowledge cards", "study cards", or "flashcards"
  from text content
- User wants to review key points from a long-form article or PDF document
  in a card format

## Limitations

The following are NOT supported and should be declined with a clear explanation:

- **Web scraping**: Do not fetch URLs or scrape web pages. If a URL is provided,
  ask the user to paste the article text instead.
- **Scanned PDFs**: If a PDF contains only scanned images (no embedded text),
  extraction will fail. Ask the user to run OCR first and provide the text.
- **Encrypted PDFs**: If a PDF is password-protected, ask the user to decrypt
  it first.
- **Anki export**: Do not generate `.apkg` files or Anki-compatible formats.
- **Graphical UI**: Do not render cards as images or interactive interfaces.
  Output is plain Markdown text only.

## Dependencies

PDF text extraction requires the `pypdf` Python library. Install it before
using the PDF feature:

```
pip install -r skills/make-knowledge-cards/scripts/requirements.txt
```

If `pypdf` is not installed and the user provides a PDF, inform them of the
dependency and offer to install it, or ask them to paste the text manually.

## Workflow

### Step 1 — Acquire Source Text

1. If the user pastes text directly, use it as the source.
2. If the user provides a local file path:
   - **`.md` or `.txt`**: Read the file content using the Read tool.
   - **`.pdf`**: Extract text using the bundled script. Run:
     ```
     python scripts/extract_pdf.py "<pdf_file_path>"
     ```
     The script outputs extracted text to stdout. If the exit code is non-zero,
     check stderr for the error message:
     - Exit code 2: File not found — ask the user to verify the path.
     - Exit code 3: PDF is encrypted — ask the user to decrypt it first.
     - Exit code 4: No text extracted — the PDF may be scanned images only.
       Ask the user to run OCR and provide the text.
   - **Other formats** (`.docx`, `.html`, etc.): Not supported. Ask the user
     to paste text or provide a `.md` / `.txt` / `.pdf` file.
3. If the user provides a URL, explain the limitation and ask for pasted text
   or a local file.

### Step 2 — Analyze Content

1. Read the full source text carefully before extracting any knowledge points.
2. Identify the article's main topic and logical structure.
3. Distinguish between:
   - **Core knowledge**: Concepts, principles, definitions, causal relationships,
     and methods that are central to the article's purpose.
   - **Supporting detail**: Examples, anecdotes, statistics, and background
     context that illustrate but do not constitute standalone knowledge.
   - **Filler**: Transitional phrases, repetition, and tangential remarks.
4. Deduplicate: When the same concept appears multiple times, merge into a
   single card.

### Step 3 — Select Knowledge Points

1. Extract 5-8 knowledge points from the core knowledge identified in Step 2.
2. Apply these selection criteria in order of priority:
   - **Importance**: Does the point matter to the article's central argument or
     learning objective?
   - **Independence**: Can the point be understood without reading other cards?
   - **Non-redundancy**: Is this point already covered by another card?
3. If the source contains fewer than 5 distinct important knowledge points,
   produce fewer cards. Do not pad with low-value or repetitive content.
4. If the source contains more than 8 important points, select the 5-8 most
   central ones. Briefly note that some points were omitted at the end of the
   output.
5. For very long articles (over 5000 words), still produce at most 8 cards.
   Focus on the article's overarching themes and key conclusions rather than
   individual section details.
6. If the user explicitly requests a specific number of cards outside the 5-8
   range, honor the request but warn when the requested count exceeds the
   available distinct knowledge points.

### Step 4 — Build Each Card

For every knowledge point, construct a card with exactly these four fields:

#### Card Fields

| Field | Description | Guidelines |
|-------|-------------|------------|
| **Title** | Short phrase naming the knowledge point | Concise noun phrase or concept name (2-8 words); no full sentences |
| **Core Knowledge** | One or two sentences stating the key fact or principle | Direct and precise; must be derivable from the source text; no fabricated details |
| **Explanation** | 2-4 sentences unpacking the knowledge point | Clarify cause, mechanism, context, or nuance; stay faithful to the source; do not introduce external information |
| **Example / Self-Test** | Either a concrete example or a self-test question | Priority: (1) if the source provides a relevant example, adapt it as "Example:"; (2) otherwise, write a self-test question whose answer requires recalling the core knowledge, labeled as "Self-Test:". Never invent examples not grounded in the source text. |

#### Card Formatting

Render each card as a Markdown block:

```markdown
---

### Card N: [Title]

**Core Knowledge:** [1-2 sentence summary]

**Explanation:** [2-4 sentence elaboration]

**[Example / Self-Test]:** [content]
```

### Step 5 — Quality Check

Before outputting, verify each card against this checklist:

- [ ] **Faithfulness**: Every statement in the card is supported by the source
      text. No fabricated facts, numbers, names, or examples.
- [ ] **Singularity**: The card covers exactly one knowledge point. If two
      concepts are bundled, split into two cards or choose the more important
      one.
- [ ] **Independence**: The card is understandable without reading other cards.
      No references like "as mentioned in Card 3".
- [ ] **No duplication**: No two cards repeat the same point with different
      wording.
- [ ] **Appropriate count**: Total cards are 5-8 (or fewer if the source
      genuinely lacks enough distinct important points).

### Step 6 — Output

1. Output all cards in sequence using the format from Step 4.
2. After the last card, add a brief summary line:

   ```markdown
   ---
   *Generated N knowledge cards from [source description].*
   ```

3. If knowledge points were omitted due to the 8-card limit, append:

   ```markdown
   *Note: Some secondary points were omitted to stay within the card limit.*
   ```

## Output Language

- If the source text is in Chinese, produce cards in Chinese.
- If the source text is in English, produce cards in English.
- If the source is mixed, match the dominant language.

## Example Output

```markdown
---

### Card 1: 间隔重复原理

**Core Knowledge:** 间隔重复是一种学习策略，通过逐渐增加复习间隔来强化长期记忆。

**Explanation:** 该方法基于遗忘曲线理论——记忆会随时间自然衰退，但在即将遗忘时复习能有效巩固记忆。每次成功回忆后，下一次复习的间隔适当延长，从而以最少的时间投入维持记忆。

**Self-Test:** 为什么在"即将遗忘时"复习比"频繁复习"更高效？

---

### Card 2: 主动回忆

**Core Knowledge:** 主动回忆是指学习者主动从记忆中提取信息，而非被动地重新阅读材料。

**Explanation:** 研究表明，主动提取信息的过程本身就能强化记忆通路。与反复阅读相比，自我测试或尝试回忆能显著提升长期记忆效果，即使回忆时出现错误。

**Example:** 读完一段文章后合上书，尝试用自己的话复述核心观点，而不是再读一遍。

---

*Generated 2 knowledge cards from "高效学习方法" article excerpt.*
```
