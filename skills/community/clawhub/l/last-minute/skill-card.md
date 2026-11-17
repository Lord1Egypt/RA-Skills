## Description:

Helps agents search same-day and urgent flight options through the flyai CLI and format real-time results with booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[palexu](https://clawhub.ai/user/palexu)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-support agents use this skill to find urgent same-day or near-term flights, compare options, and present booking links from provider results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on flyai/Fliggy and directs agents to install a third-party CLI, including global npm installation paths.

Mitigation: Review the provider and CLI before use, perform installation manually, and avoid automatic global or elevated installation.

Risk: The skill builds shell commands from user-provided travel inputs.

Mitigation: Validate city, airport, date, time, class, and budget inputs before command execution and run commands in a low-privilege environment.

Risk: Travel queries may contain sensitive itinerary details and the artifact describes optional execution logging.

Mitigation: Disable or restrict logging for sensitive trips and avoid sharing unnecessary personal travel details.

## Reference(s):

- [Templates - last-minute](references/templates.md)
- [Playbooks - last-minute](references/playbooks.md)
- [Fallbacks - Flight Category (Last Minute)](references/fallbacks.md)
- [Runbook - Execution Log Schema](references/runbook.md)
- [ClawHub skill page](https://clawhub.ai/palexu/skills/last-minute)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with tables, booking links, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are expected to be based on flyai CLI output and include booking links when flight options are shown.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
