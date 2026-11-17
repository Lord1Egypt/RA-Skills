## Description:

AI 伴学助手 is a K-12 homework companion that recognizes submitted questions from text, images, screenshots, or speech, guides students with Socratic tutoring, creates wrong-question notebooks, and produces parent reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wukongmazi](https://clawhub.ai/user/wukongmazi)

### License/Terms of Use:

MIT-0

## Use Case:

External users, especially parents and students, use this skill to support K-12 homework study through guided explanations, OCR or ASR question intake, optional spoken explanations, wrong-question tracking, and parent-facing progress reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Homework images, screenshots, audio, and generated explanation text may be sent to Tencent Cloud for OCR, ASR, or TTS processing.

Mitigation: Use the cloud features only with parent or guardian approval, and avoid submitting files that include a child's real name, school, address, or other identifiers.

Risk: Wrong-question notebooks and parent reports may contain children's study records and sensitive learning context.

Mitigation: Store generated Excel notebooks and reports in private locations, review them before sharing, and avoid recording unnecessary identity information.

Risk: The dependency file uses a lower-bound Tencent Cloud SDK requirement rather than pinned package versions.

Mitigation: Pin and review dependency versions before deployment in a managed or commercial environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wukongmazi/skills/homework-companion)
- [Subject Playbooks](references/subject-playbooks.md)
- [Safety Rules](references/safety-rules.md)
- [Wrong-Question Notebook](references/wrong-question-notebook.md)
- [Parent Report](references/parent-report.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration guidance]

**Output Format:** [Conversational text with optional Markdown reports, Excel notebooks, MP3 audio files, and shell commands for OCR, ASR, and TTS scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Tencent Cloud OCR, ASR, and TTS scripts when credentials and dependencies are configured.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
