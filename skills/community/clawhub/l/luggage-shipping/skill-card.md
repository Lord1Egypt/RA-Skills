## Description:

Search for flights with luggage shipping and extra baggage transport options, using the flyai CLI for live travel results and booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bufferstreamer](https://clawhub.ai/user/bufferstreamer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-support agents use this skill to search for luggage-shipping flights, compare recommended, cheapest, fastest, or direct options, and return Markdown results with booking links from the CLI output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install and run a third-party global npm CLI.

Mitigation: Review the CLI package before use, prefer a pinned version installed by the operator, and run it in a constrained environment.

Risk: Generated shell commands may include user-provided route, date, or query text.

Mitigation: Validate and quote user inputs, and use only documented flyai flags before executing commands.

Risk: Provider-specific booking links and travel results may influence user choices.

Mitigation: Confirm returned booking links come from CLI output and make the provider source clear to users.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bufferstreamer/skills/luggage-shipping)
- [Parameter Collection and Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results must come from flyai CLI output and include provider booking links when flights are returned.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
