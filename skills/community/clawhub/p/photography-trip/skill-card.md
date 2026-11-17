## Description:

Book flights for photography trips to scenic destinations. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more - powered by Fliggy (Alibaba Group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivan97](https://clawhub.ai/user/ivan97)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to search flight options for photography-focused trips, compare recommended, cheapest, fastest, direct, and flexible-date routes, and present bookable results with source links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs the agent to install and run a global third-party CLI package.

Mitigation: Require explicit user approval before npm installation, run in an isolated environment where possible, and verify the installed package source before execution.

Risk: The skill uses forceful CLI-only instructions and can produce incorrect travel results if parameters are incomplete or wrong.

Mitigation: Confirm origin, destination, dates, and route preferences before command execution, and only present results that come from flyai output with booking links.

## Reference(s):

- [Skill Page](https://clawhub.ai/ivan97/skills/photography-trip)
- [Parameter Collection & Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with flight comparison tables, booking links, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI output for travel data; results are expected to include booking links.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
