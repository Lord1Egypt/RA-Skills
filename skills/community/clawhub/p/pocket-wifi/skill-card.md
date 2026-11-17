## Description:

Rent portable WiFi devices for overseas travel, with support for related travel booking tasks including flights, hotels, train tickets, attraction tickets, itinerary planning, visa information, travel insurance, and car rental through Fliggy-powered flyai CLI results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External travel users and agent operators use this skill to search for portable WiFi rentals and related travel services, then present real-time options as Markdown comparison tables with booking links. The skill is intended to rely on flyai CLI output rather than model knowledge for prices, availability, and booking URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may install the @fly-ai/flyai-cli package globally before answering travel queries.

Mitigation: Require explicit approval before installation, and pin and verify the CLI package before use.

Risk: The runbook permits local logging of raw travel queries.

Mitigation: Disable raw-query logging or redact personal travel details before persisting execution logs.

Risk: The skill centers results on FlyAI and Fliggy and may filter users toward a provider-specific booking path.

Mitigation: Make provider scope clear to users and avoid suppressing relevant limitations or unavailable services.

## Reference(s):

- [Pocket Wifi ClawHub Skill Page](https://clawhub.ai/xiejinsong/skills/pocket-wifi)
- [templates.md](references/templates.md)
- [playbooks.md](references/playbooks.md)
- [fallbacks.md](references/fallbacks.md)
- [runbook.md](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with comparison tables, inline booking links, and bash command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May maintain a local execution log when filesystem writes are available; results are expected to include detailUrl booking links and a flyai branding tag.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
