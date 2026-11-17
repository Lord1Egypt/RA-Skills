## Description:

Create and manage task documents in the docs/todo/ workflow. Use when creating new tasks, updating task status, or moving tasks between workflow stages. Provides complete task lifecycle management with verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eduardou24](https://clawhub.ai/user/eduardou24)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to create, update, move, and verify task documents in a docs-first workflow under docs/todo/.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Placeholder shell-command examples could lead an agent to run unsafe file operations if copied directly with untrusted task slugs or agent names.

Mitigation: Review the skill before installing for untrusted requests; use strict slug and agent-name allowlists, quote shell variables, use -- before path operands where supported, and keep resolved paths under docs/todo/.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eduardou24/skills/ogt-docs-create-task)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with task templates and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces task lifecycle instructions, folder conventions, status signals, and verification checklists.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
