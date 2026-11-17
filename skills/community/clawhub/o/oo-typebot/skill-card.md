## Description:

Use Typebot to search and read data through the OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Typebot workspace users use this skill to list workspaces and bots, retrieve bot definitions, and read collected results through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run unverified installers or introduce broader agent changes.

Mitigation: Review a specific CLI release before enabling the skill, require approval for dependency installation, and set OO_SKILLS_SYNC_DISABLED=1 before CLI use to disable startup skill synchronization.

Risk: Using the connected service involves OOMOL handling Typebot credentials and results.

Mitigation: Decide whether OOMOL should handle these credentials and results before connecting Typebot.

## Reference(s):

- [Typebot API documentation](https://docs.typebot.com/api-reference)
- [Typebot](https://typebot.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [OOMOL publisher controls for the oo CLI](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON connector results and natural-language guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Typebot account and the selected read action.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
