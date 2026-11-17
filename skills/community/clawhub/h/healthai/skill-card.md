## Description:

Provides health-report analysis, health-risk summaries, personalized exercise plans, and daily check-in reminders from text, document, and OCR inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amitabhama](https://clawhub.ai/user/amitabhama)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and agents use this skill to extract health indicators from reports, identify abnormal values, generate exercise and diet guidance, record check-ins, and prepare health-tracking documents. It is intended for personal health management support, not clinical diagnosis or treatment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive health, check-in, messaging, and document data may be stored locally or sent through Feishu or Tencent Docs.

Mitigation: Use an isolated account, remove packaged identifiers and credentials, and decide explicitly where health data may be stored or transmitted before enabling the skill.

Risk: Broad health-related triggers and persistent reminders may activate the skill or send messages more often than intended.

Mitigation: Narrow the activation triggers and disable heartbeat or cron setup unless recurring reminders are explicitly required.

Risk: Shell command construction and cron setup can change the local environment or execute unsafe commands.

Mitigation: Review commands before installation, replace shell=True command construction with argument-list subprocess calls, and avoid automatic cron changes in shared or production environments.

Risk: Health-risk summaries and exercise or diet plans can be mistaken for medical advice.

Mitigation: Present generated guidance as informational support only and require professional medical review for diagnosis, treatment, severe symptoms, or abnormal results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/amitabhama/skills/healthai)
- [Publisher profile](https://clawhub.ai/user/amitabhama)
- [Health indicator reference ranges](artifact/references/指标参考范围.md)
- [Calorie calculation reference](artifact/references/卡路里计算参考.md)
- [Tencent Docs token setup](https://docs.qq.com/open/auth/mcp.html)
- [Feishu Open Platform](https://open.feishu.cn/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON health records and plans, shell commands, configuration snippets, and document links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist local health and check-in JSON data and may send reminders or document updates through Feishu or Tencent Docs when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact SKILL.md reports 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
