## Description:

Search and retrieve Sina Finance market, company, fund, and news data through a connected ZYHub account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an OOMOL-connected account can search Sina Finance news and retrieve market, company, fund, and instrument data for their questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup executes unchecked remote code and may add additional agent skills.

Mitigation: Review setup before enabling the skill, install a verified oo CLI independently, and disable managed-skill synchronization if you do not want it to add skills.

Risk: OOMOL mediates queries and holds the connected provider credentials; the remote installer and connector implementations were not verified.

Mitigation: Review the connection and requested access before use, and connect only an account whose credentials are appropriate for these queries.

## Reference(s):

- [Sina Finance ZYHub homepage](https://zyhub.finance.sina.cn/)
- [Sina Finance API documentation](https://zyhub.finance.sina.cn/help/interface)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-zyhub)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON response data with textual summaries as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected ZYHub service and the requested action.]

## Skill Version(s):

1.0.2 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
