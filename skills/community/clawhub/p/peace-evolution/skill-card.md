## Description:

Peace Evolution automates multi-round review of a Peace Seeds HTML game, applies review feedback to generate a new version, and sends a Feishu notification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kukuxnd](https://clawhub.ai/user/kukuxnd)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and HTML game maintainers use this skill to review a peace-themed game across art, performance, security, testing, and cultural dimensions, then produce the next versioned HTML file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads peace*.html files from the OpenClaw workspace and creates new versioned HTML files.

Mitigation: Use explicit invocation wording and review generated files before adopting or sharing them.

Risk: The workflow can send a Feishu notification with the new version.

Mitigation: Confirm the recipient and review the generated output before sending it externally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kukuxnd/skills/peace-evolution)
- [Publisher profile](https://clawhub.ai/user/kukuxnd)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, files, guidance]

**Output Format:** [Markdown status and review summaries with generated HTML file content or file creation steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces up to three review-and-revision iterations by default, using an acceptance threshold of 85 when the workflow is followed.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
