## Description:

Connects to LiveAgent through the OOMOL oo CLI to read, create, and update contacts and tickets, and to retrieve departments, groups, and other records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Support operators and other LiveAgent users use this skill to retrieve contacts, tickets, departments, and groups, and to create or update contacts and tickets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup can execute unverified software and introduce broader agent changes.

Mitigation: Review and approve the CLI installation separately; inspect its bundled-skill synchronization behavior and disable it if unwanted.

Risk: The integration handles LiveAgent credentials and data through OOMOL.

Mitigation: Connect only the LiveAgent permissions needed and account for OOMOL handling the integration's credentials and data.

## Reference(s):

- [LiveAgent skill release](https://clawhub.ai/oomol/skills/oo-liveagent)
- [LiveAgent homepage](https://www.liveagent.com)
- [LiveAgent API reference](https://support.liveagent.com/840770-Complete-API-reference)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON connector requests and responses with concise textual guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected LiveAgent account and its permissions.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
