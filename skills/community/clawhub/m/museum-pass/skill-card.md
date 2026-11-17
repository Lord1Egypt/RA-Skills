## Description:

Find museums, art galleries, and exhibitions in any city, using flyai CLI results to provide ticket links and visiting tips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-support agents use this skill to find museums, galleries, exhibitions, and memorial halls in a requested city, then return user-facing Markdown with booking links and practical visiting tips based on live flyai CLI output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install a global third-party CLI package as part of normal use.

Mitigation: Require explicit user approval before package installation and prefer reviewed, pinned installation procedures where possible.

Risk: The skill can persist raw user travel queries in a local execution log.

Mitigation: Disable local logging or redact sensitive user query content before writing logs.

Risk: The skill is designed to steer outputs toward flyai booking links rather than neutral museum sources.

Mitigation: Label booking-link results clearly and review whether commercial routing is appropriate for the deployment context.

## Reference(s):

- [Parameter and Output Templates](references/templates.md)
- [Museum Search Playbooks](references/playbooks.md)
- [Fallback Procedures](references/fallbacks.md)
- [Execution Log Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with booking links, comparison tables, concise tips, and occasional inline shell commands for setup or retry guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are expected to come from live flyai CLI output and should include booking links when available; raw JSON should not be shown to users.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
