## Description:

Operate LIFX lights and scenes through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People with an OOMOL-connected LIFX account use this skill to inspect lights and scenes, validate colors, and control lighting or effects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unchecked downloaded code and introduce broader agent changes without clear user approval.

Mitigation: Review setup before enabling the skill, explicitly approve a verified CLI installation, and review or disable bundled-skill synchronization.

## Reference(s):

- [LIFX API documentation](https://api.developer.lifx.com/reference/authentication)
- [LIFX](https://www.lifx.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action results depend on the connected LIFX account; state-changing actions require user confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
