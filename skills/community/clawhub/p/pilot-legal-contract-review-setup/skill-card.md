## Description:

Deploy a legal contract review pipeline with three agents that extract contract terms, assess risk, and summarize findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and legal operations teams use this skill to configure a multi-agent contract review setup for clause extraction, risk assessment, and executive summary delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup handles sensitive legal contracts and includes archiving and external webhook delivery.

Mitigation: Define contract retention rules, restrict webhook destinations, and treat the deployment as a sensitive legal-data pipeline.

Risk: Trust relationships can be auto-approved after reciprocal handshakes.

Mitigation: Verify peer identities before handshakes and confirm every adjacent agent is expected for the deployment.

Risk: The setup installs dependent Pilot skills without pinning versions.

Mitigation: Install only trusted Pilot skills and publishers, and pin reviewed versions where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-legal-contract-review-setup)
- [Pilot Protocol homepage](https://pilotprotocol.network)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON manifest examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl, clawhub, Pilot skills, and a running daemon.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
