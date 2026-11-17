## Description:

Summarizes academic paper PDFs into Feishu documents with structured sections, selected figures and tables, duplicate checks, and review checkpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yy-fan](https://clawhub.ai/user/yy-fan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn academic papers or technical-report PDFs into Chinese Feishu summaries with extracted metadata, figure placeholders, uploaded figures, and a reviewer pass before finalization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can upload extracted PDF contents and figures into Feishu documents and store local copies, logs, and document tokens.

Mitigation: Use a controlled workspace, avoid confidential papers unless the Feishu destination and logs are approved, and redact or protect document tokens after each run.

Risk: The skill text includes elevated package installation commands for required PDF and OCR utilities.

Mitigation: Install Poppler, Tesseract, and jq through an approved environment setup before running the skill instead of executing inline sudo commands during agent operation.

Risk: The security scan advises avoiding attacker-supplied PDFs until prompt-injection boundaries, path validation, token redaction, and JSON escaping are fixed.

Mitigation: Process only trusted PDFs in an isolated workspace and review generated summaries and Feishu updates before sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yy-fan/skills/paper-summarize-pdf-to-feishu)
- [Summary template](references/summary_template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, Feishu document updates, local text/image files, logs, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local PDF utilities and Feishu document access; may create local paper directories, logs, extracted text, images, metadata JSON, and Feishu document tokens.]

## Skill Version(s):

2.0.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
