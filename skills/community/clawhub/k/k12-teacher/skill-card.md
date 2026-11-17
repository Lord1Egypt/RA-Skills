## Description:

Provides structured, syllabus-aligned K-12 instruction, assessment, and feedback across subjects, with teaching strategies adapted to learner level.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnsmithfan](https://clawhub.ai/user/johnsmithfan)

### License/Terms of Use:

GNU GPL v3

## Use Case:

External K-12 learners and educators use the skill's prompts and references to plan lessons, adapt explanations to learner needs, create assessments, and provide feedback. It supports instruction but does not confer educator licensure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled pull-request-title workflow can execute commands embedded in a pull-request title.

Mitigation: Disable or repair the workflow before enabling GitHub Actions, and pass the title through an environment variable rather than embedding it in shell code.

Risk: The teaching material is English-focused, the curriculum knowledge base is incomplete, and its updater is a placeholder.

Mitigation: Verify instruction against current, authoritative local curricula and do not rely on the updater for complete or current syllabus content.

Risk: The skill does not confer educator licensure.

Mitigation: Present its output as instructional support, not as professional credentials or a substitute for qualified educator oversight.

## Reference(s):

- [Source repository](https://github.com/JohnSmithfan/K12-Teacher)
- [ClawHub release](https://clawhub.ai/johnsmithfan/skills/k12-teacher)
- [Instructional method patterns](references/method-patterns.md)
- [Curriculum knowledge base](references/knowledge-base.md)
- [Syllabus registry](references/syllabus-registry.md)
- [Grade crosswalk](references/grade-crosswalk.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Educational guidance, Lesson plans, Assessment items, Learner feedback]

**Output Format:** [Structured Markdown lessons, explanations, assessments, and feedback]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Adapted to learner grade, subject, and performance tier.]

## Skill Version(s):

0.1.2 (source: server-resolved ClawHub release metadata; artifact/SKILL.md lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
