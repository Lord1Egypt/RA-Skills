## Description: <br>
从图片或 PDF 文档中识别并提取文字内容，支持多种图片格式和 PDF 文件，自动判断是否包含文字并保留原始格式输出结构化结果。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuanyi-github](https://clawhub.ai/user/yuanyi-github) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to extract editable text from uploaded images and text-based PDFs, preserving structure as Markdown when possible. It is suited for office document handling, academic note-taking, content reuse, and scripted PDF extraction workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The PDF extraction script contacts a third-party usage endpoint when it runs. <br>
Mitigation: Review, remove, or block that telemetry before processing sensitive documents. <br>
Risk: Extracted Markdown can become a persistent copy of source document text. <br>
Mitigation: Store saved extraction results only where appropriate and delete them when no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuanyi-github/image-text-extractor) <br>
- [README.md](artifact/README.md) <br>
- [README.en.md](artifact/README.en.md) <br>
- [PDF extraction script](artifact/scripts/pdf_text_extractor.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, files, guidance] <br>
**Output Format:** [Markdown text for image results and JSON-wrapped Markdown for PDF extraction results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [PDF extraction returns success, text, page_count, and error fields; saved results may create Markdown files when requested.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
