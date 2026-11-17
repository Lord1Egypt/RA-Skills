## Description:

Find hotels closest to a specific attraction, landmark, or scenic spot. First verifies the POI, then searches hotels sorted by walking distance. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more powered by Fliggy (Alibaba Group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to find hotels near landmarks, attractions, scenic areas, ancient towns, theme parks, and nature areas using FlyAI/Fliggy real-time CLI results. It also guides related travel-service searches such as flights, trains, attraction tickets, itinerary planning, visa information, travel insurance, and car rental when supported by the CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a global third-party FlyAI CLI installation before it can retrieve travel data.

Mitigation: Install a pinned and reviewed CLI version in an isolated environment before allowing the agent to execute searches.

Risk: Raw travel queries and executed commands may be retained locally through the execution log behavior.

Mitigation: Disable local log persistence where possible, or redact destinations, dates, and traveler preferences before retaining logs.

Risk: The skill depends on FlyAI/Fliggy as the exclusive source for hotel data and booking links.

Mitigation: Review CLI output before acting on recommendations and treat missing booking links as invalid results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiejinsong/skills/landmark-hotel)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands when setup or retry steps are needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should be based on flyai CLI output, include booking links for listed results, and match the user's language.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
