## Description:

Guides agents that connect to Substreams WebSocket fan-out servers and consume live DatabaseChanges streams with selectors, filters, reconnects, chain reorg handling, and backpressure awareness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pinax](https://clawhub.ai/user/pinax)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to connect to live blockchain table streams over WebSocket, discover available streams, subscribe or filter by network and table, and handle lifecycle events such as reconnects, reorgs, and dropped frames.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Endpoint-provided discovery documents and stream data can vary by host and may not match assumptions from another deployment.

Mitigation: Confirm available streams through the session message or /streams endpoint before subscribing, and bind downstream parsing to the observed network, table, and module metadata.

Risk: Wildcard subscriptions can ingest broader data than intended.

Mitigation: Use narrow network@table selectors when possible, confirm active subscriptions with LIST_SUBSCRIPTIONS, and use SQE filters for event-level scoping.

Risk: Dropped-frame warnings indicate the live stream may have gaps.

Mitigation: Do not forward incomplete results as complete data; reconcile gaps with Substreams backfill before using or publishing derived output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pinax/skills/pinax-websockets)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON and WebSocket examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include WebSocket URLs, JSON request and response envelopes, SQE filter examples, and troubleshooting steps.]

## Skill Version(s):

0.6.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
