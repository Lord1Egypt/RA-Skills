## Description:

Multi-agent orchestration patterns for production deployments, including sub-agent quality-control workflows, model staggering, cross-validation, fallback chains, task routing, ACPX configuration, and cost optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design, configure, and operate multi-agent workflows that route tasks across models, add review loops, set fallback behavior, and control orchestration cost.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Orchestration examples could be mistaken for a security boundary.

Mitigation: Treat the skill as guidance and perform deployment review before relying on agent routing or review loops for control decisions.

Risk: Sub-agents with broad permissions could make unintended project changes.

Mitigation: Scope sub-agent permissions to the project and require confirmation before destructive actions.

Risk: Provider API keys could be exposed beyond the intended orchestration runtime.

Mitigation: Limit API-key availability to the intended server or agent runtime and avoid passing credentials to unnecessary sub-agents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samledger67-dotcom/skills/pl-agent-orchestration)
- [ClawHub publisher profile](https://clawhub.ai/user/samledger67-dotcom)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python, YAML, JSON, shell, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance-only skill; no bundled executable payload.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
