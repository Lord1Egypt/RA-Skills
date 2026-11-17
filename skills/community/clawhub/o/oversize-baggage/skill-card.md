## Description:

Search for flights accommodating oversize baggage and sports equipment, with related travel booking support powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-support agents use this skill to search flight options for oversized baggage, sports equipment, and related travel bookings. The skill guides the agent to collect route details, run FlyAI CLI searches, and return concise Markdown results with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to install and run an unpinned global npm CLI.

Mitigation: Require explicit approval before installation, pin and verify the package, and prefer an isolated install.

Risk: Travel searches may send route, date, and booking intent to an external CLI service.

Mitigation: Use the skill only when users trust the FlyAI CLI source and are comfortable with external travel queries and booking links.

Risk: Unsafe shell command templates could mishandle user-provided city or date values.

Mitigation: Validate origin, destination, and date inputs, and pass structured CLI arguments instead of interpolated shell strings.

## Reference(s):

- [Parameter Collection & Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [ClawHub skill page](https://clawhub.ai/xiejinsong/skills/oversize-baggage)
- [Publisher profile](https://clawhub.ai/user/xiejinsong)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with CLI-derived comparison tables and booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FlyAI CLI output for travel results; responses should avoid raw JSON and include booking links when results are shown.]

## Skill Version(s):

3.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
