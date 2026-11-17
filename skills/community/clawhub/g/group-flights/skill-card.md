## Description:

Helps agents search group flights, team travel tickets, corporate bookings, and related travel options through the FlyAI CLI with booking links for user-facing results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Agents assisting external travel planners, teams, and corporate coordinators use this skill to collect route details, run FlyAI CLI flight searches, and format group-travel options with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install a third-party FlyAI CLI globally and includes a sudo installation path.

Mitigation: Require explicit user approval before installation, avoid sudo or automatic global installs, and pin or verify the CLI package before use.

Risk: Travel details may be sent through a third-party travel provider when the CLI is used.

Mitigation: Tell users that FlyAI handles the travel query, collect only needed route details, and use the skill only when that data sharing is acceptable.

Risk: Raw travel queries can be persisted locally through the execution log behavior.

Mitigation: Disable raw query logging by default or redact user travel details before writing any local execution log.

Risk: Commercial booking links are mandatory in formatted results.

Mitigation: Disclose the booking-link behavior and review any commercial relationship before deploying the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/group-flights)
- [ClawHub publisher profile](https://clawhub.ai/user/dingtom336-gif)
- [Templates](artifact/references/templates.md)
- [Playbooks](artifact/references/playbooks.md)
- [Fallbacks](artifact/references/fallbacks.md)
- [Runbook](artifact/references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown tables and concise guidance, with inline shell commands for CLI execution and troubleshooting.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FlyAI CLI output for travel data and includes booking links when flight results are shown.]

## Skill Version(s):

3.2.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
