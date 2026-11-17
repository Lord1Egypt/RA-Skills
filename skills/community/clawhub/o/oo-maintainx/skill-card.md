## Description:

Use this skill to read, create, update, or delete MaintainX data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to manage MaintainX locations, users, work orders, and work order comments through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unchecked remote code; installer contents are unverified.

Mitigation: Review and verify the CLI installation before allowing automatic setup.

Risk: The CLI documents automatic skill syncing across agent apps.

Mitigation: Review or disable that behavior using the documented CLI controls.

## Reference(s):

- [MaintainX](https://www.getmaintainx.com/)
- [MaintainX API documentation](https://api.getmaintainx.com/v1/docs)
- [oo CLI command controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON results from MaintainX actions with concise action guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected read or write action and its input schema.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
