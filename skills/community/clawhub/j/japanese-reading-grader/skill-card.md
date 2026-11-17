## Description:

A1/A2/B1(N5/N4/N3)日语朗读音频作业批改，faster-whisper ASR+声学双通道四维AI评测；支持单人/批量批改、纠错反馈、成绩归档；AI预批改，教师人工终审，满分10分。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bianmaxingkong](https://clawhub.ai/user/bianmaxingkong)

### License/Terms of Use:

MIT-0

## Use Case:

Teachers use this skill to pre-grade Japanese reading audio assignments for A1/A2/B1 learners, generate concise feedback, and support batch grading records. The skill is designed as an AI-assisted workflow with teacher review before final grades are recorded.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Student audio, scores, reports, and progress files may contain sensitive education data.

Mitigation: Use the skill only in authorized teaching contexts, keep generated files in restricted course folders, minimize student identifiers, and follow school retention rules for deletion or archival.

Risk: ASR or acoustic analysis can misidentify pronunciation or reading errors, especially for low-confidence audio.

Mitigation: Use the skill's confidence tiers and require teacher review for low-confidence cases and pronunciation-sensitive deductions before recording final grades.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bianmaxingkong/skills/japanese-reading-grader)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown or plain text feedback reports with scores, diagnostic notes, correction suggestions, and optional local report/progress file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce per-student report text, batch progress records, failed-audio records, and teacher-review prompts for low-confidence or pronunciation-sensitive findings.]

## Skill Version(s):

2.2.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
