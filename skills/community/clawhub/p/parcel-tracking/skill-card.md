## Description:

Detects parcel carriers such as DHL, Hermes, UPS, GLS, and Amazon through the Track123 API and retrieves tracking information, with optional postal code support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dany9328](https://clawhub.ai/user/dany9328)

### License/Terms of Use:


## Use Case:

External users or support operators use this skill to check shipment status and recent tracking events for a parcel from a tracking number, optionally scoped by postal code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send tracking numbers, postal codes, and the Track123 API secret to the configured API endpoint.

Mitigation: Install only when the publisher is trusted, keep TRACK123_API_BASE set to the official Track123 HTTPS endpoint, and use a narrowly scoped Track123 API secret that can be rotated.

Risk: Tracking numbers and postal codes can reveal personal shipment information.

Mitigation: Treat these values as sensitive shipment data and avoid unnecessary sharing or retention of request and response details.

## Reference(s):

- [ClawHub Parcel Tracking skill page](https://clawhub.ai/dany9328/skills/parcel-tracking)
- [Track123 Open API endpoint](https://api.track123.com/gateway/open-api/tk/v2)

## Skill Output:

**Output Type(s):** [markdown, json]

**Output Format:** [JSON containing a Markdown tracking summary and structured shipment status fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes carrier, status, delivery flag, ETA, checkpoint count, and tracking URL when available.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
