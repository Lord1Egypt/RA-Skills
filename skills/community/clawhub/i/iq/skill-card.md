## Description:

Generate IQ tests, brain teasers, logical puzzles, riddles, and cognitive training challenges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tools](https://clawhub.ai/user/tools)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate IQ-style tests, brain teasers, daily mental challenges, and browser-based quiz experiences for practice or entertainment. Generated score ranges and feedback should be treated as informal guidance, not clinical assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Interactive HTML tests can run unsanitized quiz or answer content as browser code.

Mitigation: Use only trusted question content, avoid embedding user-provided HTML, and host generated tests only on non-sensitive origins unless the template is fixed to render quiz and answer text safely.

Risk: Generated IQ-style scores and feedback can be mistaken for formal cognitive assessment.

Mitigation: Present score ranges and recommendations as informal practice feedback and avoid using them for clinical, hiring, education, or other high-stakes decisions.

## Reference(s):

- [IQ Question Bank Reference](references/question_bank.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, plain text, JSON, and interactive HTML]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated questions, answer keys, explanations, puzzle solutions, HTML quiz files, and performance feedback.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
