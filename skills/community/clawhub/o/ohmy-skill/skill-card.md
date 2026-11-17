## Description:

ClawHub 技能的体检 + 评分 + 自动优化 + 排行榜查询 + 智能推荐基础设施。OhMySkill 系列首款产品。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hunterdeng500](https://clawhub.ai/user/hunterdeng500)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ClawHub users use this skill to inspect and score SKILL.md files, generate optimization suggestions, query ClawHub skill rankings, and get skill recommendations based on a need or installed skill stack.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation phrases may cause the skill to be invoked when the user intended a narrower skill-quality request.

Mitigation: Invoke it with explicit "ohmy skill" wording and review trigger phrases before installing in shared environments.

Risk: Generated optimization suggestions can introduce incorrect or misleading guidance into a SKILL.md file.

Mitigation: Review generated changes, scan the revised skill, and test expected invocation paths before deployment.

Risk: The artifact is written primarily in Chinese, which may make review harder for teams that do not read Chinese.

Mitigation: Have a reviewer who can read the source language confirm behavior, triggers, and generated recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hunterdeng500/skills/ohmy-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown with scored findings, recommendations, rankings, and revised SKILL.md content when optimization is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include before/after comparisons for token use, invocation success, or skill quality improvements.]

## Skill Version(s):

1.1.0 (source: frontmatter and changelog, released 2026-04-22)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
