## Description:

JSON Processor helps agents format, validate, extract fields from, and convert JSON data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoheizp](https://clawhub.ai/user/xiaoheizp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to clean up JSON, validate syntax, extract specific fields, convert JSON into CSV or table-style output, and inspect API responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on installing jq through package-manager commands, which may be inappropriate on shared or locked-down machines.

Mitigation: Review and approve the jq installation step before use, or use an already approved jq installation.

Risk: The documentation is primarily in Chinese and includes private-contact donation and custom-service language.

Mitigation: Have reviewers confirm the user-facing text and support expectations before publishing in environments that require clear public support channels.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaoheizp/skills/ke-json-processor)
- [Publisher profile](https://clawhub.ai/user/xiaoheizp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command examples and JSON-processing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires jq for the documented JSON-processing commands.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
