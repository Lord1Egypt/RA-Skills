## Description:

Manage ZeroTier networks, members, organizations, access controls, and related resources through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can inspect ZeroTier resources and manage networks, members, access, invitations, and related organization resources through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup can run an unverified remote installer, and setup may make automatic changes to other agents' skills.

Mitigation: Review and approve CLI installation separately, use a verified release, and inspect and approve any proposed skill changes.

Risk: Write and destructive actions can change or delete ZeroTier resources and accounts.

Mitigation: Confirm the exact targets and effects before changes, and retain explicit approval for destructive actions.

## Reference(s):

- [ZeroTier API documentation](https://docs.zerotier.com/api/)
- [ZeroTier](https://www.zerotier.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown with shell command examples and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands and payloads depend on the selected ZeroTier action and its live schema.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
