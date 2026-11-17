## Description:

Dune (dune.com). Use this skill for ANY Dune request — reading, creating, and updating data. Whenever a task involves Dune, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to inspect Dune query schemas and retrieve query information, results, and status through an OOMOL-connected account. It can also execute saved Dune queries and return their execution metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback may run downloaded installer code without a separate approval step.

Mitigation: Preinstall a reviewed oo CLI version or require explicit approval before running its installer; review the CLI's automatic skill synchronization settings.

## Reference(s):

- [Dune skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-dune)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Dune](https://dune.com)
- [Dune API authentication documentation](https://docs.dune.com/api-reference/overview/authentication)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Shell commands with JSON input and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include query data, status, and execution metadata.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
