## Description:

This skill helps agents write structured Chinese-language interview evaluations from transcripts, recordings, or interviewer notes for hiring decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soulzhong](https://clawhub.ai/user/soulzhong)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, hiring managers, and interviewers use this skill to convert Chinese interview transcripts, recordings, video notes, or interviewer notes into structured internal hiring evaluations. It emphasizes evidence-backed capability judgments, risk flags, and specific next-step recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may consult prior conversations and local resume files when resolving candidate names.

Mitigation: Use explicit file boundaries, avoid broad resume directories, and require user confirmation before using prior conversations or local resumes.

Risk: The skill may persist hiring-related feedback into reusable guidance.

Mitigation: Require review before writing feedback into shared reference notes, and keep candidate-specific information out of reusable guidance.

Risk: Hiring recommendations may affect candidates if transcript evidence is incomplete, misattributed, or weakly reviewed.

Mitigation: Require human review of the final evaluation for evidence quality, role relevance, fairness, and compliance with the hiring process.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/soulzhong/skills/interview-evaluation)
- [Capability Dimensions](artifact/capability-dimensions.md)
- [Attribution Errors](artifact/attribution-errors.md)
- [Probing Techniques](artifact/probing-techniques.md)
- [Evaluation Template](artifact/evaluation-template.md)
- [Example Evaluation](artifact/example-evaluation.md)
- [Evolution Log](artifact/EVOLUTION.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, files]

**Output Format:** [Chinese Markdown interview evaluation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured recommendation, strengths, weaknesses, risks, and next-step sections; the skill instructs agents to save the final evaluation as a Markdown file.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
