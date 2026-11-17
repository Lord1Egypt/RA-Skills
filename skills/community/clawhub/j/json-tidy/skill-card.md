## Description:

Formats, minifies, and sorts JSON, with line-and-column diagnostics for invalid input.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other JSON users can format or compact JSON, sort object keys, and locate syntax errors in local files or piped input.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The output option writes formatted JSON to the selected path, potentially replacing important file content.

Mitigation: Check the output path and back up important files before writing.

## Reference(s):

- [json-tidy on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/json-tidy)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Pretty-printed or compact JSON; plain-text parse errors]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes to standard output by default; an output path writes a file. The command-line messages are in Chinese.]

## Skill Version(s):

1.0.5 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
