## Description:

面向招聘与团队搭建场景的技能编排助手。用户提供公司名称、行业赛道或公司类型时，先检索公司与岗位画像信息，再在 claw.ai / ClawHub 搜索可用技能，产出“可一键安装”的角色技能包建议，并在用户确认后执行安装。适用于初次搭建 AI 团队角色、按行业快速选型技能、以及基于公司背景做技能组合推荐。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tato447](https://clawhub.ai/user/tato447)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiting, operations, and team-building users use this skill to turn a company name, industry, or company type into a concise company or industry profile, grouped candidate skills, and a confirmation-gated one-click skill package recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends and installs bundles of other skills, which can change the user's agent environment.

Mitigation: Review each recommended skill before installation, including publisher, exact skill ID and version, requested permissions, and uninstall or rollback options.

Risk: Unknown third-party skills may be unsafe in environments containing sensitive data or credentials.

Mitigation: Avoid installing unknown third-party skills into sensitive agent environments, and use the confirmation step to reject or revise risky recommendations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tato447/skills/longxia-zhipin)
- [Industry Taxonomy](references/industry-taxonomy.md)
- [Role Pack Playbook](references/role-pack-playbook.md)
- [English Output Templates](references/output-templates-en.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with structured recommendations, confirmation prompts, and installation result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose skill installation bundles and fallback choices; installation should occur only after explicit user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
