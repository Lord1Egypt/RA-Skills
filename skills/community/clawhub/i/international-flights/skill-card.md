## Description:

International Flights helps agents search international flights from China to worldwide destinations and pair results with visa, entry policy, and document requirement checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-support agents use this skill to retrieve flyai CLI-based international flight options from China, compare routes or entry cities, and present visa or transit guidance alongside booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned global CLI installation and sudo fallback can run third-party package code with broad local privileges.

Mitigation: Install only after user approval from a trusted source, avoid the sudo fallback, and prefer a pinned or verified package version in a controlled environment.

Risk: Travel queries and execution logs may include sensitive itinerary, passport, payment, or identity details.

Mitigation: Do not collect passport or payment data through this skill, warn users about raw query logging, and disable or tightly control logs before entering sensitive details.

Risk: CLI commands built from user-provided travel input can produce incorrect or unsafe execution if parameters are not validated.

Mitigation: Use only documented flyai parameters, ask for missing critical inputs, and require confirmation before installation or CLI execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiejinsong/skills/international-flights)
- [Templates reference](references/templates.md)
- [Playbooks reference](references/playbooks.md)
- [Fallbacks reference](references/fallbacks.md)
- [Runbook reference](references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with comparison tables, booking links, visa guidance, and inline CLI commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results must come from flyai CLI output, include booking links when available, and avoid raw JSON.]

## Skill Version(s):

v3.2.4 (source: ClawHub release evidence; artifact frontmatter lists 3.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
