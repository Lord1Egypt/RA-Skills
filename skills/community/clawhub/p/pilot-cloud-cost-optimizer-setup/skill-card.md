## Description:

Deploys a four-agent cloud cost optimization pipeline for scanning, analysis, approved optimization, and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and FinOps engineers use this skill to configure a distributed pipeline of scanner, analyzer, optimizer, and reporter agents for cloud cost analysis and optimization workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optimizer role can enable high-impact cloud changes such as shutdown, termination, or rightsizing actions.

Mitigation: Require human approval before shutdown, termination, or rightsizing actions and limit each role's cloud credentials.

Risk: Dependent skill installation and trust setup can expand what the agent network is allowed to do.

Mitigation: Pin and verify every dependent skill, use a safe hostname prefix, and review trust relationships before deployment.

Risk: The reporter role can send cost reports to outbound Slack, email, or webhook destinations.

Mitigation: Restrict reporter destinations to approved Slack, email, or webhook targets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-cloud-cost-optimizer-setup)
- [Pilot Protocol homepage](https://pilotprotocol.network)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown, code]

**Output Format:** [Markdown instructions with bash commands and JSON manifest templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl, clawhub, the pilot-protocol skill, and a running daemon.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
