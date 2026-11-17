## Description:

LYGO Sovereign Workflow Orchestrator helps agents run YAML-defined sovereign workflows with P0 input gating, P1 memory recall, optional P3 consensus, P5 run identity, dry-run defaults, and explicit consent gates for sensitive actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to validate and run local YAML workflow packs with an audit trail, memory recall, and consent-gated orchestration steps on infrastructure they control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install and self-check steps rely on mutable or external code.

Mitigation: Install and run only in a development environment you control, and pin or review clawhub and sandcastle-ai before use.

Risk: Untrusted workflow YAML may execute unsafe orchestration paths or include sensitive prompts.

Mitigation: Validate untrusted workflow YAML before running it, keep dry-run mode for initial use, and avoid committing workflow files that contain secrets.

Risk: Sandbox, kernel, and publishing actions can have broader system or release impact.

Mitigation: Require explicit user consent before enabling Docker or Podman sandbox actions, kernel planting, GitHub pushes, ClawHub publishing, or similar publishing steps.

## Reference(s):

- [AGENT_CONTRACT.md](artifact/references/AGENT_CONTRACT.md)
- [SECURITY.md](artifact/references/SECURITY.md)
- [ClawHub skill page](https://clawhub.ai/deepseekoracle/skills/lygo-sandcastle)
- [lygo-protocol-stack repository URL from metadata](https://github.com/DeepSeekOracle/lygo-protocol-stack)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline shell commands and file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for local-first workflow validation and orchestration, with dry-run defaults and explicit consent for publishing, sandbox, kernel, or upstream actions.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
