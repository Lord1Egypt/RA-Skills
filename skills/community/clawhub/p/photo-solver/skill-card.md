## Description:

AI photo-based problem solver that accepts problem images or text, identifies the subject area, provides step-by-step solutions, and generates an interactive HTML solution report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External learners and study helpers use this skill to turn uploaded homework or practice-problem images into subject-aware explanations, final answers, and an HTML study report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded problem images or generated reports may contain private study material.

Mitigation: Avoid using the skill with sensitive exams or private material that should not be persisted in a local HTML report.

Risk: Photo recognition can misread blurry, reflective, handwritten, or incomplete problem statements.

Mitigation: Ask the user to confirm uncertain text, mark unclear content explicitly, and request a clearer image or text supplement when needed.

Risk: The skill could be used to seek answers for an active exam.

Mitigation: Refuse assistance with ongoing exam questions and redirect the user to practice, review, or past-paper analysis.

## Reference(s):

- [Skill page](https://clawhub.ai/bettermen/skills/photo-solver)
- [Subject Taxonomy](references/subject-taxonomy.md)
- [Quality Checklist](references/quality-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Concise text response plus a generated HTML report file with KaTeX-formatted solution content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves a local photo-solver-report.html file and presents it to the user.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
