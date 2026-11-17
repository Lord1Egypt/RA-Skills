## Description:

Delegate tasks to OpenSpace, a full-stack autonomous worker for coding, DevOps, web research, and desktop automation, backed by an MCP tool and skill library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-rayluan](https://clawhub.ai/user/x-rayluan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to delegate coding, DevOps, web research, desktop automation, skill search, skill repair, and skill upload workflows to OpenSpace when local capabilities are insufficient or a multi-step task benefits from OpenSpace orchestration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delegated tasks and cloud skills may execute or import behavior that has not been reviewed locally.

Mitigation: Prefer local-only search and disable automatic cloud imports unless the operator has reviewed and approved the behavior.

Risk: Evolved or fixed skills may contain secrets, internal details, or project-specific behavior before upload.

Mitigation: Review and scan any evolved skill directory before reuse or upload.

Risk: Public upload can share skill changes more broadly than intended.

Mitigation: Require explicit approval before public uploads and use private visibility or skip upload for project-specific changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/x-rayluan/skills/openspace-delegate-task)
- [ClawHub Publisher Profile](https://clawhub.ai/user/x-rayluan)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and text responses with optional code, shell command, JSON, and configuration snippets returned by delegated OpenSpace tasks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task status, delegated task results, evolved skill summaries, and upload decisions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
