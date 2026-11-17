## Description:

Operate StoreRocket (storerocket.io) to read, create, update, and delete data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect StoreRocket projects and locations, and to create, update, or delete locations through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or configuring the oo CLI may make broader changes to an agent's skills.

Mitigation: Review and install a vetted CLI release separately, then verify that OO_SKILLS_SYNC_DISABLED=1 prevents startup skill writes.

Risk: Requests use the connected OOMOL account, and actions can change or delete StoreRocket data.

Mitigation: Review the exact action and payload, and retain user confirmation for write and destructive actions.

## Reference(s):

- [StoreRocket API documentation](https://docs.storerocket.io/api/introduction)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-storerocket)

## Skill Output:

**Output Type(s):** [JSON data, Guidance]

**Output Format:** [JSON connector responses with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write and destructive actions require user confirmation; retrieve each action's schema before building its payload.]

## Skill Version(s):

1.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
