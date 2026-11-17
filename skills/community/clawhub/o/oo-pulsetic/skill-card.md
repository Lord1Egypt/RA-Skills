## Description:

Use this skill to search and read Pulsetic monitor and uptime data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users with an OOMOL-connected Pulsetic account can retrieve monitor details and review uptime, downtime, checks, events, and hourly snapshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute remote installer code whose behavior has not been verified.

Mitigation: Install the CLI yourself from a verified source, prevent automatic installer execution, and review bundled-skill synchronization settings before enabling.

Risk: Connecting Pulsetic gives OOMOL access to the account and requested data.

Mitigation: Connect only if you trust OOMOL with the Pulsetic account access and data requested by your tasks.

## Reference(s):

- [Pulsetic API documentation](https://help.pulsetic.com/category/275-api)
- [Pulsetic](https://pulsetic.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Shell commands and JSON responses, summarized as text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a connected Pulsetic account through the oo CLI.]

## Skill Version(s):

1.0.2 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
