## Description:

A Chinese-language travel-planning workflow that researches trip details and creates itineraries, daily guidance, and shareable travel materials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liberalchang](https://clawhub.ai/user/liberalchang)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and trip planners use this skill to compare destinations, check current travel details, and prepare personalized itineraries and shareable trip guides.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outdated travel details could lead to incorrect bookings or unsafe plans.

Mitigation: Recheck current official prices, hours, transport, and weather before departure; label anything unverified.

Risk: The optional Pexels integration sends the API key and search terms to a third party.

Mitigation: Protect the key and review search terms, or use locally generated images instead.

Risk: Preparing a friend-facing version can overwrite a configured local file.

Mitigation: Review the file rules before running the conversion and check the backup and resulting file.

Risk: A public itinerary may reveal private travel or companion details.

Mitigation: Review shared versions for personal details before publishing or sending them.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/liberalchang/skills/jianhao-travel-planner)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, Guidance]

**Output Format:** [Markdown plans and self-contained HTML itinerary and food-guide files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include offline and shareable web versions, with unverified travel details labeled.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
