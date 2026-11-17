## Description:

Find the earliest departing flights of the day, sorted by departure time, with support for related travel planning tasks powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel-support agents use this skill to find early morning flights, compare real-time prices, and return booking links from the flyai CLI. It is useful when a user needs the first flight out, a morning departure, or an early arrival before meetings or daytime plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install unpinned third-party software globally and may recommend sudo as a fallback.

Mitigation: Use a reviewed and pinned non-global installation of flyai-cli, and do not run the sudo npm install fallback.

Risk: A third-party travel CLI receives itinerary details and returns booking links.

Mitigation: Install and run the skill only when users are comfortable sharing travel search details with the third-party CLI and booking service.

Risk: The runbook permits persisting raw travel queries to a local execution log without a clear retention policy.

Mitigation: Disable or remove local query logging, or define retention and access controls before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiejinsong/skills/morning-flights)
- [templates.md](references/templates.md)
- [playbooks.md](references/playbooks.md)
- [fallbacks.md](references/fallbacks.md)
- [runbook.md](references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown tables and concise guidance with inline booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires live flyai CLI output; successful results include booking links and a flyai attribution tag.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
