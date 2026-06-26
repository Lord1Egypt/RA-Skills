---
name: ppt-generator
description: Generate professional .pptx presentations from any topic, uploaded documents, or reference materials. Supports custom PPT templates (filled via python-pptx, not XML editing). Works with any LLM configured in OpenClaw. Real chart rendering, smart content chunking, guided conversation flow.
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins: ["python3", "node"]
      pip: ["markitdown[pptx]", "pypdf", "python-pptx"]
      npm: ["pptxgenjs"]
---

# PPT Generator Skill

Generate polished `.pptx` presentations using the LLM configured in OpenClaw.  
No external PPT API required — everything runs locally.

---

## Phase 0 — Environment Check (First-Time Setup)

**Run once after installing the skill, before anything else.**

```bash
python3 scripts/check_env.py
```

The script checks all required and optional dependencies and prints a clear report:

```
══════════════════════════════════════════════════════
  PPT Generator Skill — Environment Check
══════════════════════════════════════════════════════
  ✅  Python 3.9+      (3.11.4)
  ✅  Node.js          (v20.11.0)
  ✅  npm              (10.2.4)
  ✅  pptxgenjs        (installed)
  ✅  markitdown       (0.4.1)
  ✅  pypdf            (4.2.0)
  ✅  python-pptx      (0.6.23)
  ⚠️   LibreOffice      (not found)
  ⚠️   pdftoppm         (not found)
──────────────────────────────────────────────────────

  ⚠️  OPTIONAL — QA features will be unavailable:

  ▸ LibreOffice  — Optional, needed for QA visual inspection
      $ sudo apt install libreoffice       # Ubuntu/Debian
      $ brew install --cask libreoffice    # macOS

  ▸ pdftoppm  — Optional, needed for QA visual inspection
      $ sudo apt install poppler-utils     # Ubuntu/Debian
      $ brew install poppler               # macOS
══════════════════════════════════════════════════════
```

If required (❌) items are missing, exact platform-specific install commands are shown. Fix all required items before proceeding.

**Auto-install missing Python packages:**
```bash
python3 scripts/check_env.py --fix
```

**Machine-readable output (for CI / automated setup):**
```bash
python3 scripts/check_env.py --json
```

---

## Phase 1 — Requirements Gathering

**Do not run any scripts yet.** First collect everything needed through a short conversation.

### Fast-path — Skip questions when info is already provided

Before asking questions, check whether the user's first message already contains sufficient information. If **at least two** of the following can be inferred from their message, skip the corresponding question steps and proceed directly to Phase 2:

| Info needed | Example signals | Maps to |
|-------------|-----------------|---------|
| Purpose/topic | "AI 趋势", "年度总结", "产品发布" | `{purpose}`, `{raw_topic}` |
| Content source | Uploaded files, or detailed description | `{uploaded_files}` or `{raw_topic}` |
| Slide count or style | "10 页", "科技风", "简约风" | `{slide_count}`, `{style}` |

**Example:** User says "帮我做一个 10 页的 AI 趋势科技风 PPT" → purpose=科技主题, raw_topic=AI 趋势, slide_count=10, style=未来科技. Skip to Phase 2 style confirmation with pre-filled values.

**If information is insufficient**, proceed with the question steps below.

### Step 1.1 — Understand purpose and topic

Ask the user:

> 请问这个 PPT 的主题和用途是什么？比如：
> - 📚 学术报告 / 论文答辩
> - 📊 工作汇报 / 季度总结 / 年终总结
> - 🎓 培训课程 / 教学课件
> - 💼 商业提案 / 投资路演
> - 🚀 产品发布 / 项目介绍
> - 🎨 活动策划 / 创意方案
> - 其他（请描述）

Record the answer as `{purpose}`.

### Step 1.2 — Collect content and reference materials

Ask the user:

> 请提供这次 PPT 的具体内容或参考资料，可以是：
> - 直接描述主题要点（文字说明）
> - 上传文档（支持 .txt / .md / .pdf / .docx / .pptx / .csv / .json）
> - 两者都有也没问题，内容越详细，PPT 质量越高

Wait for the user's response:
- Text description → record as `{raw_topic}`
- Uploaded files → record as `{uploaded_files}`
- Both → use both

### Step 1.3 — Ask about PPT template

Ask the user:

> 您有现成的 PPT 模板文件吗？
> - **有** → 请上传（.pptx 格式）
> - **没有** → 我来为您推荐合适的风格

**If a .pptx file is uploaded**, ask a follow-up:

> 请问这个 .pptx 文件的用途是：
> - 🎨 **模板文件** — 保留它的视觉风格（背景、配色、字体、版式），填入新内容
> - 📄 **参考内容** — 提取其中的文字内容作为素材，视觉风格另行选择

Record the answer as `{pptx_role}`: `"template"` or `"content"`.

---

## Phase 2 — Style and Structure

### If no template: suggest style (Step 2.1)

Run style analysis from what was collected in Phase 1:

```bash
# Topic description only:
python3 scripts/suggest_style.py --query "{raw_topic}"

# Uploaded files only:
python3 scripts/analyze_content.py {uploaded_files} > content_analysis.json
python3 scripts/suggest_style.py --content-file content_analysis.json

# Both:
python3 scripts/analyze_content.py {uploaded_files} > content_analysis.json
python3 scripts/suggest_style.py --query "{raw_topic}" --content-file content_analysis.json
```

Present the suggestion to the user:

> 根据您的需求，推荐方案如下：
>
> | 项目 | 建议 |
> |------|------|
> | 风格分类 | {suggested_category} |
> | 预计页数 | {slide_count_estimate} 页 |
> | 建议章节 | {key_sections（逗号分隔）} |
>
> **配色方案（3 选 1）：**
>
> | # | 方案名 | 主色 | 辅色 | 强调色 |
> |---|--------|------|------|--------|
> | 1 | {palette_candidates[0].name} | ⬛ {primary} | ⬜ {secondary} | ◻ {accent} |
> | 2 | {palette_candidates[1].name} | ⬛ {primary} | ⬜ {secondary} | ◻ {accent} |
> | 3 | {palette_candidates[2].name} | ⬛ {primary} | ⬜ {secondary} | ◻ {accent} |
>
> **字体搭配：** 标题 {font_heading} / 正文 {font_body}
>
> 请选择配色方案（输入 1/2/3），或直接确认使用推荐方案 1。也可以告诉我需要调整的地方（换风格、增减页数等）。

Wait for confirmation. Record the chosen palette as `{palette_hex}` and update `{slide_count}` / `{style}` per feedback.

**Important:** After confirmation, add `"style_category": "{suggested_category}"` to the slide plan JSON (Step 3.2). This field controls which visual layout renderer is used during PPTX generation — each category produces a visually distinct slide structure.

**Style categories quick reference:**

| 分类 | 适合场景 |
|------|----------|
| 企业商务 | 商业提案、投资路演、季度汇报 |
| 未来科技 | AI/科技主题、数字化转型 |
| 年终总结 | 年度/季度/工作总结 |
| 扁平简约 | 数据报告、产品设计 |
| 中国风 | 传统文化、国学、非遗 |
| 卡通手绘 | 教学课件、培训、儿童内容 |
| 文艺清新 | 生活方式、旅行 |
| 文化艺术 | 展览、人文、艺术项目 |
| 创意趣味 | 头脑风暴、工作坊 |
| 学术研究 | 论文答辩、学术报告 |

### If template uploaded (pptx_role = "template"): analyze it (Step 2.2)

```bash
python3 scripts/analyze_template.py uploaded_template.pptx
```

Inform the user:

> 已分析您的模板文件，检测到：
> - 配色：primary=`{primary}`, secondary=`{secondary}`
> - 字体：标题={heading_font}，正文={body_font}
> - 可用版式（{n} 种）：{layout_names}
>
> 我将保留这套视觉风格，只需您确认大致的页数即可。

---

## Phase 3 — Content Analysis and PPT Generation

All information is now confirmed. Run scripts in sequence without further interruption.

### Step 3.1 — Analyze content files

```bash
python3 scripts/analyze_content.py {content_files} > content_analysis.json

# For large docs (>40k chars):
python3 scripts/analyze_content.py large_doc.pdf --max-chars 80000 > content_analysis.json

# Structure-only mode for very long docs:
python3 scripts/analyze_content.py large_doc.pdf --summary-only > content_analysis.json
```

If `truncated_files` is non-empty in the output, inform the user and offer `--max-chars` adjustment.

### Step 3.1b — Content sizing for LLM (token optimization)

Before sending content to the LLM, apply these rules to control token usage:

| Content size | Strategy | Expected tokens |
|-------------|----------|-----------------|
| < 5,000 chars | Send full content as-is | ~1.5k |
| 5,000 – 20,000 chars | Send content, strip structural summary appendix if present | ~3-6k |
| 20,000 – 40,000 chars | Send structural summary + first 5,000 chars of body content | ~3k |
| > 40,000 chars | Re-run with `--summary-only`, send summary only | ~1-2k |

**Implementation:** When reading `content_analysis.json`, check each file's `total_chars`. If content exceeds the threshold, extract only the needed portion before inserting into the LLM prompt. Do NOT blindly paste the entire `content` field into the prompt.

### Step 3.2 — Generate slide plan (LLM)

```
You are a professional presentation designer. Generate a complete slide plan in JSON format.

PRESENTATION PURPOSE: {purpose}

CONTENT SOURCES:
{content from content_analysis.json, or raw_topic if no files}

STYLE REQUIREMENTS:
- Category: {suggested_category}
- Palette: primary={primary_hex}, secondary={secondary_hex}, accent={accent_hex}
- Font heading: {font_heading}, Font body: {font_body}
- Tone: {suggested_tone}
- Target slides: {slide_count}
- Language: Match the language of the content sources

OUTPUT FORMAT — respond ONLY with valid JSON, no markdown fences:
{
  "title": "Presentation Title",
  "style_category": "{suggested_category}",
  "palette": {
    "primary": "HEX_NO_HASH",
    "secondary": "HEX_NO_HASH",
    "accent": "HEX_NO_HASH"
  },
  "font_heading": "Calibri",
  "font_body": "Calibri",
  "slides": [
    {
      "index": 1,
      "layout": "title",
      "title": "Main Title",
      "subtitle": "Subtitle / tagline / date",
      "body": [],
      "notes": "Speaker notes for this slide",
      "chart": null,
      "visual_hint": ""
    },
    {
      "index": 5,
      "layout": "content",
      "title": "Sales Performance 2024",
      "subtitle": "Year-over-year comparison",
      "body": ["Revenue grew 23% YoY", "NPS score reached 87"],
      "notes": "Emphasize the Q4 recovery story",
      "chart": {
        "type": "bar",
        "title": "Quarterly Revenue (万元)",
        "data": [
          {"label": "Q1", "value": 120},
          {"label": "Q2", "value": 145},
          {"label": "Q3", "value": 98},
          {"label": "Q4", "value": 200}
        ]
      },
      "visual_hint": ""
    },
    {
      "index": 8,
      "layout": "content",
      "title": "Team Highlights",
      "body": ["Cross-functional collaboration", "30% headcount growth"],
      "notes": "Show the team photo here",
      "chart": null,
      "visual_hint": "image:Team photo from 2024 annual offsite"
    }
  ]
}

LAYOUT TYPES:
- "title"      → Cover/conclusion, dark background (slide 1 and last slide)
- "section"    → Section divider, dark background (between major topics)
- "content"    → Standard slide: title + optional subtitle + bullets (max 8)
- "two-column" → Comparison split; body split left/right (max 10 total)
- "quote"      → Large pull quote; body[0] is the quote text (max 1)
- "stat"       → 1-3 big numbers; each body item: "Number|Label" e.g. "85%|Satisfaction" (max 3)

CHART FIELD — use for any slide with numeric data:
  chart.type:  "bar" | "line" | "pie" | "doughnut" | "area"
  chart.title: optional string shown above the chart
  chart.data:  array of {"label": string, "value": number}
               values must be plain numbers — no units, no % signs, no commas
               (e.g. use 85 not "85%" or "85万")
  Set chart to null when no chart is needed.
  When chart is present with body bullets, bullets go left and chart fills right.

VISUAL_HINT FIELD — image/icon placeholders only:
  "image:<description>"  → gray dashed placeholder box (photos, KV art, etc.)
  "icon:<name>"          → small colored accent shape
  ""                     → nothing
  DO NOT put chart data in visual_hint. Use the chart field instead.

RULES:
1. Every slide must have a clear, specific title
2. Body points: max 15 words each
3. Use varied layouts — avoid repeating "content" every slide
4. Use "section" dividers between major topic groups
5. First slide: layout "title". Last slide: "title" or "section"
6. NEVER use "#" prefix in hex colors — "1E2761" not "#1E2761"
7. index must be sequential starting from 1
8. Add chart field for slides with numeric data
9. Use visual_hint only for image/icon placeholders
10. Derive all content faithfully from the provided source materials
```

Save as `slide_plan_raw.json`.

### Step 3.3 — Validate

```bash
python3 scripts/validator.py --plan slide_plan_raw.json --out slide_plan.json 2>validation_report.json
cat validation_report.json
```

### Step 3.4 — Generate PPTX

**No template:**
```bash
python3 scripts/generate_ppt.py --plan slide_plan.json --output presentation.pptx
```

**With template:**
```bash
python3 scripts/generate_ppt.py \
  --plan slide_plan.json \
  --output presentation.pptx \
  --mode from-template \
  --template uploaded_template.pptx \
  --skip-validation
```

**Patch mode — modify specific slides without regenerating the full plan:**
```bash
python3 scripts/generate_ppt.py \
  --plan slide_plan.json \
  --output presentation.pptx \
  --patch '{"slides": [{"index": 3, "title": "Updated Title", "body": ["New bullet 1", "New bullet 2"]}]}'
```

Patch merges specified fields into matching slides by `index`. Unspecified fields and other slides are preserved. Use this when the user requests changes to specific slides — it avoids a full LLM re-generation of the slide plan.

### Step 3.5 — QA

```bash
python3 -m markitdown presentation.pptx
python3 -m markitdown presentation.pptx | grep -iE "\bx{3,}\b|lorem|ipsum|\bTODO"

# Visual inspection (requires LibreOffice + pdftoppm):
python3 scripts/office/soffice.py --headless --convert-to pdf presentation.pptx
rm -f slide-*.jpg && pdftoppm -jpeg -r 150 presentation.pdf slide
ls -1 "$PWD"/slide-*.jpg
```

---

## Full Flow at a Glance

```
Phase 0 ─── check_env.py ──────────────────── First install only
               │
Phase 1.1 ─── Ask: purpose & topic type
               │
Phase 1.2 ─── Ask: content / upload files
               │
Phase 1.3 ─── Ask: PPT template?
               │                    │
              YES                   NO
               │                    │
          Ask: template          Phase 2.1
          or content?            suggest_style.py
               │                 present → confirm
          template                    │
               │                      │
          Phase 2.2               confirmed
          analyze_template            │
          present info                │
               └──────────┬──────────┘
                           │
Phase 3 ─── analyze_content.py
               │
           LLM → slide_plan_raw.json
               │
           validator.py
               │
           generate_ppt.py
               │
           QA → output .pptx ✅
```

---

## Script Reference

| Script | Purpose | Key flags |
|--------|---------|-----------|
| `check_env.py` | Verify all dependencies (first install) | `--fix`, `--json` |
| `analyze_content.py` | Parse reference docs | `--max-chars`, `--summary-only` |
| `analyze_template.py` | Extract template design system | — |
| `suggest_style.py` | Infer style from content | `--lang`, `--slides` |
| `validator.py` | Sanitize LLM slide plan | `--out`, `--strict` |
| `generate_ppt.py` | Build PPTX (both modes) | `--mode`, `--template`, `--skip-validation`, `--patch` |
| `template_builder.py` | Fill template via python-pptx | `--template`, `--plan`, `--output` |
| `chart_builder.py` | chart dict → PptxGenJS chart code | (imported by generate_ppt.py) |

---

## Design Principles

- **Every data slide needs a chart** — use the `chart` field for any numeric data
- **Dark title slides, light content slides** — "sandwich" structure
- **Vary layouts** — never repeat the same layout 3+ times in a row
- **Left-align body text**, center titles only
- **Minimum 0.5" margins** — never crowd edges
- **Never use accent lines under titles** — use whitespace instead
- **NEVER `#` prefix in hex colors** — PptxGenJS file corruption
- **NEVER reuse PptxGenJS option objects** — use `makeShadow()` factory pattern

---

## Platform Notes

This skill works in both **OpenClaw** (agent framework with external LLM) and **AI IDEs** (Claude Code, Cursor, Windsurf, etc.).

### Script paths

All script references use relative paths (`scripts/xxx.py`). When running in an AI IDE, resolve them relative to the skill installation directory. Example:

```bash
# If skill is installed at /path/to/ppt-generator/
python3 /path/to/ppt-generator/scripts/suggest_style.py --query "AI trends"
```

### Step 3.2 in AI IDEs

In Claude Code, Cursor, and similar environments, the agent itself IS the LLM. Step 3.2's slide plan prompt should be treated as a self-instruction: generate the JSON directly and write it to `slide_plan_raw.json`. No external API call is needed.

### Dependency installation in sandboxed environments

Some AI IDEs run in sandboxed containers. If `check_env.py --fix` fails due to permission issues, try:
```bash
pip install "markitdown[pptx]" pypdf python-pptx --break-system-packages --user
```

---

## Dependencies

```bash
# Python (required)
pip install "markitdown[pptx]" pypdf python-pptx --break-system-packages

# Node.js (required)
npm install -g pptxgenjs

# System (optional — QA visual inspection only)
# Linux:  sudo apt install libreoffice poppler-utils
# macOS:  brew install --cask libreoffice && brew install poppler
# Windows: see check_env.py output for download links
```
