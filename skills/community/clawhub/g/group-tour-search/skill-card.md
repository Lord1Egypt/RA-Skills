## Description:

Searches group tours, private tours, and curated tour packages by destination or travel scenario, and can query train and flight options to the destination through connected travel platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to find package tour options from destination or scenario prompts, then compare train or flight options for reaching the selected destination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends destination, departure city, and travel date queries to external proxy services.

Mitigation: Review the data flow before installation and avoid entering sensitive personal details in travel queries.

Risk: The artifact embeds a reusable proxy token.

Mitigation: The publisher should remove and rotate the embedded token and use a scoped runtime secret instead.

Risk: Prices, availability, ratings, and schedules may change after results are returned.

Mitigation: Confirm current details on the linked booking page before relying on any itinerary or purchase decision.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/group-tour-search)
- [Publisher profile](https://clawhub.ai/user/travel-skills)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style text with ranked travel options, prices, ratings, schedules, and booking links when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on external proxy services and live travel-platform availability.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
