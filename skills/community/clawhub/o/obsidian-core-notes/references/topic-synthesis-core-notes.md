# Topic Synthesis Core Notes

Use this reference before creating or rewriting `专题综合.core.md` across an Obsidian vault.

## Core Distinction

`资料索引.md` answers: "What is in this folder?"

Lightweight `专题综合.core.md` answers: "What are the direct sources and version clues?"

V3-like `专题综合.core.md` answers: "What does this topic mean, what judgment should survive, and what reusable patterns or actions follow from the sources?"

Do not bulk-promote all folders to V3-like synthesis. A shallow folder should stay as a source map.

## Candidate Criteria

Prioritize folders that meet several of these conditions:

- Contains a main strategy, research, architecture, project, or meeting-summary document.
- Has multiple versions, drafts, meeting records, or progress reports that show an evolution of thinking.
- Supports business or technical judgment, not only personal credentials, raw attachments, logs, exports, or generated run output.
- Can produce reusable methods, templates, components, role boundaries, or action plans.
- Has enough readable source text from Markdown, TXT, DOCX, or PPTX to support evidence-based synthesis.
- Belongs to an active knowledge domain such as AI transformation, algorithms, risk control, business opportunity, data quality, AI platform, AI coding, meeting assistant, Agent engineering, or department planning.

Deprioritize folders that are only:

- Raw receipts, identity/certificate files, photos, OCR intermediate output, generated artifacts, dependency folders, model output folders, or vendor resource bundles.
- One-off data drops without an interpretable project or method.
- Research indexes that need a different "research digest" standard unless the user explicitly asks for that.

## Required V3-Like Structure

A deep topic note should include:

```markdown
---
core_note_type: topic_synthesis
core_note_schema: topic-synthesis-v3-like
synthesis_depth: deep
generated_at: "YYYY-MM-DD"
source_folder: "path/from/vault/root"
source_file_count: N
tags:
  - tag
---
<!-- CORE_FILE_NOTE_V1 -->

# 专题综合: Topic Name

## 筛选结论
Why this folder deserves deep synthesis.

## 一句话总纲
The durable thesis.

## 来源资料与历史版本
Source table with links, file types, and roles.

### 版本线索
Version/date/final/draft cues.

## 核心判断
Judgments that should survive beyond the folder.

## 内容结构地图
The topic architecture.

## 关键内容整理
Evidence-backed source synthesis.

## 可复用模式 / 模板 / 组件
Reusable operating assets.

## 推进建议
Concrete next actions.

## 待深化问题
Decisions or evidence gaps.

## 相关入口
Links to folder index and related topic notes.
```

Keep the generated marker so the note can be safely refreshed or cleaned only when explicitly requested. Add `core_note_schema: topic-synthesis-v3-like` so validation and future searches can distinguish deep synthesis from lightweight source maps.

## Workflow For Broad Vault Work

1. Run `scan` to understand vault size.
2. Run `topic-candidates` to rank candidate folders.
3. Manually review the top candidates and exclude irrelevant high-volume folders.
4. Rewrite only selected `专题综合.core.md` files with the V3-like structure.
5. Leave other topic notes as lightweight source maps or folder indexes.
6. Back up generated notes before aggressive overwrite or deletion.
7. Validate generated markers and run a wikilink check for rewritten topic notes.

## Judgment Rules

- Do not infer conclusions from unread PDFs or spreadsheets; list them as sources unless text was actually extracted.
- Prefer source-backed synthesis over filename-only summaries.
- Preserve source provenance and version history in the note, but do not let version history dominate the note.
- When a folder contains multiple project artifacts, summarize the project logic: objective, evolution, current judgment, reusable pattern, action, and open issue.
- For organizational topics, record responsibility boundaries explicitly. Example: an algorithm team may own patterns, components, model evaluation, and reusable development paradigms while data governance remains a separate responsibility.
