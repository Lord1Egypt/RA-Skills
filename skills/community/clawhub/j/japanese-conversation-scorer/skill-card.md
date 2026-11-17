## Description:

Grades A1, A2, and B1 Japanese conversation-test audio by transcribing responses with faster-whisper, producing teacher-reviewed pre-scores across content completeness, accuracy, and fluency, plus teacher and student feedback reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bianmaxingkong](https://clawhub.ai/user/bianmaxingkong)

### License/Terms of Use:

MIT-0

## Use Case:

External educators and language-program staff use this skill to batch grade Japanese conversation-test recordings, review ASR-backed pre-scores, and generate separate detailed teacher reports and concise student feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional course-platform adapters may post student grades and feedback through APIs without a clearly required final confirmation or dry-run.

Mitigation: Use the default CSV or local-report workflow, keep tokens in local config or environment variables, and require a teacher-reviewed preview before any adapter posts grades or feedback.

Risk: ASR-backed pre-scores can be unreliable when audio quality, transcript alignment, or recognition confidence is low.

Mitigation: Treat low-confidence AI scores as internal diagnostics only and require the teacher to provide the final score before student-facing feedback is released.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bianmaxingkong/skills/japanese-conversation-scorer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain-text feedback reports with inline shell commands and CSV-compatible summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces teacher-facing detailed reports, student-facing concise feedback, and optional CSV exports; low-confidence ASR results require teacher scoring.]

## Skill Version(s):

1.1.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
