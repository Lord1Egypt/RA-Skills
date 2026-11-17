## Description:

Query and explain parcel logistics across courier providers, including tracking, courier identification, multi-package lookup, status interpretation, and delivery-update guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to identify couriers, interpret parcel statuses, and summarize one or more logistics tracking numbers across courier providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled helper returns simulated tracking data, which may be mistaken for live delivery status.

Mitigation: Label outputs as simulated unless a live courier integration is added, and do not use the results for real delivery decisions.

Risk: Tracking numbers and results are retained locally, and the clear action does not erase the main database.

Mitigation: Disclose local retention to users and require separate removal or rotation of stored history before handling sensitive shipment identifiers.

Risk: Dependency versions are lower-bounded but not pinned.

Mitigation: Pin and review dependency versions before deployment.

## Reference(s):

- [ClawHub Logistics Skill](https://clawhub.ai/harrylabsj/skills/logistics)
- [Kuaidi100 API Base](https://api.kuaidi100.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Concise text or Markdown guidance, with optional CLI commands and tabular command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include courier identification, tracking-status interpretation, batch summaries, history, subscriptions, and privacy information.]

## Skill Version(s):

1.0.2 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
