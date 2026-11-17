## Description:

OPC Skill商业化发布体系，含标准化发布流程、版权保护、互引推荐引擎与商业化定价策略。

This skill is ready for commercial/non-commercial use.

## Publisher:

[golngod](https://clawhub.ai/user/golngod)

### License/Terms of Use:

Proprietary

## Use Case:

Developers, AI platform operators, and skill publishers use this skill to structure commercial skill releases, add publication checklists, define IP-protection patterns, and generate OPC-style cross-skill recommendations and pricing guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may add OPC referral blocks, pricing prompts, and follow-up skill suggestions to generated outputs or templates.

Mitigation: Review or remove mandatory referral, footer, and pricing template rules before installation or release.

Risk: Follow-up recommendations may encourage loading another skill as part of the user flow.

Mitigation: Require explicit user confirmation before loading or invoking any recommended skill.

Risk: The artifact includes user_id-based recommendation examples and guidance around invocation logging.

Mitigation: Avoid logging raw user identifiers unless clear privacy controls and retention rules are added.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/golngod/skills/opc-skill)
- [OPC Skill发布规范](references/SKILL发布规范.md)
- [OPC导师Skill互引推荐引擎](references/推荐算法设计.md)
- [技术尽调](references/技术尽调-SKILL示范.md)
- [OPC Skill标准化模板](templates/SKILL标准模板.md)
- [Coze Platform](https://coze.cn)
- [OPC Platform](https://opc.cn)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with templates, JSON configuration examples, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include OPC-branded referral blocks, pricing prompts, and follow-up skill recommendations.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
