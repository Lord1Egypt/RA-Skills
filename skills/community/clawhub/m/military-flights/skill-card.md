## Description:

Finds military flight benefits, veteran discounts, armed forces travel deals, and related travel options through flyai CLI results powered by Fliggy (Alibaba Group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-assisting agents use this skill to collect travel parameters, execute flyai searches, and format real-time military-oriented flight options with booking links and military ID reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install and invoke a third-party global npm CLI for travel searches and booking links.

Mitigation: Require explicit approval before installation and run it in an isolated environment.

Risk: The skill executes shell commands shaped by user-provided travel parameters.

Mitigation: Validate origin, destination, dates, prices, and route filters before command execution.

Risk: The skill may persist raw travel queries in a hidden execution log.

Mitigation: Disable the log when possible, or redact sensitive trip details before persistence.

Risk: The skill returns booking links from third-party CLI output.

Mitigation: Validate returned URLs before presenting them to users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiejinsong/skills/military-flights)
- [templates.md](references/templates.md)
- [playbooks.md](references/playbooks.md)
- [fallbacks.md](references/fallbacks.md)
- [runbook.md](references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses flyai CLI output as the required data source and requires each displayed result to include a booking link.]

## Skill Version(s):

3.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
