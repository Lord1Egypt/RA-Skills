## Description:

Create, format, align, sort, transpose, and convert tables between Markdown, CSV, JSON, and TSV using pure Python without dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darbling](https://clawhub.ai/user/darbling)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and documentation maintainers use this skill to generate and reformat GitHub-Flavored Markdown tables from structured data or existing Markdown tables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted CSV or JSON content can be converted into Markdown that is later published or rendered in a sensitive context.

Mitigation: Review and sanitize generated tables before publishing or rendering them in sensitive documentation systems.

Risk: Some advertised capabilities, including merge and TSV conversion, are not implemented in the bundled script.

Mitigation: Confirm required commands are present before relying on the skill for table merging or TSV conversion workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/darbling/skills/markdown-table-maker)
- [Publisher profile](https://clawhub.ai/user/darbling)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown tables and concise usage guidance, with optional file output from the bundled Python helper.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces GitHub-Flavored Markdown tables from Markdown, CSV, and JSON inputs; TSV and merge behavior are advertised but not implemented in the bundled script.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
