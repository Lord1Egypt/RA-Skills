## Description:

Control mobile robots via instant messaging platforms, with support for Unitree robots and the Insight9 AI stereo camera.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qinrui-dm](https://clawhub.ai/user/qinrui-dm)

### License/Terms of Use:

MIT

## Use Case:

Developers, robotics teams, researchers, educators, and hobbyists use this skill to connect OpenClaw agents to supported robots through IM platforms and issue movement, posture, navigation, and status commands.

### Deployment Geography for Use:

Global, with supported IM platform availability varying by region.

## Known Risks and Mitigations:

Risk: Live robot movement through IM commands can create physical safety hazards.

Mitigation: Use a supervised test area, keep an emergency stop available, and add confirmation steps plus motion limits before connecting live hardware.

Risk: Unrestricted IM access or exposed bot credentials could allow unauthorized robot control.

Mitigation: Restrict who can send commands, protect IM credentials, and review authorization behavior before deployment.

Risk: Installer or release integrity uncertainty can increase supply-chain risk.

Mitigation: Install only after reviewing the code and preferably from a pinned release or verified commit.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qinrui-dm/skills/openclaw-robotics)
- [README](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [Publisher Profile](https://clawhub.ai/user/qinrui-dm)

## Skill Output:

**Output Type(s):** [Text, Code, Configuration, API Calls, Guidance]

**Output Format:** [Markdown guidance with Python examples and JSON-like command result dictionaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Robot control should be reviewed and constrained before connection to live hardware.]

## Skill Version(s):

2.1.0 (source: ClawHub release metadata and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
