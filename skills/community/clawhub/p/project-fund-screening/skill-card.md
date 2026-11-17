## Description:

为寻求融资的初创或成长期项目做初步筛选诊断，同时对照 VC/PE 分阶段 BP 标准与政府引导或产投基金落地要求，输出结构化达标度、红旗清单与整改建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuiwensm99](https://clawhub.ai/user/zhuiwensm99)

### License/Terms of Use:

MIT-0

## Use Case:

External users, founders, FA teams, investment bankers, and fundraising advisors use this skill to screen startup or growth-stage projects before fundraising. It compares project facts against VC/PE stage expectations and China government or industrial fund landing requirements, then highlights readiness scores, red flags, evidence gaps, and improvement steps.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The reports are preliminary screening outputs and may not reflect current local fund rules or city-specific application guidance.

Mitigation: Verify current local fund rules and official city guidance before making financing, landing, or application decisions.

Risk: Generated Markdown could be unsafe if rendered with raw HTML or automatic remote-image loading enabled.

Mitigation: Render reports in a Markdown viewer that disables raw HTML and automatic remote-image loading, especially for externally supplied project data.

Risk: Attacker-controlled JSON could lead to misleading report content or unsafe downstream rendering behavior.

Mitigation: Use trusted project inputs, review generated reports before sharing, and sanitize content before publishing or rendering in web contexts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhuiwensm99/skills/project-fund-screening)
- [Publisher profile](https://clawhub.ai/user/zhuiwensm99)
- [筛选标准细则（参考知识库）](references/standards.md)
- [评分卡与权重（Rubric）](references/scorecards.md)
- [项目筛选诊断 — 输入模板与输出骨架](assets/diagnosis-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese-language Markdown report with optional JSON summary and local shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports mark missing project facts as pending verification and include VC/PE readiness, government fund landing fit, red flags, and remediation guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
