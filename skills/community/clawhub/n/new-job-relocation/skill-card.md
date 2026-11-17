## Description:

Helps agents search and format relocation travel booking options by running the flyai CLI and returning user-facing results with booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to plan new-job relocation travel by collecting route details, executing real-time flight searches, and presenting comparable booking options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install and run an unpinned external travel CLI that receives user travel details.

Mitigation: Review or pin the CLI package before installation and run it with constrained permissions.

Risk: Unsafe command templates or malformed arguments could lead to unintended CLI execution.

Mitigation: Validate arguments against the documented parameter list before running commands.

Risk: Travel results may be incomplete or unsafe to trust if they are not sourced from live CLI output.

Mitigation: Only present results returned by the CLI and require each booking option to include a detailUrl booking link.

## Reference(s):

- [Parameter Collection and Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with comparison tables and booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires real-time flyai CLI output; booking results must include detailUrl links.]

## Skill Version(s):

3.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
