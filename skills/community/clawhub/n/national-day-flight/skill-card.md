## Description:

Book National Day holiday flights for October 1st Golden Week travel, with related travel booking support powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

Travel agents and end users use this skill to search and present National Day and Golden Week flight options through the flyai CLI, including recommended, cheapest, fastest, direct, and flexible-date route workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to install and run an unpinned global npm CLI.

Mitigation: Require approval before installation, prefer a pinned local install or sandbox, and verify the CLI before use.

Risk: The skill builds shell commands from user-provided travel details.

Mitigation: Validate origin, destination, dates, and sort options against the documented parameter table before execution.

Risk: Booking links route users to a commercial travel provider.

Mitigation: Present links as provider booking links and avoid framing results as neutral travel advice.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiejinsong/skills/national-day-flight)
- [templates.md](references/templates.md)
- [playbooks.md](references/playbooks.md)
- [fallbacks.md](references/fallbacks.md)
- [runbook.md](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with comparison tables, inline booking links, and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flight results must come from flyai CLI output and include booking links when results are shown.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
