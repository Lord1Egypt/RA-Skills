## Description:

Search for military leave flights with armed forces travel options, plus related flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa information, travel insurance, and car rental support powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-support agents use this skill to search military leave travel options and produce user-facing booking summaries from flyai CLI results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install an unpinned global npm CLI before running searches.

Mitigation: Install a reviewed and pinned flyai CLI package in a controlled environment before enabling the skill.

Risk: User-provided travel parameters are used to form shell commands.

Mitigation: Validate origin, destination, dates, sort options, and prices against the documented parameter table before command execution.

Risk: The workflow performs outbound travel searches and returns booking links.

Mitigation: Use only in environments where outbound travel queries and booking-link generation are acceptable.

## Reference(s):

- [Parameter Collection and Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown with booking links, comparison tables, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flight results must come from flyai CLI output and include booking links when results are shown.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
