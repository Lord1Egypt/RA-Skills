## Description:

Use J&T Express (极兔速递) for shipment tracking, shipping guidance, service-type comparison, outlet lookup, and delivery-time or fee estimation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and logistics support agents use this skill to check J&T Express shipment status, estimate shipping fees or delivery times, compare economy carriers, find outlets, and prepare parcel details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local runtime features may store shipment history, subscriptions, and possibly address records under ~/.openclaw/data/jtexpress/.

Mitigation: Use the documented privacy info, export, and clear commands to inspect or remove local data, and disclose local persistence before using workflows that store shipment-related data.

Risk: Shipping fees and delivery times may be estimates when live carrier tools or current rate tables are unavailable.

Mitigation: State assumptions, present cautious ranges, and avoid claiming confirmed prices, delivery dates, or completed shipping actions unless live tools are available and confirmed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/jtexpress)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cautious estimates, assumptions, comparison guidance, and privacy disclosures when local runtime features are used.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
