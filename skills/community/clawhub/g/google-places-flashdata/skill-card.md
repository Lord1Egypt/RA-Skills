## Description:

Search Google Places with FlashData for local businesses, addresses, ratings and review counts. Use for local business search, comparing places, or building a list of businesses in a chosen city. Requires a FlashData API key and paid Credits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flashdatadev](https://clawhub.ai/user/flashdatadev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to find local businesses by category and location, then organize returned names, addresses, ratings, and review counts into a shortlist or comparison.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries send requests to the hosted FlashData service and may spend paid FlashData Credits.

Mitigation: Review pricing and the requested query count before running searches; use only the budget authorized for the task.

Risk: A timed-out query may have been charged, so resubmitting it can create a duplicate charge.

Mitigation: Check the returned job ID or FlashData Jobs before retrying; if there is no job ID, check the console and report the outcome as unknown.

## Reference(s):

- [FlashData Google Places documentation](https://flashdata.dev/docs/sources/google_places?utm_source=clawhub&utm_medium=integration&utm_campaign=intent_gtm_2026q4&utm_content=google_places-task)
- [FlashData pricing](https://flashdata.dev/pricing?utm_source=clawhub&utm_medium=integration&utm_campaign=intent_gtm_2026q4&utm_content=google_places-task)
- [Search argument example](artifact/references/query.json)
- [Search argument schema](artifact/references/schema.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Structured place search results and concise text or Markdown shortlists and comparisons]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned place counts and fields vary; missing ratings or review counts should remain unknown.]

## Skill Version(s):

1.0.3 (source: frontmatter; release evidence confirms)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
