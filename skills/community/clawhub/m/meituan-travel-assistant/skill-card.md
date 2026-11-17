## Description:

美团旅行助手 lets agents query hotels, flights, trains, scenic tickets, booking links, and itinerary suggestions for travel requests across 300+ Chinese cities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel agents use this skill to turn natural-language Chinese travel requests into hotel, flight, train, attraction ticket, booking-link, and itinerary results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel-query privacy and operational control are review-worthy because city and travel request data are sent to a remote proxy.

Mitigation: Review the proxy endpoint, retention controls, and data handling disclosures before deployment; avoid sending sensitive personal travel details unless the publisher's controls are acceptable.

Risk: The release evidence reports a built-in proxy token.

Mitigation: Publisher should rotate the token and remove default credentials from the distributed skill before production use.

Risk: The release evidence reports inconsistent tool declarations.

Mitigation: Confirm the declared tool names match the executable tool route before relying on automated invocation.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Guidance, API Calls]

**Output Format:** [JSON responses that agents can summarize as travel guidance and booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires city and natural-language query inputs; sends travel queries to a remote proxy service.]

## Skill Version(s):

2.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
