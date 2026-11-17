## Description:

Fly with pets, find pet-friendly airlines and in-cabin pet tickets with animal cargo booking options, using Fliggy/flyai CLI output for flight, booking, and travel options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bufferstreamer](https://clawhub.ai/user/bufferstreamer)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-support agents use this skill to search pet-friendly flight options, prioritize direct or shorter routes, and present booking candidates with pet-travel reminders. It requires real-time results from the flyai CLI rather than stored travel knowledge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install an unpinned global flyai CLI package.

Mitigation: Install and pin the CLI through a reviewed package-management process before enabling the skill; do not permit automatic global installation by the agent.

Risk: The fallback instructions may ask for sudo during CLI installation.

Mitigation: Disallow sudo escalation during skill execution and require manual administrator review for any privileged installation.

Risk: The runbook describes local persistence of raw travel queries.

Mitigation: Disable the execution log or sanitize and disclose it before retaining any user travel details.

Risk: Flight results and booking links are candidates, not confirmed pet-policy approvals.

Mitigation: Require users to confirm cabin, cargo, carrier, and fee policies directly with the airline before booking.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bufferstreamer/skills/pet-flights)
- [Parameter and output templates](references/templates.md)
- [Pet-flight playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with booking links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flight results must come from flyai CLI output and include booking links when results are shown.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
