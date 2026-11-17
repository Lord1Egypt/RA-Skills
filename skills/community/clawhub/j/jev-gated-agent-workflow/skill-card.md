## Description:

Guides developers in placing a default-deny JEV decision gate before costly or privacy-sensitive agent tools, with fixed allowlists and minimal retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jes614753-sketch](https://clawhub.ai/user/jes614753-sketch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design or review a constrained routing gate before an agent reads sensitive data or invokes costly tools. It guides allowlist validation, short-lived permits, and narrowly scoped retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An incorrect route or stale permit could authorize the wrong protected action.

Mitigation: Use a narrow local allowlist, default-deny checks, and short-lived one-time permits bound to the request, tool, and target.

Risk: Credentials or private identifiers could be exposed in the package or diagnostics.

Mitigation: Keep keys, real IDs, logs, and local policy files outside the skill package; redact diagnostics.

Risk: A permitted write could have irreversible or high-impact effects.

Mitigation: Require explicit confirmation whenever local policy calls for it before executing the write.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/jes614753-sketch/skills/jev-gated-agent-workflow)
- [Implementation checklist](references/implementation-checklist.md)
- [Router contract](references/router-contract.md)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, Code]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Design guidance only; the host must validate routes and permits before executing protected tools.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
