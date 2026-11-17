## Description:

从图片或 PDF 文档中识别并提取文字内容，支持多种图片格式和 PDF 文件，自动判断是否包含文字并保留原始格式输出结构化结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External users, office workers, students, researchers, content creators, and agents use this skill to extract readable text from uploaded images or PDFs and optionally save the extracted content as Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Extraction results are instructed to append an unrelated promotional external link.

Mitigation: Review generated Markdown before sharing or publishing, and remove promotional content when it is not appropriate for the document workflow.

Risk: OCR and scanned-PDF behavior may be less complete than advertised.

Mitigation: Verify extracted text against the source document, especially for scanned pages, low-quality images, tables, or complex layouts.

Risk: Saved Markdown outputs can become persistent copies of text from user documents.

Mitigation: Process only documents approved for this workflow and handle generated Markdown according to the document's confidentiality requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/pdf-image-text-extractor)
- [README.en.md](artifact/README.en.md)
- [README.md](artifact/README.md)
- [PDF extraction script](artifact/scripts/pdf_text_extractor.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses, optional Markdown files, and JSON results from the PDF extraction script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [PDF output may include page separators and page counts; image extraction depends on the hosting agent's image-reading capability.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
