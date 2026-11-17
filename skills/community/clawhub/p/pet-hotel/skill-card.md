## Description:

Pet Hotel helps agents find pet-friendly hotel options with pet policies, nearby walking areas, room choices, and booking links using FlyAI/Fliggy CLI results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel-support agents use this skill to search for pet-friendly stays, compare hotel options, and return booking-link-backed Markdown results from current FlyAI CLI data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a globally installed FlyAI CLI and its package supply chain.

Mitigation: Install only a trusted, pinned CLI version after user approval and run it in a restricted environment.

Risk: User travel details may be incorporated into shell commands.

Mitigation: Use safe argument-based CLI execution and validate destination, date, price, and keyword values before execution.

Risk: Raw query logging may retain sensitive travel details.

Mitigation: Disable or remove persistent raw-query logging and avoid storing personal or sensitive itinerary data.

Risk: Booking links may send users to unvalidated destinations.

Mitigation: Validate booking-link domains before presenting links to users.

## Reference(s):

- [Parameter and output templates](references/templates.md)
- [Pet hotel playbooks](references/playbooks.md)
- [Hotel fallback guidance](references/fallbacks.md)
- [ClawHub skill page](https://clawhub.ai/xiejinsong/skills/pet-hotel)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown tables with booking links and inline shell commands for setup or troubleshooting]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are expected to include FlyAI-sourced hotel details, prices, and booking links when available.]

## Skill Version(s):

3.2.1 (source: server release metadata; artifact frontmatter lists 3.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
