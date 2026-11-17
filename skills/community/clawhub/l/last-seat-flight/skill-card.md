## Description:

Search for last available seats on nearly full flights, with support for flight booking, hotels, trains, attraction tickets, itinerary planning, visa information, travel insurance, car rental, and related travel tasks powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-support agents use this skill to collect route details, run the flyai CLI, and return current travel options with booking links. It is intended for urgent or availability-sensitive travel searches rather than knowledge-only travel advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may globally install and execute an unpinned third-party CLI.

Mitigation: Require explicit approval before installation, pin the CLI version, and run it in a restricted environment.

Risk: Travel searches pass user-provided itinerary data to an external CLI and may return external booking links.

Mitigation: Validate origin, destination, date, and budget inputs before execution, and have the user review booking links before taking action.

## Reference(s):

- [Parameter Collection and Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown response with booking links and inline shell commands when execution is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires results to come from flyai CLI output and include booking links when travel options are shown.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
