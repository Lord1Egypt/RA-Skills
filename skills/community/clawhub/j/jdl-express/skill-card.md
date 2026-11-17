## Description:

Use JD Logistics (京东快递) for shipment tracking, shipping guidance, service-type comparison, outlet lookup, and delivery-time or fee estimation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and support agents use this skill to answer routine JD Logistics questions, including shipment tracking, service comparison, fee or delivery-time estimation, outlet lookup, and return pickup guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local runtime features may retain shipment history, subscription records, and possibly address records under ~/.openclaw/data/jdl-express/.

Mitigation: Use persistence only when needed, disclose the local storage behavior when relevant, and use the documented privacy info, export, and clear controls for retained data.

Risk: Fee and delivery-time answers may be estimates when exact JD Logistics data is unavailable.

Mitigation: State assumptions, provide cautious ranges, and do not claim to complete real shipping actions unless live tools are available and confirmed.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cautious delivery-time or fee estimates with stated assumptions when exact values cannot be confirmed.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
