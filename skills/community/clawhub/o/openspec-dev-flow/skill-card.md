## Description:

Provides a Chinese OpenSpec-based iterative development workflow for planning, implementing, verifying, and archiving creation or code-change tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangxiaoqian007](https://clawhub.ai/user/huangxiaoqian007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to run an OpenSpec-style workflow for feature work, refactoring, bug fixes, and skill development with staged proposal, implementation, verification, and archive steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has broad activation for creation and development tasks, so it may introduce OpenSpec planning into many workflows.

Mitigation: Install it only when OpenSpec planning is desired for those workflows, and review whether the trigger behavior fits the target agent environment.

Risk: The documented skip-confirmation phrases allow the agent to proceed without staged review prompts.

Mitigation: Avoid those phrases unless the user is comfortable with the agent moving through planning and implementation without each intermediate confirmation.

Risk: The workflow can create OpenSpec documents and guide code changes.

Mitigation: Review generated planning documents and resulting code changes before committing, deploying, or distributing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huangxiaoqian007/skills/openspec-dev-flow)
- [OpenSpec official documentation](https://github.com/Fission-AI/OpenSpec)
- [OpenSpec Getting Started](https://github.com/Fission-AI/OpenSpec/blob/main/docs/getting-started.md)
- [OpenSpec Workflows](https://github.com/Fission-AI/OpenSpec/blob/main/docs/workflows.md)
- [OpenSpec Commands](https://github.com/Fission-AI/OpenSpec/blob/main/docs/commands.md)
- [OpenSpec Concepts](https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with proposed file changes and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates OpenSpec planning documents and may guide code changes when the workflow reaches implementation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
