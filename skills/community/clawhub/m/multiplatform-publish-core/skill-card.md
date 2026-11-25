## Description:

为多平台内容发布提供编排指导，涵盖状态清单、幂等判据、串行批处理和发布前质量门禁。

This skill is ready for commercial/non-commercial use.

## Publisher:

[oracis](https://clawhub.ai/user/oracis)

### License/Terms of Use:

MIT

## Use Case:

面向开发者和内容运营人员，用于规划和核对多平台发布流程，尤其是重发幂等、草稿回读、批次串行和发布前合规检查。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reconciliation that matches posts by title could delete or replace distinct posts that share a title.

Mitigation: Use stable remote IDs for matching and require explicit confirmation before deleting or merging items.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/oracis/skills/multiplatform-publish-core)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Code]

**Output Format:** [Markdown guidance with workflow diagrams, tables, code, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Platform-independent orchestration guidance; platform adapters and a complete implementation are not included in this release.]

## Skill Version(s):

0.3.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
