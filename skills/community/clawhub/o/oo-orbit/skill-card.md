## Description:

Use this skill for any Orbit task—including reading, creating, updating, or deleting data—instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to search Orbit, read and enrich profiles, and manage bulk searches, watchers, and webhooks through an OOMOL-connected account. It guides the agent to inspect action schemas and obtain approval for state-changing operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup directs the agent to execute downloaded code whose full behavior is unverified.

Mitigation: Use a verified CLI installation and require separate approval before setup executes downloaded code.

Risk: Orbit actions can incur charges or create persistent watchers and webhooks.

Mitigation: Review charges and persistent effects before approving actions, and check the CLI's automatic skill-synchronization settings.

## Reference(s):

- [Orbit homepage](https://orbitsearch.com)
- [Orbit API authentication documentation](https://docs.orbitsearch.com/authentication)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Guidance]

**Output Format:** [Orbit search and profile data as JSON or compact Markdown, plus action guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include profile information; some actions can incur charges or create persistent watchers and webhooks.]

## Skill Version(s):

1.0.2 (source: frontmatter; corroborated by release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
