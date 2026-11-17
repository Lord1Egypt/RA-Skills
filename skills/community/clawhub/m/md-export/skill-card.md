## Description:

Converts Markdown files into DOCX, PPTX, XLSX, PDF, HTML, IPYNB, CSV, JSON, XML, LaTeX, and code-block outputs through documented export commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and operations teams use this skill to convert Markdown documents, tables, slide decks, notebooks, and code blocks into shareable output files during documentation and workflow automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes unexplained API, callback, and credential guidance that does not fit a local Markdown exporter.

Mitigation: Use only local file conversion commands unless the publisher documents why network or API access is required and what data leaves the machine.

Risk: Markdown inputs may contain sensitive documents that could be exposed if callback or API paths are used.

Mitigation: Do not provide tokens, API keys, callback URLs, or sensitive documents unless the data-flow and retention behavior are reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/md-export)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline shell command examples and file-output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports file-path based Markdown conversions; generated file formats depend on the selected exporter subcommand.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
