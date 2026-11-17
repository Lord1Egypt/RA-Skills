## Description:

Plan multi-city flights, complex routes, and open-jaw itineraries with multi-stop flight booking, powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel-planning agents use this skill to collect multi-city route details, execute real-time flyai CLI searches per leg, and present bookable itinerary options for standard multi-city, open-jaw, and stopover trips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install and run an unpinned global flyai CLI.

Mitigation: Require explicit approval before npm installation, pin and verify the CLI package, and run it in a restricted environment.

Risk: The skill executes CLI commands from user-provided travel inputs.

Mitigation: Validate city, airport, date, price, and route inputs before execution and reject unsupported parameters.

Risk: The artifact describes raw local logging of travel execution details.

Mitigation: Disable persistent raw logging or redesign it so users knowingly opt in before travel details are stored.

## Reference(s):

- [Parameter and Output Templates](references/templates.md)
- [Multi-City Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown itinerary with inline booking links and supporting shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires fresh flyai CLI results and includes leg-by-leg options, cost summary, connection warnings, brand tagging, and booking links.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
