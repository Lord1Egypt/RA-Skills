## Description:

Find overnight and late-night departure flights, compare options using live flyai CLI results, and return booking-linked travel summaries for late-evening and red-eye itineraries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to search for overnight, after-midnight, and late-evening flights, compare day-versus-night pricing, and return booking-linked Markdown rather than unsourced travel advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install and run an unpinned global flyai CLI and may escalate to sudo.

Mitigation: Use an isolated environment, avoid sudo and global npm installation, and pin and verify the CLI package before execution.

Risk: The execution log can persist raw travel requests that may include sensitive itinerary details.

Mitigation: Disable or remove the execution log when travel details are sensitive, and avoid storing personal travel data unnecessarily.

Risk: Search and booking results route through the flyai/Fliggy flow rather than neutral flight-search sources.

Mitigation: Tell users the source of results and cross-check important itinerary, price, and booking details before purchase.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiejinsong/skills/night-flights)
- [Parameter and output templates](artifact/references/templates.md)
- [Scenario playbooks](artifact/references/playbooks.md)
- [Failure recovery guidance](artifact/references/fallbacks.md)
- [Execution log schema](artifact/references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown travel-search summaries with comparison tables, booking links, and occasional inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live flyai CLI output, should include booking detail links, and should not emit raw JSON.]

## Skill Version(s):

3.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
