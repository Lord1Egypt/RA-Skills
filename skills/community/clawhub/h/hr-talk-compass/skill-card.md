## Description:

HR 员工谈心与 OD 洞察助手，帮助 HR 准备员工一对一、演练关键对话、赋能业务经理，并将谈后复盘沉淀为组织诊断信号。

This skill is ready for commercial/non-commercial use.

## Publisher:

[realzjr](https://clawhub.ai/user/realzjr)

### License/Terms of Use:

MIT

## Use Case:

HR, HRBP, OD, and people managers use this skill to prepare employee one-on-ones, rehearse sensitive conversations, create follow-up plans, and summarize de-identified conversation signals for organizational diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask users to create or aggregate sensitive employee profiles and risk records.

Mitigation: Use only approved HR and AI data-processing workflows, minimize inputs, use employee codes, avoid raw personal quotes where possible, restrict access, and define retention and deletion rules.

Risk: Generated risk labels or OD summaries could affect employment decisions if treated as authoritative.

Mitigation: Use outputs as decision-support only; require qualified human review before any employment, performance, retention, or escalation decision.

Risk: Employee conversations may surface psychological crisis, legal, medical, harassment, discrimination, or labor-dispute matters.

Mitigation: Stop general AI analysis for those matters and route them to approved EAP, legal, compliance, medical, or HR specialist processes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/realzjr/skills/hr-talk-compass)
- [Methodology source: 数字生命卡兹克 article](https://mp.weixin.qq.com/s/VDlBdkspV0SQNFJYLxOogQ)

## Skill Output:

**Output Type(s):** [Text, Markdown, YAML, Guidance]

**Output Format:** [Markdown guidance with optional structured YAML records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only outputs include conversation outlines, coaching notes, follow-up scripts, risk labels, OD summaries, and de-identified structured records.]

## Skill Version(s):

1.1.0 (source: server release metadata and CHANGELOG, released 2026-07-31)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
