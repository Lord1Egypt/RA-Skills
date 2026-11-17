## Description:

NewsData.io (newsdata.io). Use this skill to search and read NewsData.io data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve current, cryptocurrency, historical, and source-list news from NewsData.io. It provides a guided way to inspect available action inputs and request news data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup can execute unverified remote installation code without clear user approval.

Mitigation: Review the installer and pin a trusted oo CLI release before installing; require approval for installation and changes to other agent skills.

Risk: Connecting NewsData.io gives OOMOL access to its credentials, and usage may incur charges.

Mitigation: Connect only the intended NewsData.io account, keep credentials within the managed connection, and monitor usage and billing.

## Reference(s):

- [NewsData.io documentation](https://newsdata.io/documentation)
- [NewsData.io](https://newsdata.io)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [oo CLI commands and JSON news responses, presented as text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [News results depend on the selected action and filters.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
