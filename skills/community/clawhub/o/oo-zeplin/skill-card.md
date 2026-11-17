## Description:

Search and read Zeplin data through the user's OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use this skill to retrieve Zeplin project details, colors, text styles, screen versions, and account information through an existing OOMOL connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger remote software installation and changes to installed agent skills.

Mitigation: Review and approve CLI installation separately; set OO_SKILLS_SYNC_DISABLED=1 for every invocation to prevent automatic changes to other agents' skills.

Risk: OOMOL handles access to connected Zeplin data, and the remote installer and hosted connector implementation remain unverified.

Mitigation: Understand that OOMOL handles access to connected data and review the documented CLI environment controls before use.

## Reference(s):

- [Zeplin API documentation](https://docs.zeplin.dev/reference)
- [Zeplin](https://zeplin.io)
- [oo CLI environment controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON request and response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Zeplin account and selected action.]

## Skill Version(s):

1.0.5 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
