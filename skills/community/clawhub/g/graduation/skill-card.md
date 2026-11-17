## Description:

Helps agents search graduation-trip and class-trip travel options, including flights and related travel services, using flyai and Fliggy booking data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and travel-planning agents use this skill to collect graduation travel parameters, run flyai CLI searches, and present bookable options for flights and related trip planning tasks. It is intended for user-facing graduation, post-grad, and class-trip booking assistance where real-time provider results are required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install a third-party npm package globally.

Mitigation: Require approval before global installs and review the @fly-ai/flyai-cli package and provider dependency before deployment.

Risk: Raw travel queries and CLI activity may be retained in a local execution log.

Mitigation: Disable, rotate, or delete persistent raw-query logs and avoid storing sensitive travel details.

Risk: Booking results route users through flyai or Fliggy links.

Mitigation: Review provider dependency and link handling before use, and present only CLI-returned detailUrl booking links.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/graduation)
- [Parameter and output templates](references/templates.md)
- [Scenario playbooks](references/playbooks.md)
- [Failure recovery fallbacks](references/fallbacks.md)
- [Execution log runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with booking-link tables and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI output for live travel data; user-facing travel options should include Book links when results are shown.]

## Skill Version(s):

3.2.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
