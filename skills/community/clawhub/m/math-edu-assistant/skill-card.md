## Description:

数学教材同步教育助手，用于在数学学习请求中提供知识点讲解、智能出题、作业批改和解题答疑，覆盖小学至高中数学并按教材章节范围输出。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gzybt](https://clawhub.ai/user/gzybt)

### License/Terms of Use:

MIT-0

## Use Case:

External learners, parents, and educators use this skill for Simplified Chinese K12 math tutoring, practice generation, homework review, and step-by-step problem explanation. It is intended to keep responses within the relevant grade, chapter, problem type, and difficulty.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad math-help activation examples may cause the skill to be selected for loosely worded mathematics requests in environments with many skills.

Mitigation: Review the activation examples and keep routing constrained to K12 mathematics tutoring, practice generation, homework review, and problem explanation.

Risk: Generated tutoring, grading, or practice content can be incorrect or exceed the learner's intended curriculum level.

Mitigation: Check grade, chapter, difficulty, and final math results before relying on outputs for teaching, assessment, or study plans.

Risk: Image-based homework review depends on the host platform's visual understanding and may misread handwritten or low-quality inputs.

Mitigation: Prefer text input for critical grading and ask the learner to clarify ambiguous symbols, diagrams, or answer steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gzybt/skills/math-edu-assistant)
- [Publisher profile](https://clawhub.ai/user/gzybt)
- [课程知识图谱 — K12 数学教材同步](references/curriculum_map.md)
- [核心知识点速查库](references/knowledge_points.md)
- [题目模板与出题规范](references/question_templates.md)
- [批改评分标准](references/grading_rubric.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with LaTeX math notation and structured tutoring sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include explanations, original practice questions, answer keys, grading feedback, and study suggestions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
