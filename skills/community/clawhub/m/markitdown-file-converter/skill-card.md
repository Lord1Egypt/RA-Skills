## Description:

Converts PDF, Word, Excel, PowerPoint, image, text, data, ebook, and audio files into Markdown or structured JSON using pandoc, MarkItDown, mammoth, and OCR fallbacks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moniq888](https://clawhub.ai/user/moniq888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert individual files or batches of documents into Markdown for reading and editing, or into JSON sections for downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OCR can send document images or contents to a hard-coded PaddleOCR Cloud endpoint during normal use.

Mitigation: Use the skill only with files approved for cloud OCR, require explicit cloud-OCR opt-in, and remove or replace the hard-coded PaddleOCR defaults before private-document use.

Risk: Automatic dependency installation can modify the local Python or system environment.

Mitigation: Preinstall reviewed dependencies in a dedicated virtual environment or container and disable automatic installation in managed environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moniq888/skills/markitdown-file-converter)
- [Pandoc installation documentation](https://pandoc.org/installing.html)
- [Poppler Windows releases](https://github.com/oschwartz10612/poppler-windows/releases)
- [Baidu AI Studio](https://aistudio.baidu.com/)
- [Baidu Intelligent Cloud](https://login.bce.baidu.com/)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Files, Shell commands, Guidance]

**Output Format:** [Markdown or structured JSON files, with extracted image files when source documents contain images.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-file and batch conversion, backend selection, timeout control, and verbose progress output.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
