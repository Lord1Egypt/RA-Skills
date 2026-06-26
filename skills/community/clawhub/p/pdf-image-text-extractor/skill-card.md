## Description: <br>
从图片或 PDF 文档中识别并提取文字内容，支持多种图片格式和 PDF 文件，自动判断是否包含文字并保留原始格式输出结构化结果。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to extract readable text from uploaded images and PDFs, preserve basic document structure, and optionally produce Markdown output for review or reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Extracted text from sensitive documents may appear in the chat or in a Markdown file when saved. <br>
Mitigation: Use only documents whose contents are appropriate for the active agent session and storage location. <br>
Risk: Image OCR and complex PDF layout extraction can be incomplete or inaccurate. <br>
Mitigation: Review extracted text against the source document before using it for decisions, records, or downstream automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redfox-data/pdf-image-text-extractor) <br>
- [Skill instructions](SKILL.md) <br>
- [PDF text extractor script](scripts/pdf_text_extractor.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown text or JSON script results with extracted text, page count, status, and errors] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save extracted content as a Markdown file when requested by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
