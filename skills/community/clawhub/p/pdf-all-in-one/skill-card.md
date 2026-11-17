## Description:

All-in-one PDF processing tool for merging, splitting, extracting, converting, OCR, PDF-to-image conversion, and table recognition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sonicrang](https://clawhub.ai/user/sonicrang)

### License/Terms of Use:

Anthropic Consumer Terms of Service or Commercial Terms of Service

## Use Case:

Developers, employees, and external users use this skill to inspect, transform, extract data from, convert, and fill PDFs in a local workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local PDF processing can expose sensitive document contents or write files to unintended paths.

Mitigation: Keep input and output files inside the documented workspace and review paths before running commands.

Risk: Dependency installation examples include package manager commands that can change the host environment.

Mitigation: Install Python dependencies in a virtual environment when possible and review any sudo package installation before running it.

Risk: Password removal and decryption examples can be misused on PDFs the user is not authorized to process.

Mitigation: Use decryption or password-removal examples only for PDFs you own or are authorized to process.

## Reference(s):

- [PDF Processing Advanced Reference](artifact/reference.md)
- [PDF Form Filling Reference](artifact/forms.md)
- [ClawHub Skill Page](https://clawhub.ai/sonicrang/skills/pdf-all-in-one)
- [OpenClaw Fork Metadata Link](https://github.com/anthropics/skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with Python and shell code blocks; generated artifacts may include PDFs, images, text, tables, and JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local filesystem read/write for user-provided PDFs; no external API keys detected.]

## Skill Version(s):

1.0.2 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
