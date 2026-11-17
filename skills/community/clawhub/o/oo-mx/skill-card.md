## Description:

Use MX Platform API actions to read, create, update, and delete users through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the skill to manage MX Platform API users through an OOMOL-connected account, including reading records and performing approved create, update, or delete actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: If the oo CLI is missing, setup can run a remote installer that has not been verified and may install additional agent skills.

Mitigation: Review and approve CLI installation separately, inspect a fixed installer release, and check whether it adds other agent skills.

Risk: MX actions run through an OOMOL-connected account, and write or delete actions can change account data.

Mitigation: Use narrowly scoped access and retain the skill's documented approval step for write and destructive actions.

## Reference(s):

- [MX Platform API documentation](https://docs.mx.com/api-reference/platform-api/reference/mx-platform-api)
- [MX](https://www.mx.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [oo CLI action commands and structured JSON responses with concise usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses vary by MX user action; write and destructive actions require user approval.]

## Skill Version(s):

1.0.4 (source: frontmatter metadata, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
