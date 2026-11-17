## Description:

Deploys an expense tracking pipeline with three agents that automate receipt collection, categorization, and report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure a three-agent Pilot Protocol expense workflow that collects receipts, categorizes expenses, flags policy status, and sends reports for approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow handles sensitive business, receipt, employee, and approval data.

Mitigation: Avoid sending unnecessary employee or receipt details and restrict Slack or webhook destinations before using it in real expense workflows.

Risk: The setup makes persistent multi-agent hostname, manifest, and trust changes.

Mitigation: Use a simple hostname-safe prefix, verify each peer agent identity before handshakes, and review trust state after setup.

Risk: The workflow depends on Pilot tooling and several downstream skills.

Mitigation: Pin or otherwise verify dependent skills, pilotctl, clawhub, and the running Pilot daemon before production use.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-expense-tracker-setup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces role-specific setup steps, Pilot hostnames, manifests, handshake commands, and data-flow examples.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
