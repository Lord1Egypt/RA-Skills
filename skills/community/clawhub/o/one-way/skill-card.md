## Description:

Search one-way flights, single-trip tickets and open-ended travel bookings with no return date required, powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-support agents use this skill to search and format one-way flight options with booking links from flyai CLI results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install a global flyai CLI package.

Mitigation: Review the package source and provenance first, require explicit approval before installation, and pin a reviewed version.

Risk: The skill runs commands derived from user travel requests.

Mitigation: Use safe argument-based command execution with strict validation of supported flags and user-provided values.

Risk: Raw travel queries may be retained in local execution logs.

Mitigation: Disable or remove raw logging and avoid entering sensitive personal travel details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiejinsong/skills/one-way)
- [Fallbacks](references/fallbacks.md)
- [Playbooks](references/playbooks.md)
- [Runbook](references/runbook.md)
- [Templates](references/templates.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flight results should be sourced from flyai CLI output and include booking links when available.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
