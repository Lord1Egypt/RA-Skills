## Description:

Ensures alignment between user and Claude during feature/spec planning through a structured interview process.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiao1804](https://clawhub.ai/user/xiao1804)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to run a structured requirements interview before planning non-trivial implementation work, including new features and refactors. It helps capture technical constraints, scope boundaries, risk tolerance, success criteria, and validation expectations before codebase exploration and implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approving the generated plan is treated as consent for the agent to begin implementation immediately.

Mitigation: Review the plan, success criteria, and implementation checklist carefully before approving it.

Risk: Installing through an unpinned package command can weaken supply-chain assurance.

Mitigation: Pin or verify the installer and source revision before running the install command.

## Reference(s):

- [Plan Interview on ClawHub](https://clawhub.ai/xiao1804/skills/plan-interview)
- [Iterative Plan Refinement Prompts](references/iterative-plan-refinement-prompts.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown plans, user-facing questions, checklists, and concise implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or refine plan files and convert an approved plan into tracked implementation tasks.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
