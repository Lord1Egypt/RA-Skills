## Description: <br>
Converts document attachments into Markdown for text-only agents, using a local MarkItDown MCP server for text-bearing files and an optional OpenAI-compatible OCR layer for scanned PDFs or images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keepyaoung](https://clawhub.ai/user/keepyaoung) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when a text-only agent receives PDFs, Office files, spreadsheets, HTML, CSV, JSON, XML, EPUB, ZIP files, scanned PDFs, or images and needs readable Markdown content for answering, summarizing, quoting, or storage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/keepyaoung/markitdown-skill-for-non-multimodal-agent) <br>
- [MarkItDown fork referenced by the skill](https://github.com/Self-made-Orange/markitdown) <br>
- [Microsoft MarkItDown referenced by the skill](https://github.com/microsoft/markitdown) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional OCR requires OPENAI_API_KEY and a vision-capable model. Security evidence marks the release suspicious and recommends installing only if the publisher is trusted.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
