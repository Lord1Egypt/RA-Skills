---
name: outline-revision-annotator
description: Use when comparing a revised PDF outline, script, treatment, beat sheet, season map, or character bio against an older DOCX/PDF version and you need a high-signal change report plus visible PDF markup for structural additions or rewrites. 当需要对比新版 PDF 大纲、剧本、人物小传、季纲、分集梗概等与旧版 DOCX/PDF 版本，并生成只标注结构性新增或重写的高信号差异报告与可见 PDF 标注时使用；也用于 AI 刚改完这些内容后自动补一份新的对比标注版 PDF。
license: MIT
---

# Outline Revision Annotator

Compare a new outline/script PDF with an older baseline, then produce:

- a UTF-8 markdown report
- a DOCX report generated from that markdown
- an annotated PDF with visible yellow note boxes in the page margin

This skill is for structural revision review, not line editing.

## Invocation Hooks

### Explicit hook

- `$outline-revision-annotator`

### English trigger phrases

- compare revised outline PDF with old DOCX
- compare new and old script versions
- annotate structural changes in PDF
- generate an annotated diff PDF
- mark only structural additions or rewrites
- compare character bio versions
- create a high-signal change report

### 中文触发词

- 对比新旧大纲
- 对比新版 PDF 和旧版 DOCX
- 对比剧本改动
- 对比人物小传版本
- 生成对比报告
- 生成标注版 PDF
- 结构性改动
- 只标新增和重写
- 差异标注
- 对比标注版

### Auto-follow hook

Run this skill automatically after the agent itself edits any of the following:

- outline
- script
- treatment
- beat sheet
- season map
- episode breakdown
- character bio
- role profile

Automatic follow-up applies when all of these are true:

- there is an older baseline version to compare against
- the revised draft is already a PDF, or can be exported to PDF in the current environment
- the user did not explicitly opt out of comparison output

When the auto-follow hook fires, generate a fresh:

- `compare_report.md`
- `compare_report.docx`
- annotated comparison PDF

If no baseline exists, or the revised draft cannot be turned into a PDF, say what is missing and stop.

中文规则：

- 当 AI 自己刚改完大纲、剧本、人物小传、季纲、分集梗概等内容后，如果存在旧版本基线，并且新版可获得 PDF，就自动触发本 skill
- 自动补产物时，不需要等用户再次提醒“再生成一份对比版”
- 如果缺旧版基线，或当前环境无法拿到新版 PDF，就明确说明缺什么，不要假装已完成

## Use This Skill For

- Story bibles, season outlines, beat sheets, treatments, scripts, and character bios
- `new.pdf` versus `old.docx` review workflows
- `new.pdf` versus `old.pdf` review workflows when the old version is also a PDF
- Chinese-language documents where PDF popup comments often render as garbled text
- Deliverables that need to be readable without clicking annotation popups

## Do Not Use It For

- punctuation or wording polish
- paragraph-level copy edits that do not change story function
- literal redline review
- mark-everything diffs

## Qualification Rule

Mark only changes that alter structure or story function:

- new season engine, thematic spine, or professional framework
- new antagonist, institutional pressure line, or evaluation thread
- a character arc rewritten to serve a different dramatic job
- ending reset from a closed loop to a next-season hook
- a case line upgraded from emotional texture to ethical or institutional conflict

Do not mark:

- sentence rewrites with the same dramatic function
- softened or intensified phrasing
- richer detail that does not change structure

## Workflow

### 1. Make sure the revised draft exists as PDF

If the agent has just edited a DOCX, Markdown, or other text source, first export or obtain a revised PDF. The renderer marks the revised PDF, not the editable source file.

### 2. Extract the sources

Run the helper script first. It produces plain text and page/block maps for the new PDF, plus plain text for the old baseline.

- Windows commands: [references/windows.md](references/windows.md)
- macOS commands: [references/macos.md](references/macos.md)

### 3. Compare semantically

Read the extracted text and decide which changes are structural. Then author two files:

- `compare_report.md`
- `annotation_manifest.json`

Manifest schema and examples: [references/manifest-schema.md](references/manifest-schema.md)

### 4. Render the final deliverables

Run the same script in `render` mode. It will:

- create an annotated PDF with visible margin boxes
- copy the markdown report as UTF-8
- convert the markdown report into DOCX
- write a normalized manifest copy into the output folder

### 5. Visually verify the PDF

Open the annotated PDF and check:

- the right-side yellow box text is visible without clicking
- Chinese text is not garbled
- note boxes do not cover the source paragraph
- only structural changes were marked

If something is wrong, read [references/troubleshooting.md](references/troubleshooting.md).

## Non-Negotiable Rules

- On Windows PowerShell, never pipe Chinese Python source directly into `python -`. Save a real UTF-8 `.py` file and run the file.
- Do not rely on popup PDF comments for Chinese review notes. Write visible note boxes into the page margin.
- If a change is stylistic rather than structural, leave it unmarked.
- Prefer an ASCII fallback filename if a downstream tool or browser tab cannot handle Chinese filenames cleanly.
- If the auto-follow hook fired, do not silently skip the compare PDF. Either generate it or state the concrete blocker.

## Deliverables Checklist

- `annotated.pdf`
- `compare_report.md`
- `compare_report.docx`
- `annotation_manifest.normalized.json`

## Script Entry Points

The bundled script is:

- `scripts/build_outline_diff_outputs.py`

Supported modes:

- `extract`: dump source text and PDF block maps
- `render`: build the annotated PDF and report outputs

## What the Script Does Not Decide

The script is deterministic. The agent still decides:

- which changes count as structural
- which blocks should be grouped into one note
- how to phrase the comparison report
- how to phrase each yellow-box explanation

Keep that judgment in the agent. Keep extraction and rendering in the script.
