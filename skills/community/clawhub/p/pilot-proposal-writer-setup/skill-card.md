## Description:

Deploy a three-agent proposal writing system for research, drafting, and compliance review of RFP responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and proposal operations teams use this skill to configure a three-agent workflow that researches RFP requirements, drafts proposal sections, and reviews submissions for compliance and win themes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup installs helper skills without pinned versions.

Mitigation: Pin and verify the dependent skills before business deployment.

Risk: Proposal and pricing content can be routed to webhook and Slack integrations.

Mitigation: Confirm the exact webhook and Slack destinations and avoid sending confidential proposal or pricing data unless approved.

Risk: Unsafe or ambiguous hostname prefixes can affect peer handshakes and routing.

Mitigation: Use only hostname-safe prefixes and verify the peer handshakes before sending proposal data.

Risk: The setup manifest can persist after the deployment is no longer needed.

Mitigation: Remove ~/.pilot/setups/proposal-writer.json when the deployment is retired.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-proposal-writer-setup)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands and JSON configuration templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides role selection, dependent skill installation, host naming, setup manifest creation, and peer handshakes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
