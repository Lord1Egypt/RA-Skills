## Description:

Search and read procurement notices from Zhiliao Biaoxun through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users and procurement researchers use this skill to search Chinese tender and award notices, read notice details and project timelines, and check the connected account balance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may execute unverified remote code and make broader changes to agent skills.

Mitigation: Review and install a fixed CLI release yourself, and explicitly control automatic skill synchronization before use.

Risk: Procurement queries may incur provider charges.

Mitigation: Check the connected account and expected query costs before running paid searches or retrievals.

## Reference(s):

- [Zhiliao Biaoxun API documentation](https://ai.zhiliaobiaoxun.com/docs/api)
- [Zhiliao Biaoxun homepage](https://www.zhiliaobiaoxun.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Connector results in JSON, with notice and search information available for summarization as text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected account and may include paid procurement queries.]

## Skill Version(s):

1.0.2 (source: skill frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
