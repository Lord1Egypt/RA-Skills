## Description:

Deploy a real estate analysis system with four agents for property scraping, market valuation, comparable analysis, and deal alerting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and real estate operations teams use this skill to set up a four-agent deal-finding workflow that scrapes listings, evaluates market metrics, produces comparative market analysis reports, and sends investor alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup installs multiple skills without pinned versions.

Mitigation: Review the dependency list before installing and prefer pinned versions or verified publishers.

Risk: The setup establishes persistent agent trust through peer handshakes.

Mitigation: Confirm each peer hostname and intended role before initiating handshakes.

Risk: Deal alerts sent to Slack, email, or webhook destinations may expose sensitive property, investor, valuation, or ROI data.

Mitigation: Use approved notification destinations and send only the details necessary for the alert workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-real-estate-analyzer-setup)
- [Pilot Protocol Homepage](https://pilotprotocol.network)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command blocks and JSON manifest templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl, clawhub, pilot-protocol, and a running daemon.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
