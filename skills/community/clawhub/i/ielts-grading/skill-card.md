## Description:

根据用户提供的雅思写作或口语回答进行官方标准评分。使用前先联网检索并确认原始题目，再按本项目内评分标准逐维度打分、给出总分与可执行改进建议。适用于用户提到 IELTS/雅思、作文批改、口语评分、band 分数、Task 1/Task 2、speaking mock 等场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yezaijun](https://clawhub.ai/user/yezaijun)

### License/Terms of Use:

MIT-0

## Use Case:

External learners, tutors, and exam-preparation users use this skill to score IELTS Writing or Speaking responses against local official-style band descriptors. It returns evidence-backed criterion scores, an overall band estimate, confidence notes, and prioritized improvement guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Writing prompt verification may expose personal identifiers, candidate numbers, or private exam-session details if they are included in search queries.

Mitigation: Ask users to omit private identifiers and offer a local-only or no-web rubric review when web verification is not needed.

Risk: Speaking scores based only on transcripts cannot support high-confidence pronunciation assessment.

Mitigation: State that pronunciation is low confidence when no audio is available and base the rest of the score on visible transcript evidence.

Risk: Prompt-version conflicts or unverified remembered prompts can reduce confidence in task-response scoring.

Mitigation: Report the adopted prompt version and sources when available; if no reliable prompt is found, grade against the user-provided version and lower the relevant confidence.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yezaijun/skills/ielts-grading)
- [雅思写作评分标准](artifact/写作评分标准.md)
- [雅思口语评分标准](artifact/口语评分标准.md)
- [中国雅思官网计分说明](https://www.chinaielts.org/prepare/understand-ielts-score/bands)
- [IELTS Writing Band Descriptors](https://cdn.ielts.org/Guides/ielts-writing-band-descriptors.pdf)
- [IELTS Speaking Band Descriptors](https://ielts.org/cdn/ielts-guides/ielts-speaking-band-descriptors.pdf)
- [IELTS Scoring in Detail](https://www.ielts.org/ielts-for-organisations/ielts-scoring-in-detail)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown, usually in Chinese, with score breakdowns, evidence excerpts, confidence notes, and improvement suggestions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source links for writing prompt verification and low-confidence notes when prompt, transcript, or audio evidence is incomplete.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
