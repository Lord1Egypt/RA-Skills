## Description:

Zipcodebase (zipcodebase.com). Use this skill for ANY Zipcodebase request — searching and reading data. Whenever a task involves Zipcodebase, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users can search postal codes by location, find nearby or distance-matched postal codes, calculate distances, and check account status through a connected Zipcodebase account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unverified CLI software or introduce broader, persistent agent changes without clear user control.

Mitigation: Review and preinstall a known CLI version, disable automatic skill synchronization with the documented OO_SKILLS_SYNC_DISABLED control, and connect only the intended Zipcodebase account.

Risk: Queries pass through OOMOL while using the connected Zipcodebase account.

Mitigation: Connect only the intended account and review the CLI and connection controls before enabling the skill.

## Reference(s):

- [Zipcodebase API documentation](https://app.zipcodebase.com/documentation)
- [Zipcodebase](https://zipcodebase.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI commands and controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON connector results with concise Markdown summaries or guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected postal-code action and the connected Zipcodebase account.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
