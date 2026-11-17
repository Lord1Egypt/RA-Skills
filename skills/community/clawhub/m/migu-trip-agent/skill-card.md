## Description:

Plans and revises travel itineraries, recommends attractions, dining and lodging, and generates travel guides using the Migu Travel service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[llforest](https://clawhub.ai/user/llforest)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and their agents use this skill to plan and adjust trips, review daily schedules and recommendations, and request a shareable travel guide. The user configures their own Migu Travel login credential locally for service access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local Migu Travel login token can grant access to the user's account-linked trip data.

Mitigation: Have the user configure the token locally; never paste it into chat or include it in shared files.

Risk: Raw traffic logs and requests to the travel service can expose account-linked itinerary details.

Mitigation: Only use the service if sharing itinerary details with it is acceptable; avoid raw traffic logging during normal use and delete existing traffic logs.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/llforest/skills/migu-trip-agent)
- [Detailed itinerary format appendix](references/SKILL_APPENDIX.md)
- [Migu Travel web app](https://gulangyu.migudm.cn/multi-city-trip-agent/)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Links]

**Output Format:** [Markdown itineraries and travel guides, structured trip data, and travel-guide image links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports summary and detailed itineraries, trip revisions, and travel-guide generation.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
