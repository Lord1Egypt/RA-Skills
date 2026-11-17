## Description:

Internalize Me helps developers analyze an open-source project against AI Agent and LLM engineering competency dimensions and turn the codebase into a learning plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoyta](https://clawhub.ai/user/zhaoyta)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect an open-source repository, identify which AI Agent and LLM engineering competencies it demonstrates, and generate focused learning materials from concrete code evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Markdown may add incorrect analysis or unwanted learning-plan files under a repository's .learn directory.

Mitigation: Review generated .learn files before committing them, especially in shared repositories or projects with automation that reacts to new files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaoyta/skills/internalize-me)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown reports written under .learn/<project-slug>/]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates limited Markdown files in the analyzed project's .learn directory.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
