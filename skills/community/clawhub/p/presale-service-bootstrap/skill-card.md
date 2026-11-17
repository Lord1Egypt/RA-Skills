## Description:

Scaffold a presale service foundation with docs, configuration, implementation plans, launch materials, and readiness checks before coding begins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dtsiomo](https://clawhub.ai/user/dtsiomo)

### License/Terms of Use:


## Use Case:

Developers and presale automation teams use this skill to create a reusable project foundation before implementation. It helps capture scope, non-goals, governance configuration, verification plans, and readiness criteria for one-pass execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated plans and launch materials may guide implementation or deployment with incomplete project context.

Mitigation: Review the scope, non-goals, verification matrix, and readiness checklist before coding or deployment.

Risk: The skill can create or request local project directories and planning documents.

Mitigation: Run it in the intended workspace and review generated files before using them as execution inputs.

Risk: The artifact references an optional scaffold script that is not included in the submitted files.

Mitigation: Verify any external scaffold script separately before execution.

## Reference(s):

- [Workflow](references/workflow.md)
- [Required Artifacts](references/artifacts.md)

## Skill Output:

**Output Type(s):** [markdown, configuration, guidance, shell commands]

**Output Format:** [Markdown documents, YAML configuration, checklists, and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local project scaffolding artifacts and keeps coding blocked until readiness gates are satisfied.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
