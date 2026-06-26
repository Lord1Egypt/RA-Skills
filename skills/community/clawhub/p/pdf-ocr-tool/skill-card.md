## Description: <br>
Intelligent PDF and image to Markdown converter using Ollama GLM-OCR with smart content detection for text, tables, and figures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TsukiSama9292](https://clawhub.ai/user/TsukiSama9292) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to convert PDFs and single images into structured Markdown through a local OCR workflow. It is suited for documents that contain text, tables, figures, or mixed page layouts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installer and prerequisite setup may run external installation commands that need review. <br>
Mitigation: Review install steps before execution and prefer trusted package-manager or vendor-documented installation paths. <br>
Risk: OCR requests and outputs may contain confidential document content, especially when using non-local Ollama endpoints. <br>
Mitigation: Keep Ollama on localhost for sensitive documents or use only trusted servers and network paths. <br>
Risk: Generated or temporary images may preserve original document content. <br>
Mitigation: Handle generated images as sensitive artifacts and delete them when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TsukiSama9292/pdf-ocr-tool) <br>
- [Ollama API Documentation](https://docs.ollama.com/api/generate) <br>
- [GLM-OCR Model Page](https://ollama.com/library/glm-ocr) <br>
- [poppler-utils](https://poppler.freedesktop.org/) <br>
- [uv Package Manager](https://github.com/astral-sh/uv) <br>
- [Text prompt template](prompts/text.md) <br>
- [Table prompt template](prompts/table.md) <br>
- [Figure prompt template](prompts/figure.md) <br>
- [Mixed-content prompt template](prompts/mixed.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown documents generated from PDF or image OCR, with optional extracted image files and CLI configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv, Ollama, and pdftoppm; supports text, table, figure, mixed, and auto processing modes.] <br>

## Skill Version(s): <br>
1.3.0 (source: ClawHub release evidence and _meta.json; pyproject.toml lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
