## Description:

Hire a private car with driver for customized day tours -- visit multiple attractions at your own pace without the hassle of public transport, with support for flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa information, travel insurance, car rental, and more through Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel planners use this skill to find private-car day tours and related travel services from FlyAI/Fliggy, then receive concise Markdown comparisons with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an unpinned global npm CLI install.

Mitigation: Review the FlyAI CLI package before use, install a pinned version manually where possible, and prefer an isolated environment.

Risk: Raw travel queries may be persisted in a local execution log.

Mitigation: Avoid entering sensitive itinerary or personal details unless logging is disabled, sanitized, or otherwise acceptable for the deployment environment.

Risk: Results are tied to FlyAI/Fliggy as the exclusive provider and include booking links and branding.

Mitigation: Confirm this provider constraint is acceptable for the intended release and review results before relying on them for bookings.

## Reference(s):

- [Private Car Skill Page](https://clawhub.ai/xiejinsong/skills/private-car)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown tables and concise guidance with inline shell commands when setup or retry steps are needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Result output is expected to include booking links and a FlyAI powered-by tag when real-time results are shown.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
