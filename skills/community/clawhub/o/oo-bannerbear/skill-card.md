## Description:

Operate Bannerbear through a connected account to inspect templates and images, verify project access, and create images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to read Bannerbear templates and images, check account access, and request image creation through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unverified installers.

Mitigation: Review and install a verified CLI release before using the skill.

Risk: Setup or refresh may add agent skills without clearly explaining those effects.

Mitigation: Review the installation and refresh behavior; the CLI command reference documents OO_SKILLS_SYNC_DISABLED=1 to disable startup skill writes.

## Reference(s):

- [Bannerbear API documentation](https://developers.bannerbear.com/)
- [Bannerbear](https://www.bannerbear.com/)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Image URLs]

**Output Format:** [Text and JSON results, including generated image URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image creation changes Bannerbear state and requires confirmation under the skill's instructions.]

## Skill Version(s):

1.0.4 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
