## Description:

Book flights for marathon and running event trips, with related travel-planning support for hotels, trains, attraction tickets, itineraries, visa information, travel insurance, and car rental powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bufferstreamer](https://clawhub.ai/user/bufferstreamer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to search marathon and race-day travel options through the flyai CLI, collect missing route or date inputs, and return booking-ready Markdown results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install and run a global third-party CLI.

Mitigation: Review the flyai npm package before installation, prefer a sandboxed environment, pin or vet the CLI version, and require explicit approval before global installation.

Risk: Broad triggers may produce commercial booking links.

Mitigation: Confirm user intent, route, dates, and preferences before execution, and include only links returned by the CLI detailUrl field.

Risk: Travel prices and availability can change quickly.

Mitigation: Rerun the CLI for current results and avoid relying on model memory or previously cached travel data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bufferstreamer/skills/marathon-trip)
- [Parameter Collection & Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries with comparison tables, booking links, and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flight and travel results are expected to come from flyai CLI output and include detailUrl booking links.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
