## Description:

Intelligent orchestrator for the Platonic Coding workflow that auto-detects project state and routes agents through initialization, recovery, RFC specification, implementation, testing, and review tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caesar0301](https://clawhub.ai/user/caesar0301)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to run a specification-driven development workflow: bootstrap project structure, recover specifications from existing code, manage RFCs, implement from guides with tests, and review code for specification compliance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project configuration can steer write-capable workflows without clear path confinement.

Mitigation: Review `.platonic.yml` before use, keep specs, impl, and drafts paths relative to the project, inspect proposed plans before write-capable modes, and reserve auto-mode or "no confirmations" for trusted repositories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caesar0301/skills/platonic-coding)
- [Platonic Coding complete reference](references/REFERENCE.md)
- [Workflow overview](references/WORKFLOW/workflow-overview.md)
- [Implementation full workflow](references/IMPL/impl-full.md)
- [Spec compliance review](references/REVIEW/review-spec-compliance.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with proposed file changes, templates, commands, implementation plans, and review reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write project files through initialization, specification, implementation, and review workflows when the agent has workspace access.]

## Skill Version(s):

2.3.0 (source: server release metadata and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
