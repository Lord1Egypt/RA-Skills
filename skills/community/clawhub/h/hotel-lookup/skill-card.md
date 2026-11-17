## Description:

Hotel discovery, shortlist comparison, and booking handoff using FlyAI search-hotel on Fliggy MCP with structured filters for destination, dates, POI proximity, lodging type, star tier, bed layout, sort order, and nightly CNY cap.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuckonit](https://clawhub.ai/user/zuckonit)

### License/Terms of Use:

MIT-0

## Use Case:

External travel-planning users and agents use this skill to find hotels, compare shortlists by price, location, stars, bed type, or POI proximity, and hand off booking through returned supplier detail links. It is suited to city stays, family lodging, business travel, and budget-constrained hotel search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a third-party global FlyAI CLI installation and optional persistent API-key configuration.

Mitigation: Prefer a pinned reviewed CLI version, avoid sudo or administrator installation, and keep FLYAI_API_KEY out of logs and chat transcripts.

Risk: Hotel destinations, dates, budgets, and preferences are sent to the FlyAI/Fliggy service when searches run.

Mitigation: Tell users before running searches that their travel criteria will be sent to the service and avoid collecting unnecessary personal details.

Risk: Hotel search results can omit fields or require final confirmation on supplier pages.

Mitigation: Present only fields returned in JSON and direct users to the returned detailUrl to verify price, cancellation terms, room details, and availability before payment.

## Reference(s):

- [search-hotel reference](references/search-hotel.md)
- [FlyAI homepage](https://open.fly.ai/)
- [ClawHub skill page](https://clawhub.ai/zuckonit/skills/hotel-lookup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with concise hotel shortlist bullets or comparison tables, inline shell commands, hotel images, and booking links when present in JSON results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses only fields returned by search-hotel JSON, typically shortlists 3-5 hotels, and asks for clarification when required destination or date inputs are ambiguous.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact metadata reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
