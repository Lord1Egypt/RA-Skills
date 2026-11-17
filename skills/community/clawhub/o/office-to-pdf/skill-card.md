## Description:

Convert office files to PDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minchocoin](https://clawhub.ai/user/minchocoin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert user-selected presentations, documents, and spreadsheets into PDFs with LibreOffice in headless mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing LibreOffice adds an OS package dependency.

Mitigation: Confirm the LibreOffice package source is acceptable before installation.

Risk: Office document contents are processed locally by LibreOffice during conversion.

Mitigation: Run conversion commands only on files intentionally provided for processing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/minchocoin/skills/office-to-pdf)
- [Publisher profile](https://clawhub.ai/user/minchocoin)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands produce PDF files from LibreOffice-supported office documents.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
