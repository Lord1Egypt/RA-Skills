## Description:

Designs gated, checkable sub-loops for medium or large AI-coding tasks and writes a runnable loop runbook without executing the loop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentjiang06](https://clawhub.ai/user/vincentjiang06)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to design reviewable, machine-checkable workflows for semi-autonomous coding tasks. It produces a loop specification and runbook rather than executing the proposed workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generating a runbook creates files in the target project's .loop/ directory.

Mitigation: Review the target project and intended output paths before generating the runbook.

Risk: The documented npx installation command is not pinned to an immutable version.

Mitigation: Verify the publisher and release before installation, and pin a reviewed version where possible.

Risk: Generated commands may affect a project if a user later runs them; local linting does not validate those effects.

Mitigation: Review generated checks and commands against the target project before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vincentjiang06/skills/loop-constructor)
- [Loop selection procedure](references/loop-selection.md)
- [Loop design specification](references/loop-design-shape.md)
- [Loop operating model](references/loops-model.md)

## Skill Output:

**Output Type(s):** [JSON configuration, Markdown runbook, Guidance]

**Output Format:** [JSON design and Markdown files under the target project's .loop/ directory]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a decision log and runnable checks; designs the loop but does not execute it.]

## Skill Version(s):

0.5.0 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
