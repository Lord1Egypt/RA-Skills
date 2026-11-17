## Description:

Generates personal Gaode Map QR codes and supports geocoding, reverse geocoding, POI search, nearby search, route planning, and IP location through the AMap Web Service API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lbs-amap](https://clawhub.ai/user/lbs-amap)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn address, POI, nearby-place, and route requests into Gaode Map personal-map QR codes that can be opened in the Gaode Map app.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive addresses, trips, customer locations, or private itineraries may be sent to AMap services and to a QR generation service.

Mitigation: Use the skill only when sharing that location data with those services is acceptable, and avoid private or regulated location data unless appropriate approval is in place.

Risk: Generated QR images, schema URLs, and fallback links can reveal personal map or itinerary details if saved or shared broadly.

Mitigation: Store generated files in a controlled workspace, limit redistribution of QR codes and URLs, and remove generated artifacts when they are no longer needed.

Risk: The artifact instructs sessions to generate a personal-map QR code broadly, which can be surprising when the user only wanted search or routing information.

Mitigation: Confirm the user wants a QR code or personal-map link before generating, downloading, or presenting map artifacts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lbs-amap/skills/personal-map)
- [ClawHub publisher profile](https://clawhub.ai/user/lbs-amap)
- [Gaode Open Platform](https://lbs.amap.com/)
- [QR code generation service endpoint](https://api.qrserver.com/v1/create-qr-code/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with Python examples, shell environment setup, JSON-like API results, URLs, and local QR image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AMAP_API_KEY; map and itinerary data may be sent to AMap services and QR generation services when QR code output is requested.]

## Skill Version(s):

1.0.0 (source: server release evidence, SKILL.md frontmatter, and config.json; artifact changelog also mentions v1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
