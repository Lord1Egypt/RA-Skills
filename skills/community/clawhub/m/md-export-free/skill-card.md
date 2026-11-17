## Description:

Converts Markdown content into DOCX, PPTX, XLSX, PDF, HTML, IPYNB, CSV, JSON, XML, LaTeX, Markdown, or extracted code files through markdown-exporter commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and automation teams use this skill to convert Markdown documents, tables, slide decks, notebooks, and code blocks into common publishing and data exchange formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security review says the skill asks for API credentials and external-service setup without explaining why or where data would go.

Mitigation: Use it only for local Markdown conversion unless the publisher clearly documents any remote service, data transfer, and credential handling.

Risk: Markdown inputs and generated outputs can contain sensitive document content.

Mitigation: Do not provide credentials, callback URLs, or sensitive documents unless data handling and output paths are understood and approved.

Risk: The artifact includes command execution and file writing workflows.

Mitigation: Review commands, input paths, and output paths before execution, and run conversions in a controlled workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/md-export-free)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with command examples and file-format descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or describes document, data, notebook, presentation, web, and extracted-code outputs from Markdown file paths.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
