## Description:

Search for flights suitable for loyalty program miles redemption, with support for flight booking, hotel reservations, train tickets, attraction tickets, itinerary planning, visa information, travel insurance, car rental, and related travel tasks powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bufferstreamer](https://clawhub.ai/user/bufferstreamer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-focused agents use this skill to search loyalty, miles, points, award, cheapest, fastest, and direct flight options through the flyai CLI. It helps agents collect route and date parameters, execute live travel searches, and format booking-ready Markdown with links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill tells agents to run user-derived shell commands and install an unpinned third-party CLI globally.

Mitigation: Review commands before execution, prefer a pinned and locally reviewed CLI installation, and require explicit approval before any global npm install or generated shell command runs.

Risk: Travel search details may be sent to FlyAI or Fliggy, and returned booking links point to external services.

Mitigation: Use the skill only when the user accepts sharing travel search details with the service, and review booking links before following or presenting them.

Risk: Incorrect airport, city, date, or cabin parameters can produce misleading travel recommendations.

Mitigation: Validate origin, destination, date, and class inputs before execution, and ask concise clarification questions when required route details are missing.

## Reference(s):

- [Parameter Collection and Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands, comparison tables, and booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires live flyai CLI output for travel results and instructs agents not to emit raw JSON.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
