## Description:

Get Shit Done - Full project planning and execution workflow. Handles project initialization with deep context gathering, automated research, roadmap creation, phase planning, and execution with verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oleg-schmidt](https://clawhub.ai/user/oleg-schmidt)

### License/Terms of Use:


## Use Case:

Developers and coding agents use GSD to initialize projects, gather requirements, research implementation options, create roadmaps, execute phase plans, and verify completed work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Highly autonomous project execution can make broad code, planning, or git changes.

Mitigation: Disable or tightly gate autopilot and YOLO behavior, and review plans before execution on private or production projects.

Risk: Workflows may involve secrets or external service credentials.

Mitigation: Avoid pasting live secrets into chat; prefer secret stores, masked environment configuration, or interactive authentication.

Risk: Deployment commands, destructive git operations, external-service changes, and global tool installs can affect production resources or the local environment.

Mitigation: Require explicit confirmation before these actions and review any global tool installs such as CCR.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oleg-schmidt/skills/glittercowboy)
- [Checkpoint execution reference](references/checkpoint-execution.md)
- [Checkpoint types reference](references/checkpoint-types.md)
- [Planning configuration reference](references/planning-config.md)
- [Git integration reference](references/git-integration.md)
- [Verification patterns reference](references/verification-patterns.md)
- [CCR integration reference](references/ccr-integration.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks, generated planning files, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update project planning artifacts and propose repository changes when invoked by the user.]

## Skill Version(s):

1.0.0 (source: server release metadata, released 2026-02-13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
