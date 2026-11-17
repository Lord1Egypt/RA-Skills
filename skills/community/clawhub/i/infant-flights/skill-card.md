## Description:

Book infant flights, baby travel tickets and bassinet seat options with child fare and infant-in-arm booking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-support agents use this skill to search infant-friendly flights, prioritize direct or short-duration itineraries, and format CLI-derived booking options with baby travel reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to install and run an unpinned global flyai CLI before returning travel results.

Mitigation: Require explicit user approval before package installation, pin or verify the CLI source where possible, and do not allow sudo installation.

Risk: Travel searches and booking-link workflows may expose itinerary preferences or sensitive passenger context to an external service.

Mitigation: Avoid entering passport numbers, payment details, or unnecessary identity data, and review the flyai service and logging behavior before use.

Risk: The artifact describes local execution logs for user travel requests.

Mitigation: Disable, remove, or tightly control local logging before using the skill with sensitive travel queries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/infant-flights)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with booking links, comparison tables, baby travel tips, and inline shell commands when troubleshooting is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires live flyai CLI results for flight options and booking URLs.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
