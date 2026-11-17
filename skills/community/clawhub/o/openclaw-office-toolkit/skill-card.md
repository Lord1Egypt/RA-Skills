## Description:

Office Toolkit helps agents read, create, and edit Word, Excel, PowerPoint, CSV, and PDF documents using common Python document libraries plus Pandoc and LibreOffice when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect, generate, format, convert, and update Office documents and PDFs during document automation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Privileged and unpinned setup commands can modify host system packages.

Mitigation: Review setup commands before installing, prefer a virtual environment, avoid --break-system-packages, and only use sudo apt install with trusted OS package sources.

Risk: Document editing workflows can overwrite or damage existing files.

Mitigation: Keep backups before editing existing documents and verify outputs with the appropriate Office or PDF tooling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/axelhu/skills/openclaw-office-toolkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code blocks and file-operation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify Office document files when the agent applies the guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
