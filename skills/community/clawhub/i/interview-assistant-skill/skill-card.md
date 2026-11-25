## Description:

基于腾讯会议(tmeet)通讯录与会议录制/纪要，覆盖面试全链路：会前生成候选人画像与结构化面试提纲，会中记录关键信息，会后输出带维度评分与录用建议的结构化评估。

This skill is ready for commercial/non-commercial use.

## Publisher:

[golgys0621](https://clawhub.ai/user/golgys0621)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, hiring managers, interviewers, and recruiting operations teams use this skill to prepare structured interviews, organize meeting notes or transcripts, and produce evidence-based candidate evaluation summaries. It supports both Tencent Meeting-assisted workflows and a local file-based helper for resumes, job descriptions, and interview notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes sensitive hiring data, including resumes, contact details, meeting recordings, transcripts, and interview notes.

Mitigation: Use it only when authorized, obtain appropriate consent, and follow organizational privacy, retention, and access-control requirements.

Risk: Generated scores and hiring recommendations may be incomplete or reflect bias in source notes, transcripts, or keyword-based signals.

Mitigation: Treat outputs as decision support, require human review, and apply the organization's bias-review and hiring compliance process before making employment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/golgys0621/skills/interview-assistant-skill)
- [面试评估模板](artifact/references/evaluation_template.md)
- [Offline interview helper](artifact/scripts/interview_helper.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown interview outlines, notes summaries, scoring tables, recommendations, and optional shell commands for the local Python helper.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses five evaluation dimensions and marks missing evidence as items to verify; the local helper uses explainable keyword-signal scoring.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
