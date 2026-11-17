## Description:

为多平台内容发布提供状态管理、幂等对账、串行批处理和发布前质量门禁的编排指导。

This skill is ready for commercial/non-commercial use.

## Publisher:

[oracis](https://clawhub.ai/user/oracis)

### License/Terms of Use:

MIT-0

## Use Case:

内容运营人员和开发者用它规划多平台发布流程、核对本地与远端状态，并在重试或批量发布前检查内容与发布结果。它提供编排指导，不提供各平台的发布适配器。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A missing or stale publishing record can lead to duplicate posts or skipped content.

Mitigation: Synchronize existing platform records before publishing and reconcile local and remote state before retrying.

Risk: A successful save action may not mean the remote draft contains the intended content.

Mitigation: Read back the remote draft and compare its content before marking it saved or published.

Risk: Content suitable for one platform may violate another platform's rules.

Mitigation: Check each destination's requirements and inspect all rendered text, including text on images, before publishing.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/oracis/skills/multiplatform-publish-core)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with command and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance only; no executable payload or platform-specific posting adapter.]

## Skill Version(s):

0.3.0 (source: server-resolved release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
