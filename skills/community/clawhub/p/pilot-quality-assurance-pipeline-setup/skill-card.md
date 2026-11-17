## Description:

Deploy a quality assurance pipeline with 3 agents that automate test generation, execution, and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to set up a three-agent Pilot Protocol quality assurance pipeline for test generation, execution, result aggregation, bug filing, and team reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Role setup installs multiple dependent Pilot skills that may vary by publisher or version.

Mitigation: Confirm each referenced skill comes from a trusted publisher and use fixed versions before installation.

Risk: The generated reporter role can send QA reports to external webhooks, Slack, dashboards, and bug trackers.

Mitigation: Restrict reporter destinations and redact secrets, customer data, screenshots, and logs before enabling outbound integrations.

Risk: Agent handshakes establish trusted peer communication for test suites and test results.

Mitigation: Verify peer identities before accepting handshakes and use a simple lowercase alphanumeric-and-hyphen deployment prefix.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-quality-assurance-pipeline-setup)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with bash commands and JSON manifest templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilot-protocol, pilotctl, clawhub, a running daemon, and role-specific Pilot skills.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
