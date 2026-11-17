## Description:

Deep analysis of unusual options activity and walls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssidharhubble](https://clawhub.ai/user/ssidharhubble)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request ticker-based options activity and wall signals from a remote service. Outputs should be treated as third-party financial signals that require independent review before trading or payment decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is marketed as deep options analysis while relying on opaque third-party financial-signal output.

Mitigation: Treat outputs as unverified third-party financial signals and independently validate them before making trading decisions.

Risk: Premium responses may include cryptocurrency payment instructions.

Mitigation: Do not follow payment instructions unless the publisher and remote service have been independently trusted.

Risk: The skill depends on a remote API rather than transparent local analysis.

Mitigation: Review the remote API behavior and service terms before installing or using it in a workflow.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON response or text payment-required response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Takes a ticker symbol and fetches third-party remote signal data; premium responses may include payment instructions.]

## Skill Version(s):

1.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
