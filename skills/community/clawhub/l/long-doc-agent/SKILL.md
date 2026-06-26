---
name: long-doc-agent
license: MIT
metadata:
  version: "3.3.0"
  category: document-generation
  triggers:
    - "write feasibility report"
    - "write proposal"
    - "multi-chapter"
    - "parallel writing"
    - "agent write document"
description: >
  Multi-Agent collaborative system for writing ultra-long feasibility study reports.
  Phase 0 Requirements → Phase 1 Planner Outline → Phase 2 Parallel Sub-Agent Writing →
  Phase 2.5 Cross-Chapter Consistency Review → Phase 3 Integrator Final Output (styled docx).
  Core files: integrate_report.py (integration/CLI), parallel_tracker.py (parallel progress tracking).
---

# Ultra-Long Feasibility Report Multi-Agent Collaborative Writing v3.3

## Changelog (v3.3)

- ✅ Table parsing fully fixed (`_flush_table` not calling `_parse_md_table` caused character-by-character splitting)
- ✅ Colorful chapter headings officially launched (H1 deep navy full-row band / H2 medium blue block / H3 light blue left bar)
- ✅ Styled tables launched (deep blue header + white text + alternating row colors)
- ✅ Key callout boxes launched (【关键】【注意】【优势】【风险】【数据】 color-coded cards)
- ✅ Cover style enhanced (tech-digital style deep ocean blue full-screen background + white text)
- ✅ Cover/Contents/Executive Summary title bars all colored
- ✅ Fixed `cover_style` integer vs string comparison preventing cover from applying
- ✅ Fixed `RGBColor.from_string()` instead of `eval` to avoid type errors

## Core Capabilities

- **Multi-Agent Parallel**: Up to 5 sub-agents writing concurrently, doubled efficiency
- **Incremental Updates**: Chapters with unchanged content are skipped, faster processing
- **Beautiful Formatting**: Auto-generated cover, table-style TOC, colorful chapter headings, key callout boxes, styled tables
- **Feishu RAG**: Auto-search Feishu knowledge base to supplement reference materials
- **6 Cover Styles**: Switch freely to suit different scenarios

---

## File Structure

```
skill_dir/
├── SKILL.md                    # This file
├── integrate_report.py          # Core engine: parse/ integrate/CLI
├── parallel_tracker.py          # Parallel progress tracking
└── references/                 # Sub-process reference documents
    ├── phase0_guide.md         # Phase 0 requirements confirmation flow
    ├── phase1_guide.md         # Planner prompt template
    ├── phase2_guide.md         # Sub-Agent prompt template
    ├── table_format_guide.md   # Markdown table format specification
    └── bug_fix_guide.md        # Bug troubleshooting & forced rebuild
```

> **First-time setup**: Ensure the `F:/agent/chapters/` directory exists.

---

## Pipeline Routing

```
User Task
├─ First writing request ("I want to write xxx"/"help me write a feasibility report")
│   → Phase 0 Requirements → Phase 1 Planner
│
├─ Outline exists, request to start writing
│   → Phase 2 Parallel Sub-Agents
│
├─ A chapter needs modification
│   → Small change: directly edit F:/agent/chapters/0X-xxx.txt
│   → Large change: regenerate that chapter
│
├─ All chapters done, request docx generation
│   → Phase 2.5 Review → Phase 3 Integrator
│
├─ Independent small proposal (2~5 chapters, no existing chapters dependency)
│   → Write Markdown directly → make_docx.py to generate styled docx
│   → See: references/bug_fix_guide.md "make_docx.py Mode"
│
└─ Just need to check progress/glossary/reference materials
    → Direct CLI commands
```

---

## Phase 0: Requirements Confirmation

Confirm 4 items in order; all confirmed → Phase 1:

1. **Writing Topic**: document type / audience / style / special constraints
2. **Background Information**: project background / construction goals / industry context
3. **Reference Materials** (most important):
   - A. Local file path or paste directly
   - B. Feishu document (RAG search)
   - C. Paste content directly
   - D. Not provided for now
4. **Outline Confirmation**: After planner outputs outline, user chooses A.Start / B.Adjust / C.Cancel

> More reference materials → more business-aligned content. See `references/phase0_guide.md` for details.

---

## Phase 1: Planner

**Input**: Phase 0 topic / background / reference materials

**Execute**:
```bash
python integrate_report.py glossary
```
Auto-generates `plan.json` + `plan_outline_snapshot.md`

> Full prompt template in `references/phase1_guide.md`

**After completion, send WeChat notification** (using `message` tool, channel=`openclaw-weixin`):

```
📋 Report Outline Generated

📌 《[Report Topic]》
📊 Chapters: [X] chapters
🔍 Industry: [Industry Field]

✅ Reply "start writing" once the outline is confirmed — the system will launch parallel creation!
```

---

## Phase 2: Parallel Sub-Agents

**Execution flow** (fully automatic, no manual confirmation):
1. Display outline / current batch status (display only, no waiting)
2. `python parallel_tracker.py clear` to clear previous batch state
3. Start up to 5 concurrent sub-agents (`sessions_spawn`), automatically execute all batches
4. `python parallel_tracker.py wait` to monitor in background until this batch is complete
5. After completion, automatically run `python integrate_report.py convert-batch`

**Sub-Agent prompt template**: see `references/phase2_guide.md`

**After each batch completes, send WeChat notification** (using `message` tool, channel=`openclaw-weixin`):

```
✅ Batch [X] Chapter Writing Complete!

📖 Completed: [Done]/[Total] chapters
📝 This batch:
   • [Chapter 1 Title]
   • [Chapter 2 Title]
   • [Chapter 3 Title] (if any)

⏳ Next batch: [Next batch chapter list]
(Automatically proceeds to next batch, no manual confirmation needed)
```

- Small change: directly edit `F:/agent/chapters/0X-xxx.txt`, save and regenerate
- Large change: re-trigger sub-agent to rewrite, replacing the original file

---

## Phase 2.5: Cross-Chapter Consistency Review

```bash
python integrate_report.py check
```
Review numerical indicator consistency and terminology uniformity (对照 glossary.json)

**After review completes, send WeChat notification** (using `message` tool, channel=`openclaw-weixin`):

```
🔍 Consistency Review Complete

✅ Terminology uniformity: OK
✅ Numerical indicators: consistent
✅ Cross-chapter references: no conflicts

📄 Proceeding to final integration phase...
```

---

## Phase 3: Integrator Summary

```bash
python integrate_report.py
```

Auto-completes: parse chapters (error isolation) → update glossary → consistency review → generate styled docx

**After final completion, send WeChat notification** (using `message` tool, channel=`openclaw-weixin`):

```
🎉🎉🎉 Report Writing Complete! 🎉🎉🎉

📄 《[Report Topic]》
📊 Scale: [X] chapters / ~[Y] thousand characters
🎨 Cover Style: [Style Name]

✅ Styled report generated!
📁 File location: F:/agent/chapters/output/

Wenxin, full text ready for your review~
```

---

## Document Beautification Features (Auto-Applied)

Generated reports automatically include the following formatting effects (selected via `cover_style` field in `plan.json`):

1. **6 Cover Styles** — Edit `plan.json` → `cover_style` field (integer 1~6)
2. **Executive Summary** — Deep blue title bar (`#1F4E79`) background + white text + body indent
3. **Table-Style TOC** — Deep blue title bar + three-column entries (number/chapter/page)
4. **Colorful Chapter Headings**:
   - H1: Full-row deep navy background `#1F4E79` + white text Microsoft YaHei
   - H2: Medium blue background `#2E75B6` + white text
   - H3: Light blue background `#D6E4F0` + dark blue text + `▌` left bar
5. **Key Callout Boxes** — Auto-detect 【关键】【注意】【优势】【风险】【数据】 tags, render as color cards (background/white text/border)
6. **Styled Tables** — Header deep navy background `#1F4E79` + white text + alternating row colors (`#DEEAF6` / `#FFFFFF`)

---

## Cover Styles (6 Types)

Cover style specified via `cover_style` field in `plan.json` (integer, 1~6):

| # | Style Name | Features | Recommended For |
|---|------------|----------|-----------------|
| 1 | Classic Government | Deep navy top bar + gold accents | Government/state enterprise approval |
| 2 | Modern Minimalist | Left blue heavy block + right info | Tech/business reports |
| 3 | Business Elegant | Burgundy + centered progression | Consulting/investment bank reports |
| 4 | Tech Digital | Deep ocean blue fill + large white title | Internet/digital projects |
| 5 | Chinese Traditional | Forbidden City red + rice paper cream background | Traditional culture/state enterprise |
| 6 | Full Immersive | Deep ocean blue fill + large white title | Digital/tech projects |

> **Note**: `cover_style` value is integer (e.g., `4`), code automatically converts to string for comparison.

---

## CLI Command Reference

| Command | Description |
|---------|-------------|
| `python integrate_report.py` | Generate integrated report (full) |
| `python integrate_report.py convert-batch` | Batch convert to docx |
| `python integrate_report.py convert-one <in> <out>` | Single chapter to docx |
| `python integrate_report.py check` | Consistency review |
| `python integrate_report.py glossary` | Glossary generation/update |
| `python integrate_report.py ref show` | View reference materials |
| `python integrate_report.py ref clear` | Clear reference materials |
| `python integrate_report.py preview [chapter prefix]` | Preview chapter summary |
| `python integrate_report.py feishu-search <query>` | Search Feishu knowledge base |
| `python parallel_tracker.py show` | View writing progress |
| `python parallel_tracker.py wait` | Block & monitor (Ctrl+C to stop) |
| `python parallel_tracker.py clear` | Clear tracking state |

> **Switching cover style**: Edit `cover_style` field (integer 1~6) in `F:/agent/chapters/plan.json`, then regenerate.
> After modifying code: delete `.pyc` files under `__pycache__` + `content_hashes.json` to force rebuild.

---

## State Files

| File | Description |
|------|-------------|
| `F:/agent/chapters/plan.json` | Chapter metadata |
| `F:/agent/chapters/glossary.json` | Terminology table |
| `F:/agent/chapters/reference_material.txt` | Raw reference materials |
| `F:/agent/chapters/plan_outline_snapshot.md` | Outline snapshot |
| `F:/agent/chapters/content_hashes.json` | Incremental cache (delete to force rebuild) |
| `F:/agent/chapters/writing_tracker.json` | Parallel progress tracking |
| `F:/agent/chapters/config.json` | Cover style and other config |

---

## Critical Rules

### Markdown Table Format (Sub-Agents Must Follow)

See `references/table_format_guide.md` for full spec

Key points:
- Separator row must be `|---|---|---|` (leading/trailing `|` required)
- All rows must have same column count as header
- Cell content should avoid containing `|` (use `～` or `-` for ranges)

### Force Rebuild (Must Do Both Steps After Code Changes)

After modifying `integrate_report.py`, must delete both files for new code to take effect:

```bash
# 1. Delete .pyc cache (required after code changes)
del "C:\Users\Administrator\AppData\Roaming\LobsterAI\SKILLs\long-doc-agent\__pycache__\integrate_report.cpython-311.pyc"

# 2. Delete incremental hash (or incremental mode skips everything)
del F:\agent\chapters\content_hashes.json

# 3. Regenerate
python integrate_report.py
```

### Known Bugs Fixed (For Reference)

See `references/bug_fix_guide.md`, including:
- `_flush_table` not calling `_parse_md_table` causing character-by-character table splitting
- `cover_style` integer vs string comparison preventing cover from applying
- `eval` RGB color assignment type error
- `.pyc` cache causing new code to not take effect
- `RGBColor` using index access `rgb[0]/rgb[1]/rgb[2]` instead of `.red/.green/.blue`
- `add_cover()` setting `section.margin=0` causing body text to have no margins
- `PermissionError` when docx file is open in WPS → auto-add `_v2` suffix
- `write` tool has 50KB line limit → large scripts must be written in chunks

---

## References

| File | Content |
|------|---------|
| `references/phase0_guide.md` | Phase 0 requirements confirmation full flow & scripts |
| `references/phase1_guide.md` | Planner full prompt template & plan.json format |
| `references/phase2_guide.md` | Sub-Agent full prompt template (incl. table format warnings) |
| `references/table_format_guide.md` | Markdown table format spec, common errors & examples |
| `references/bug_fix_guide.md` | Bug troubleshooting & forced rebuild procedures |
