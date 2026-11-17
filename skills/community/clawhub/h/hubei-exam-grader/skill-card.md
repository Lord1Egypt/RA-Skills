## Description:

按湖北技能高考计算机类规则批改答卷并标注八类错因标签，输出结构化判分结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[z324169276](https://clawhub.ai/user/z324169276)

### License/Terms of Use:

MIT-0

## Use Case:

Teachers and other graders use this skill to assess answers for Hubei's computer-category vocational skills exam. It applies the supplied scoring rules, labels each incorrect answer with one primary error cause, and returns explanations and review suggestions.

### Deployment Geography for Use:

China (Hubei Province)

## Known Risks and Mitigations:

Risk: The security review is incomplete because one reference could not be resolved, and grading results may be unreliable if the supplied rubric does not match current exam criteria.

Mitigation: Check the referenced rubric and confirm it against current official exam criteria; review borderline answers before relying on scores.

## Reference(s):

- [Scoring Rubrics and Error Labels](references/rubrics.md)
- [ClawHub Skill Listing](https://clawhub.ai/z324169276/skills/hubei-exam-grader)
- [Imported GitHub Source](https://github.com/z324169276/hubei-exam-skills/tree/main/hubei-exam-grader)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON with per-question verdicts, scores, error labels, explanations, and review suggestions; batch grading also includes a class summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Per-question explanations are 120–200 Chinese characters; batch grading summarizes error labels, weak topics, and questions for review.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
