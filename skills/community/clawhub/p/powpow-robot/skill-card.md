## Description:

向 PowPow 全球地图部署和管理 OpenClaw 机器人，包括创建、移动、删除和分配任务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to deploy OpenClaw robots to the PowPow global map, locate them, move them, and assign tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is rated suspicious because bulk deletion has no confirmation step and script inspection was incomplete.

Mitigation: Review the complete script and verify which robots will be affected before deleting; avoid delete --all until its effects are understood.

## Reference(s):

- [PowPow Global Map](https://global.powpow.online/map)
- [PowPow API](https://global.powpow.online/api)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Text, Guidance]

**Output Format:** [Markdown with shell command examples and operation summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands and guidance for robot account, location, and task operations.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
