## Description:

Find hotels with swimming pools, including indoor heated pools, outdoor infinity pools, rooftop pools, and kid-friendly splash areas, with related travel booking support powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-focused agents use this skill to search for pool hotels and related travel options through the flyai CLI, then present concise Markdown results with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires installing and running the flyai CLI.

Mitigation: Use a version-pinned, user-approved, locally sandboxed CLI installation before running travel searches.

Risk: Travel searches are sent to a third-party service and booking links are selected by that service.

Mitigation: Tell users when third-party services are used and validate booking links before presenting or opening them.

Risk: Local logging may expose travel queries or booking-related details.

Mitigation: Disable logging where possible or redact sensitive query details before persistence.

## Reference(s):

- [Pool Hotel skill page](https://clawhub.ai/xiejinsong/skills/pool-hotel)
- [xiejinsong publisher profile](https://clawhub.ai/user/xiejinsong)
- [Fallbacks - Hotel Category](references/fallbacks.md)
- [Playbooks - pool-hotel](references/playbooks.md)
- [Runbook - Execution Log Schema](references/runbook.md)
- [Templates - pool-hotel](references/templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with booking links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include comparison tables, troubleshooting steps, and a flyai-powered brand tag.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
