## Description:

PDF document processing skill for reading, extracting, merging, splitting, annotating, rendering, and form-filling PDF files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guohongbin-git](https://clawhub.ai/user/guohongbin-git)

### License/Terms of Use:

Anthropic service terms

## Use Case:

Developers and agents use this skill to inspect, extract, transform, create, and fill PDF documents with Python libraries and command-line PDF tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF-processing commands and helper scripts can overwrite or create local files, including modified PDFs.

Mitigation: Make backups before running commands that modify PDFs, especially in-place operations such as qpdf --replace-input.

Risk: Untrusted dependency installation or unquoted paths can introduce ordinary local execution and file-handling risk.

Mitigation: Install dependencies from trusted package indexes, prefer pinned versions, and quote file paths carefully.

Risk: Form-filling workflows can place data in the wrong fields when field IDs, page numbers, or bounding boxes are incorrect.

Mitigation: Use the provided extraction, bounding-box validation, and visual verification steps before relying on filled PDF output.

## Reference(s):

- [PDF forms guide](artifact/forms.md)
- [PDF processing advanced reference](artifact/reference.md)
- [ClawHub skill page](https://clawhub.ai/guohongbin-git/skills/pdf-cn)
- [OpenClaw fork metadata link](https://github.com/anthropics/skills)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown with inline code blocks, shell commands, JSON examples, and local file outputs when scripts are executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local PDF, PNG, JSON, text, or spreadsheet artifacts through user-run commands and helper scripts.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
