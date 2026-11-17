## Description:

Fetches Hong Kong URBTIX event listings, parses natural language event questions, and returns matching performances by date, venue, and event filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevenho1394](https://clawhub.ai/user/stevenho1394)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer questions about Hong Kong URBTIX event performances, including show dates, venues, and ticket links. It is suited for public event lookup workflows that need English or Traditional Chinese responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts a public URBTIX XML distribution endpoint and stores event-feed cache files locally.

Mitigation: Install it only where outbound public web requests and local workspace cache writes are acceptable; no credentials are required.

Risk: Public event listings can change, become unavailable, or be delayed relative to ticketing status.

Mitigation: Verify final event details and ticket availability through the official booking link before making purchase or attendance decisions.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/stevenho1394/skills/hk-urbtix-events)
- [URBTIX public XML distribution endpoint](https://fs-open-1304240968.cos.ap-hongkong.myqcloud.com/prod/gprd/URBTIX_eventBatch_YYYYMMDD.xml)

## Skill Output:

**Output Type(s):** [text, markdown, JSON]

**Output Format:** [JSON object containing a human-readable markdown answer, structured event matches, and an optional clarification message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports English and Traditional Chinese responses; results may include official booking links when available.]

## Skill Version(s):

1.0.4 (source: evidence.release.version and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
