## Description:

Provides customized travel packing lists and related travel-service results through the flyai CLI, including booking-linked travel options when available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to turn destination, season, trip type, and activity details into a Markdown packing-list response backed by flyai CLI results and booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install and run a third-party flyai CLI and send travel queries to that service.

Mitigation: Review the CLI package, installation scope, and service behavior before installing, and run only in an isolated environment.

Risk: The skill can return booking links and travel-service results beyond a simple packing-list response.

Mitigation: Confirm booking links are desired for the use case and review generated links before sharing or acting on them.

Risk: The skill can keep a hidden local log of raw requests when filesystem writes are available.

Mitigation: Confirm the logging behavior before use, avoid sensitive travel details, or restrict filesystem writes for the agent runtime.

## Reference(s):

- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown with booking links and inline shell commands when setup or retry steps are needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI output and booking detailUrl links; may keep a local execution log when filesystem writes are available.]

## Skill Version(s):

3.2.1 (source: server release evidence; artifact frontmatter reports 3.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
