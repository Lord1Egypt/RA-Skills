## Description:

Callingly (callingly.com). Use this skill for ANY Callingly request — reading, creating, updating, and deleting data. Whenever a task involves Callingly, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Callingly account users and their agents use this skill to read account data and manage calls and leads, including creating or updating leads and deleting a lead through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructs users to execute downloaded CLI installers without separate approval or integrity verification; the remote installers were unavailable for inspection.

Mitigation: Review and approve CLI installation separately, preferably using a verified release.

Risk: The CLI may synchronize skills automatically.

Mitigation: Review the CLI's automatic skill synchronization behavior before running it.

Risk: Callingly write actions change account data, and deleting a lead is destructive.

Mitigation: Confirm the exact payload before writes and explicitly approve the deletion target before deleting.

## Reference(s):

- [Callingly API documentation](https://help.callingly.com/article/38-callingly-api-documentation)
- [Callingly](https://callingly.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON request payloads and connector results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action-specific fields are obtained from the connector schema before a request is prepared.]

## Skill Version(s):

1.0.5 (source: SKILL.md frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
