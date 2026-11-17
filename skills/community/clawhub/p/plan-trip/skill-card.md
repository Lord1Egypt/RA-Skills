## Description:

Plan your entire trip with AI — flights, hotels, attractions, and day-by-day itinerary planning — using destination, dates, and interests to support flight booking, hotel reservation, train tickets, attraction tickets, visa info, travel insurance, car rental, and more, powered by Fliggy (Alibaba Group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to collect trip details, retrieve travel options for flights, hotels, visa information, and attractions, and assemble day-by-day Markdown itineraries with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to install and run an unpinned global third-party travel CLI.

Mitigation: Review the package and pin an approved version before installation; run it in a controlled environment with normal package and network monitoring.

Risk: Travel responses depend on a single third-party data source and require commercial booking links and flyai branding.

Mitigation: Treat prices, availability, and booking links as third-party results that users should verify before purchase.

Risk: The artifact describes persisting raw travel queries in a hidden local execution log.

Mitigation: Avoid entering sensitive personal, passport, visa, or confidential itinerary details unless logging is disabled or clearly governed.

## Reference(s):

- [Plan Trip ClawHub Listing](https://clawhub.ai/xiejinsong/skills/plan-trip)
- [Templates - trip-planner](references/templates.md)
- [Playbooks - trip-planner](references/playbooks.md)
- [Fallbacks - Trip Planning Category](references/fallbacks.md)
- [Runbook - Execution Log Schema](references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands for retries or setup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be based on retrieved travel data and include booking links when results are shown.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
