## Description:

Search and read Recruit CRM candidates, companies, contacts, and jobs through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiting teams can use this skill to look up and review candidate, company, contact, and job records in Recruit CRM.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup directs the user to execute downloaded installer code whose contents are unverified.

Mitigation: Install the CLI through a separately approved, verified process before using the skill.

Risk: Setup may automatically synchronize agent skills, and the connector implementation remains unverified.

Mitigation: Review setup, decide whether to disable automatic skill synchronization, and confirm OOMOL is an acceptable intermediary for recruitment data.

## Reference(s):

- [Recruit CRM](https://recruitcrm.io)
- [Recruit CRM API documentation](https://docs.recruitcrm.io/docs/rcrm-api-reference/ZG9jOjExMDcyMQ-authentication)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON data, Text, Shell commands]

**Output Format:** [Recruit CRM records returned as JSON and summarized in text; CLI commands shown in Markdown code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only candidate, company, contact, and job lookups]

## Skill Version(s):

1.0.4 (source: frontmatter; release evidence 1.0.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
