## Description: <br>
Grades user-provided IELTS Writing or Speaking responses against local band-descriptor rubrics after confirming the prompt when needed, then returns band scores, evidence, limitations, and actionable improvement advice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yezaijun](https://clawhub.ai/user/yezaijun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External IELTS learners, tutors, and test-preparation workflows use this skill to assess IELTS Writing and Speaking responses with criterion-level scores, textual evidence, confidence notes, and prioritized improvement guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence marks the release suspicious and describes behavior that may use powerful local or cloud CLIs and external reviewers. <br>
Mitigation: Review the installed bundle before use and choose restrictive review-helper options unless full-access nested agents or external LLM review of diffs is intended. <br>
Risk: IELTS Speaking pronunciation scoring has limited confidence when the user provides only text transcripts. <br>
Mitigation: State the pronunciation limitation in the scoring output and lower confidence for that criterion unless audio evidence is available. <br>
Risk: Writing scores can be misleading when the original prompt is incomplete or cannot be reliably verified. <br>
Mitigation: Confirm the complete Writing prompt first, cite the adopted prompt version, and mark task-response confidence lower when prompt provenance remains uncertain. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yezaijun/ielts-grading) <br>
- [IELTS writing scoring bands](https://www.chinaielts.org/prepare/understand-ielts-score/bands) <br>
- [IELTS writing band descriptors](https://cdn.ielts.org/Guides/ielts-writing-band-descriptors.pdf) <br>
- [IELTS speaking band descriptors](https://ielts.org/cdn/ielts-guides/ielts-speaking-band-descriptors.pdf) <br>
- [IELTS scoring in detail](https://www.ielts.org/ielts-for-organisations/ielts-scoring-in-detail) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown scoring report, usually in Chinese, with prompt confirmation, criterion scores, evidence, confidence, loss points, and improvement advice.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writing scores cover Task Achievement or Task Response, Coherence and Cohesion, Lexical Resource, and Grammatical Range and Accuracy; Speaking scores cover Fluency and Coherence, Lexical Resource, Grammatical Range and Accuracy, and Pronunciation with limited confidence when only transcripts are provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
