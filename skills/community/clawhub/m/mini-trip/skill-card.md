## Description:

Plan a complete 3-day, 2-night trip — optimal pacing with morning activities, afternoon exploration, and evening dining experiences. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more — powered by Fliggy (Alibaba Group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to plan short 3-day, 2-night trips with flights, lodging, attractions, transportation, visa, insurance, and car rental options sourced through the flyai CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to install and run an unpinned global flyai CLI.

Mitigation: Use only a reviewed, pinned flyai CLI version in a contained environment; do not allow automatic global npm installation.

Risk: The skill can persist raw travel requests, including the user_query field, in a hidden local execution log.

Mitigation: Disable local log persistence or redact raw user queries before any execution log is written.

Risk: Travel recommendations depend on live flyai CLI data and may be incomplete when commands fail or return partial results.

Mitigation: Report failed sections clearly, retry only with documented fallback commands, and include only results with verified booking links.

## Reference(s):

- [Fallbacks](references/fallbacks.md)
- [Playbooks](references/playbooks.md)
- [Runbook](references/runbook.md)
- [Templates](references/templates.md)
- [Mini Trip on ClawHub](https://clawhub.ai/xiejinsong/skills/mini-trip)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with booking links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be based on flyai CLI results, include booking links, and avoid raw JSON.]

## Skill Version(s):

3.2.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
