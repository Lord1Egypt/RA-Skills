## Description:

Helps agents search and present real-time Mid-Autumn Festival flight booking options through the flyai CLI, with booking links powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External travel users and support agents use this skill to collect route and date preferences, run live flight searches, and format bookable Mid-Autumn Festival travel options in the user's language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires installing and running an unpinned global flyai CLI package.

Mitigation: Review the CLI package source and installation path before deployment, and only allow global npm installs in environments where that supply-chain exposure is acceptable.

Risk: User-provided travel details are passed into shell commands.

Mitigation: Require explicit approval before execution and validate origin, destination, date, and sort parameters against the documented parameter table.

Risk: Flight results include third-party booking links.

Mitigation: Use the skill only where third-party travel-booking links are acceptable and preserve the required Book links so users can inspect the destination before booking.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/xiejinsong/skills/mid-autumn-flight)
- [Parameter Collection and Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with booking links and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires live flyai CLI output; every listed option should include a Book link.]

## Skill Version(s):

3.2.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
