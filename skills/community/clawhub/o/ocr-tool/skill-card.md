## Description:

This skill helps agents extract text from images with Tesseract OCR, with examples for multilingual and financial screenshot workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuzhengmcc-debug](https://clawhub.ai/user/liuzhengmcc-debug)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and analysts use this skill to extract text from screenshots, charts, reports, and document images. It is especially oriented toward Chinese and English OCR and optional review of OCR-derived financial entities, stock codes, and metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OCR output can misread names, stock codes, numbers, or financial metrics.

Mitigation: Verify extracted text and any financial interpretation against the source image or authoritative records before relying on it.

Risk: Batch and Telegram-style examples can process private or many local images if copied directly.

Mitigation: Limit input directories, confirm files before processing, and avoid running bulk OCR on sensitive images without approval.

Risk: Chinese or other non-English extraction depends on installed Tesseract language data.

Mitigation: Install and test the required language packs before using multilingual OCR workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuzhengmcc-debug/skills/ocr-tool)
- [Tesseract tessdata language data](https://github.com/tesseract-ocr/tessdata)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell and Python code examples; scripts can emit plain text OCR output and console summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local Tesseract installation and appropriate language packs for non-English OCR.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
