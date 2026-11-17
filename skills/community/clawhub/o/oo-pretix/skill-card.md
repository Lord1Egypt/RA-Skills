## Description:

Search and read pretix events, ticket items, organizers, and orders through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Event organizers and operators use this skill to inspect pretix events, ticket items, organizers, and orders through an already connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs users to run a remote installer whose changes were unavailable for inspection.

Mitigation: Review and install the CLI yourself from a verified release where available before enabling the skill. Check automatic skill synchronization settings and limit the connected pretix account to the reads you need.

## Reference(s):

- [pretix](https://pretix.eu)
- [pretix API documentation](https://docs.pretix.eu/dev/api/)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Natural-language summaries and pretix lookup data (JSON)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only lookup results.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
