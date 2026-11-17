## Description:

Retrieve and summarize public travel notes and popular attraction data from Mafengwo for destinations, including ratings, reviews, tickets, and opening times.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

Travel analysts, operators, and agents use this skill to summarize public Mafengwo destination pages, attraction details, and travelogue trends for lightweight analysis, itinerary suggestions, and notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may browse public Mafengwo pages for travel summaries.

Mitigation: Use specific destinations or pages and avoid broad scraping, API reversal, or attempts to bypass platform rules.

Risk: Prices, opening times, ratings, and comment counts can change over time.

Mitigation: Include the collection time in outputs and treat time-sensitive travel details as needing confirmation before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/codekungfu/skills/mafengwo)
- [Mafengwo homepage](https://www.mafengwo.cn/)
- [Mafengwo travel guides](https://www.mafengwo.cn/gonglve/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or concise text summaries with extracted fields and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should note collection time when prices or opening hours may change.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
