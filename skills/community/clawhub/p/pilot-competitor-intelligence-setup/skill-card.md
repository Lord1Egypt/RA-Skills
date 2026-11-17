## Description:

Deploy a competitive intelligence system with four agents for crawling, analysis, tracking, and alerting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to configure a four-agent competitive intelligence pipeline that crawls competitor sites, analyzes changes, tracks history, and routes alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup installs many companion skills and changes the agent environment.

Mitigation: Review each companion skill before installation and pin trusted versions or digests where possible.

Risk: The setup writes persistent configuration and changes agent hostnames.

Mitigation: Use a simple alphanumeric deployment prefix and confirm any existing ~/.pilot setup file before writing the manifest.

Risk: The setup establishes peer trust and may route competitive-intelligence data to Slack or webhooks.

Mitigation: Verify peer hostnames before handshakes and treat Slack or webhook delivery as external data sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-competitor-intelligence-setup)
- [Pilot Protocol homepage](https://pilotprotocol.network)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell command and JSON manifest blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces role-specific setup instructions, peer handshakes, and persistent manifest configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
