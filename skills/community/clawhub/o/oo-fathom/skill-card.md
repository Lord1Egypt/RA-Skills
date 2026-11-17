## Description:

Operate Fathom Analytics through an OOMOL-connected account to read analytics and manage sites, events, and milestones.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site owners, and analysts can use this skill to inspect their Fathom account and site analytics, create or update sites, events, and milestones, and run aggregation reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run downloaded software without separate permission, and the exact installer behavior is unverified.

Mitigation: Review and verify the CLI release before installation, or require separate approval before running its installer.

Risk: The connected account and analytics requests are handled by OOMOL, and the CLI may synchronize skills automatically.

Mitigation: Review the CLI's synchronization behavior and disable automatic skill synchronization if it is not needed.

## Reference(s):

- [Fathom Analytics](https://usefathom.com)
- [Fathom API documentation](https://usefathom.com/api)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [oo CLI commands with JSON payloads and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands use the live connector action schema; responses include data and execution metadata.]

## Skill Version(s):

1.0.4 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
