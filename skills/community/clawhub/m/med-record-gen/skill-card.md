## Description:

从中文医患对话文本生成门诊初诊病历，输出结构化分段的病历正文（文本）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaiccee](https://clawhub.ai/user/aaiccee)

### License/Terms of Use:

MIT-0

## Use Case:

Clinicians, medical documentation staff, and developers can use this skill to turn Chinese doctor-patient dialogue transcripts into structured outpatient initial visit record text for review. It is a documentation aid and requires final review by a licensed physician.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles doctor-patient dialogue that may contain personal health information, and the security evidence reports that raw dialogue is sent to an external API despite de-identification claims.

Mitigation: Review before installing; use only with consent and an approved data-processing pathway, or require local de-identification, explicit endpoint disclosure, and tests proving identifiers are not transmitted.

Risk: Generated medical-record text may be incomplete or clinically incorrect if the source dialogue is ambiguous or the generated output is flawed.

Mitigation: Require a licensed physician to review, correct, and approve the generated record before it is used for care or documentation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaiccee/skills/med-record-gen)
- [Publisher profile](https://clawhub.ai/user/aaiccee)
- [External record-generation API endpoint](https://shangbao.yunzhisheng.cn/skills/record-gen/gen_record_by_diag_v1)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [UTF-8 structured Chinese medical-record text, optionally written to a file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sections commonly include chief complaint, present illness, past history, physical examination, auxiliary examinations, diagnosis, and management.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
