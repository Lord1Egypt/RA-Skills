## Description:

OpenClaw agent safety checklist for action review, risk assessment, rollback planning, and LLM output validation before external effects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kadubon](https://clawhub.ai/user/kadubon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to review proposed external-effect actions before execution by documenting evidence, missing evidence, rollback options, and risk level. It is intended as an advisory guardrail for shell commands, file changes, network requests, credential handling, installs, repository mutations, messages, payments, and other actions with external effects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is advisory and does not itself enforce sandboxing or prove that actions are safe.

Mitigation: Use it together with OpenClaw sandboxing, approvals, allowlists, and tool policy, and require explicit confirmation for sensitive actions.

Risk: Action proposals or PIC reports may contain shell text, network text, route requests, or suggested next steps that are review data rather than approved tasks.

Mitigation: Treat proposals and PIC reports as evidence to inspect, preserve unresolved items, and avoid executing suggested actions until evidence, authority, scope, approval, and rollback checks are adequate.

## Reference(s):

- [PIC Residual Guard on ClawHub](https://clawhub.ai/kadubon/skills/pic-residual-guard)
- [PIC OpenClaw Skill Repository](https://github.com/kadubon/pic-openclaw-skill)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with structured action-review checklists and decision rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces advisory review content only; it does not execute proposed actions or replace sandboxing, approvals, allowlists, or tool policy.]

## Skill Version(s):

0.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
