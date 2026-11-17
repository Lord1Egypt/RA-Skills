## Description:

Toolkit for interacting with and testing local web applications using Playwright, including frontend verification, UI debugging, browser screenshots, and browser log review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[corbin-breton](https://clawhub.ai/user/corbin-breton)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to test local web applications with Playwright, inspect rendered UI behavior, capture screenshots, review browser logs, and automate browser interactions in development or staging environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Server commands run as real local command execution.

Mitigation: Review server and automation commands before running them, and install the skill only for local web testing workflows you intend to execute.

Risk: Shell mode can execute compound commands through the system shell.

Mitigation: Avoid --shell unless the command is trusted and reviewed; prefer the default argv command mode.

Risk: Browser automation can interact with unintended targets if pointed outside the expected environment.

Mitigation: Keep Playwright targets to localhost or staging and do not use the skill against production sites.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/corbin-breton/skills/keats-webapp-testing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with inline Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Playwright scripts, local server commands, screenshots paths, console log summaries, selector findings, and testing guidance.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
