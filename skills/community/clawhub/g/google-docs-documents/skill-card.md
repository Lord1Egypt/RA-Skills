## Description:

Google Docs API integration with managed OAuth for searching, reading, creating, and updating Google Docs documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent find, read, create, and update Google Docs documents through a connected Google account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on ClawLink as an external OAuth bridge for Google Docs access.

Mitigation: Install only after reviewing ClawLink verification or source information where available, and use the least-privileged Google account suitable for the task.

Risk: Connected tools can modify Google Docs content.

Mitigation: Preview and explicitly confirm create, update, delete, and other write operations before execution.

Risk: OAuth access may remain available after the immediate task is complete.

Mitigation: Revoke the Google authorization or remove the plugin allowlist entry when the integration is no longer needed.

## Reference(s):

- [Google Docs API Overview](https://developers.google.com/docs/api)
- [Google Docs Documents Resource](https://developers.google.com/docs/api/reference/rest/v1/documents)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/google-docs-documents)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Google Docs document identifiers, previews, document text, and confirmation prompts before write operations.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
