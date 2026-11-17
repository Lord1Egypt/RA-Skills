## Description:

Monitors and summarizes earnings from bandwidth nodes, decentralized storage, DeFi yields, and staking with alerts for drops or offline status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariusfit](https://clawhub.ai/user/mariusfit)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to monitor passive income sources, summarize earnings, configure alerts, and export local earning history for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local logs, wallet identifiers, node identifiers, optional API keys, and webhook alerts can expose sensitive financial metadata.

Mitigation: Restrict permissions on the config and log directory, prefer stdout or local file alerts for privacy, and enable webhooks only for trusted endpoints.

## Reference(s):

- [Passive Income Monitor on ClawHub](https://clawhub.ai/mariusfit/skills/passive-income-monitor)
- [Publisher profile: mariusfit](https://clawhub.ai/user/mariusfit)
- [Skill source artifact](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands, JSON configuration examples, status tables, alerts, and export instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local config, logs, wallet or node identifiers, optional API keys, and trusted webhook endpoints.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
