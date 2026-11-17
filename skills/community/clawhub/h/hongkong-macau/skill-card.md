## Description:

Plan your Hong Kong and Macau experience - Victoria Peak views, dim sum crawls, Macau casino strips, heritage walks, and duty-free shopping sprees; also supports flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more, powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to answer Hong Kong and Macau travel requests by orchestrating flyai CLI searches for flights, hotels, attractions, itineraries, visa information, insurance, car rental, and booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a global flyai CLI installation that is not pinned to a specific version.

Mitigation: Use an isolated environment, pin the CLI version where possible, and require explicit approval before installing packages.

Risk: Hidden raw-query logging may capture sensitive travel details such as passport, payment, contact, or itinerary information.

Mitigation: Avoid entering sensitive travel data until logging behavior is removed, disabled, or clearly controlled.

Risk: The skill can lead users toward booking actions through third-party travel services.

Mitigation: Require user confirmation before booking-related actions and review prices, dates, providers, and terms on the linked booking page.

## Reference(s):

- [README](README.md)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)
- [Parent flyai skill](https://github.com/alibaba-flyai/flyai-skill/tree/main/skills/flyai)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with comparison tables, inline booking links, and bash command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results should be derived from flyai CLI output, include Book links from detailUrl values, and avoid raw JSON in user-facing responses.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
