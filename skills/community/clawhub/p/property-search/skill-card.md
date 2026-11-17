## Description:

Search property.com.au for Australian property valuations, sold history, suburb profiles, and property details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jakelin](https://clawhub.ai/user/jakelin)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to construct property.com.au links for Australian property research, including valuations, sold history, suburb profiles, street browsing, and related listing paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Property addresses and searches may be sent to public real estate websites if an agent browses generated links.

Mitigation: Confirm user intent before browsing sensitive addresses and avoid submitting unnecessary personal or private details.

Risk: Generated links can be incomplete when property IDs are unknown or stale if the source website changes URL patterns.

Mitigation: Validate generated links against property.com.au or public search results before relying on property estimates, sold history, or suburb data.

Risk: Automated web fetches may be blocked by REA Group anti-bot controls.

Mitigation: Use ordinary browser navigation or public search when fetches fail, and do not attempt to bypass access controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jakelin/skills/property-search)
- [property.com.au property profile URL pattern](https://www.property.com.au/{state}/{suburb}-{postcode}/{street-name}/{number}-pid-{propertyId}/)
- [property.com.au suburb profile URL pattern](https://www.property.com.au/{state}/{suburb}-{postcode}/)
- [property.com.au sold history URL pattern](https://www.property.com.au/{state}/{suburb}-{postcode}/sold/)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Markdown guidance with URL templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include public property.com.au and realestate.com.au links; no API key required.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
