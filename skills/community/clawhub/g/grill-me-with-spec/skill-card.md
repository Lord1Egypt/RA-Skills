## Description:

Use when the user needs to create or refine a feature SPEC SDD before implementation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afonsoft](https://clawhub.ai/user/afonsoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to interview stakeholders in Portuguese, clarify ambiguous work, and draft a complete Spec-Driven Development document before implementation begins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SPEC documents may contain incomplete or incorrect requirements if user answers are incomplete.

Mitigation: Review the draft SPEC before approval and keep unresolved items marked as [A DEFINIR] until they are clarified.

Risk: The workflow may inspect repository files and create SPEC documents under .specs/.

Mitigation: Install only when repository inspection and local SPEC file creation are expected, and confirm downstream PR behavior before implementation.

## Reference(s):

- [SPEC SDD Template](references/spec-sdd-template.md)
- [Publisher source URL](https://github.com/afonsoft/skills)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Portuguese interview rounds and a Markdown SPEC SDD file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a .specs/SPEC-{YYYYMMDD}-{feature}.md draft and waits for user approval before implementation.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
