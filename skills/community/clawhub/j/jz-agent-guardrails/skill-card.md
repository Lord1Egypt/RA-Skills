## Description:

Agent Guardrails provides mechanical enforcement tools that help AI coding agents avoid reimplementation, secret leaks, deployment gaps, and skill update gaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jzocb](https://clawhub.ai/user/jzocb)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill to add repository-level guardrails for AI coding agents, including Git hooks, secret checks, deployment verification, and import registry guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs persistent Git hooks and can affect repositories that already have hook workflows.

Mitigation: Review installation scripts and existing hooks before use, then customize generated hooks for the target repository.

Risk: Secret scanning can expose matched secret values in shared logs.

Mitigation: Run secret checks in controlled environments and redact or suppress matched values before sharing logs.

Risk: Installer behavior is described by the security review as broken or overstated, including a missing pre-commit asset.

Mitigation: Verify installed files and hook behavior manually before relying on the skill as enforcement.

Risk: The skill update feedback loop adds persistent post-commit automation and semi-automatic skill commit behavior.

Mitigation: Enable the feedback loop only in repositories where persistent automation and human-confirmed skill updates are acceptable.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/jzocb/skills/jz-agent-guardrails)
- [Server-resolved homepage](https://github.com/anon/agent-guardrails#readme)
- [Deployment verification guide](references/deployment-verification-guide.md)
- [Enforcement research](references/enforcement-research.md)
- [Skill update feedback loop](references/skill-update-feedback.md)
- [AGENTS.md template](references/agents-md-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, scripts, and configuration templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces repository guardrail instructions and local setup commands for agent-assisted development workflows.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
