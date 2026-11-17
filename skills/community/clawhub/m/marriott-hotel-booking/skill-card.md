## Description:

Searches Marriott-family hotels and returns live prices, hotel details, package offers, and booking links for Marriott brands including Sheraton, Westin, Ritz-Carlton, JW Marriott, Renaissance, Fairfield, and St. Regis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-booking agents use this skill to search Marriott-family hotels in Chinese by destination, date, brand keyword, price, and sort order, then retrieve hotel details, package offers, and booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hotel search details and any local PROXY_TOKEN value may be sent to an opaque external proxy.

Mitigation: Install only after reviewing the proxy relationship, limit environment-variable exposure, and run the skill with scoped network access when possible.

Risk: The skill can trigger live hotel searches and booking-link retrieval when user intent is unclear.

Mitigation: Use it only after clear Marriott hotel search, detail, package, or booking intent is established.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/marriott-hotel-booking)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands]

**Output Format:** [Markdown-formatted Chinese hotel search, detail, and package results with inline booking links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are limited by the requested limit value and reflect data returned by the configured proxy service.]

## Skill Version(s):

1.1.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
