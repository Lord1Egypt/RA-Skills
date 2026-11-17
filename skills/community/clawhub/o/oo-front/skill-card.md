## Description:

Front (front.com). Use this skill for ANY Front request — reading, creating, and updating data. Whenever a task involves Front, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Support agents and operations staff who need to read Front contacts and teammates or create and update company contacts through their OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unverified downloaded code or introduce broader agent changes through automatic skill synchronization.

Mitigation: Use a reviewed oo CLI release, avoid unattended execution of downloaded installers, and review or disable automatic skill synchronization.

Risk: The OOMOL connection mediates access to Front data, and contact changes can modify account data.

Mitigation: Understand the connected account access and keep confirmation enabled after reviewing the exact payload and effect of each contact change.

## Reference(s):

- [Front](https://front.com)
- [Front API documentation](https://dev.frontapp.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown instructions, oo CLI commands, and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions return Front data; contact creation and updates require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
