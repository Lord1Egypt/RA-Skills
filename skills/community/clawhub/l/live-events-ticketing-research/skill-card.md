## Description:

Research public StubHub and SeatGeek event calendars and resale-price snapshots for location, category, performer, and venue comparisons without purchasing tickets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Event researchers and ticket shoppers compare public resale-market event schedules and price snapshots across StubHub and SeatGeek by location, category, performer, or venue. The skill does not purchase or reserve tickets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill sends ticket-research queries and an API key to the external Crawlora service.

Mitigation: Use a dedicated Crawlora API key and avoid including sensitive information in event, venue, or location queries.

Risk: Resale prices and availability can change and may omit checkout fees or taxes.

Mitigation: Show the observation time, source, currency, and price meaning; do not present snapshots as purchase offers or guaranteed inventory.

## Reference(s):

- [Ticketing endpoint reference](artifact/reference/endpoints.md)
- [ClawHub skill listing](https://clawhub.ai/crawlora-org/skills/live-events-ticketing-research)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [Markdown snapshot table with source links and observed timestamps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves provider IDs, local event times, price meaning, currency, and availability signals; no checkout or availability guarantee.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
