## Description:

养老与传承会谈纪要整理自动生成 Skill。把客户沟通录音转写、聊天记录、自由笔记或零散信息，整理成结构化会谈纪要整理：家庭架构（含虚线框未确认项）、五板块信息矩阵（健康/财务/房产居住/家庭关系/现有保障）、风险信号初判、信息缺口清单、客户画像与可直接发送的跟进消息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hukaiyi777](https://clawhub.ai/user/hukaiyi777)

### License/Terms of Use:

MIT-0

## Use Case:

养老与传承顾问 and related client-service teams use this skill to turn Chinese-language client conversations, call transcripts, chat records, and notes into structured internal meeting notes. It organizes family structure, health, finance, housing, family relationships, existing protection, risk signals, information gaps, client profile, next actions, and a client-facing follow-up message.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Client meeting materials may contain sensitive personal, family, financial, medical, contact, identity, account, or third-party information.

Mitigation: Remove unnecessary identifiers before use and confirm permission to process client or family information.

Risk: The skill works in insurance, medical, legal, regulatory, and trust-related contexts where unverified outputs could be mistaken for professional conclusions.

Mitigation: Human reviewers should verify related facts and keep externally shared messages desensitized and appropriately toned.

Risk: Generic trigger phrases may cause unwanted auto-invocation in agents that automatically select skills.

Mitigation: Narrow the invocation triggers when deploying in environments with automatic skill routing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hukaiyi777/skills/hky-meeting-notes)
- [hky-insure-risk-report](https://github.com/hukaiyi777/hky-insure-risk-report)
- [hky-insure-solution](https://github.com/hukaiyi777/hky-insure-solution)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are structured meeting notes with five information categories, family-structure notes, risk signals, information gaps, next actions, and a concise follow-up message.]

## Skill Version(s):

0.1.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
