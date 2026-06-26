---
name: medical-record-translator
description: |
  Use when users need structure-preserving translation of medical records, lab reports,
  discharge summaries, prescriptions, pathology/radiology reports, or similar documents.
  Main artifact must be Chinese-first, original-preserving, and doctor-readable.
  Triggers on mentions of medical translation, 病历翻译, report translation, or when users
  share PDF/image medical documents.
---

# Medical Record Translator

Produce a structure-preserving translation artifact, not a summary report.

## Core Rules

1. Classify each PDF as `text PDF` or `scanned PDF` before translation.
2. Always derive source document blocks first, then translate block-by-block.
3. Maintain strict 1:1 mapping: one source block -> one translated block.
4. Preserve structure types:
   - tables remain tables
   - key-value regions remain key-value regions
   - free text remains free text blocks
5. Output constrained Markdown artifact (not free-form narrative/report writing).
6. Chinese-first reading is required, with original source text immediately available for each block.
7. Do not add summary-style sections, terminology tables in the main artifact, or explanatory rewrite sections.
8. Do not split/merge source paragraphs or regions for readability rewriting.

## Operational Workflow

1. Ingest file and classify:
   - `text PDF`: digital text layer is extractable.
   - `scanned PDF`: content is image-based or text layer is unreliable.
2. Route by type:
   - `text PDF` path: extract text + structural hints first, then map blocks.
   - `scanned PDF` path: use a vision-capable model first, perform region detection, then recover region text and block types.
3. Build block model from detected structure.
4. Translate with one-to-one block alignment and structure preservation.
5. Emit constrained Markdown per output contract.

## Scanned PDF Mandatory Rules

1. For scanned PDFs, parsing must start with a vision-capable model.
2. Perform region detection before translation (table regions, key-value regions, paragraph regions, headers, footers as applicable).
3. Translate only after region text recovery and block typing are complete.
4. Mark uncertainty at the smallest useful scope:
   - uncertain cell ownership -> mark that cell or minimal table span
   - uncertain key-value field value -> mark that field only
   - uncertain phrase -> mark that phrase only
5. Do not promote local uncertainty to document-level warnings unless clinically necessary.

## Output And Quality References

Follow these documents directly instead of re-specifying them here:

- `references/output-contract.md`
- `references/block-model.md`
- `references/quality-checklist.md`
- `references/terminology.md`

## Export

```bash
python3 skills/medical-record-translator-publish/scripts/render_translation.py \
  skills/medical-record-translator-publish/examples/sample_translation.md \
  --output-dir skills/medical-record-translator-publish/examples/rendered-sample

python3 skills/medical-record-translator-publish/scripts/check_rendered_pdf.py \
  skills/medical-record-translator-publish/examples/rendered-sample/sample_translation.pdf
```

## Privacy Disclaimer

> ⚠️ **隐私提醒 | Privacy Notice**
>
> 医疗病历包含敏感个人信息。在使用本技能前，请注意：
> - 请勿上传包含你不愿分享的个人健康信息的文档
> - 翻译内容将发送至AI服务进行处理
> - 如有隐私顾虑，建议使用本地部署的AI服务或人工翻译
>
> Medical records contain sensitive personal information. Before using this skill:
> - Do not upload documents with health information you don't want to share
> - Translation content will be sent to AI services for processing
> - If you have privacy concerns, consider locally-deployed AI or human translators
