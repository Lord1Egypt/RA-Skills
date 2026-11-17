## Description:

Get Shit Done - Full project planning and execution workflow. Handles project initialization with deep context gathering, automated research, roadmap creation, phase planning, and execution with verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oleg-schmidt](https://clawhub.ai/user/oleg-schmidt)

### License/Terms of Use:


## Use Case:

Developers and project teams use this skill to plan and execute greenfield or brownfield software projects through structured discovery, research, requirements, roadmap creation, phase planning, implementation, debugging, and verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad project write access, shell access, git commit authority, subagent execution, web research, and possible deployment or provider CLI authority can affect local projects or external services.

Mitigation: Install only where that level of autonomy is acceptable, review planned actions before execution, and use scoped test environments for provider or deployment workflows.

Risk: The security evidence flags risky secret handling patterns.

Mitigation: Do not paste production API keys into chat; use provider login flows, secret managers, masked inputs, or short-lived scoped credentials.

Risk: Autopilot, CCR, global npm link, .env verification, and remove-phase behavior require extra review before use.

Mitigation: Review those workflows before running them and require human confirmation for destructive or environment-changing actions.

## Reference(s):

- [CCR Integration](references/ccr-integration.md)
- [Checkpoint Execution](references/checkpoint-execution.md)
- [Checkpoint Types](references/checkpoint-types.md)
- [Checkpoints](references/checkpoints.md)
- [Continuation Format](references/continuation-format.md)
- [Deviation Rules](references/deviation-rules.md)
- [Framework Patterns](references/framework-patterns.md)
- [Git Integration](references/git-integration.md)
- [Model Profiles](references/model-profiles.md)
- [Planning Config](references/planning-config.md)
- [Questioning Guide](references/questioning.md)
- [TDD](references/tdd.md)
- [UI Patterns for Telegram](references/ui-brand.md)
- [UI Principles](references/ui-principles.md)
- [Verification Patterns](references/verification-patterns.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with code blocks, shell commands, configuration snippets, and generated planning files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write project planning artifacts under .planning/ and coordinate subagents, shell commands, git commits, web research, and provider CLI actions depending on the selected workflow.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
