## Description:

MOSES Governance Single provides single-agent governance controls for agent mode, posture, role, and audit logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunrisesillneversee](https://clawhub.ai/user/sunrisesillneversee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to apply advisory governance modes, transaction posture controls, role awareness, and tamper-evident audit logging to a single OpenClaw agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist governance settings and audit records across sessions.

Mitigation: Review or clear ~/.openclaw/governance and ~/.openclaw/audits/moses when switching projects, trust contexts, or operators.

Risk: The governance controls are advisory and should not be treated as a hard safety boundary.

Mitigation: Use human approval for sensitive actions and avoid unrestricted or offense posture for high-risk work.

Risk: Audit entries may capture action details that should not include secrets or hidden reasoning.

Mitigation: Keep secrets and private reasoning out of audit detail fields and review recent ledger entries before sharing logs.

Risk: MOSES_OPERATOR_SECRET is an optional signing key for audit attestation.

Mitigation: Set it only in trusted local environments and never paste it into chat, prompts, logs, or shared artifacts.

## Reference(s):

- [MOSES Governance Modes Reference](references/modes.md)
- [MOSES Posture Controls Reference](references/postures.md)
- [MOSES Role Hierarchy Reference](references/roles.md)
- [Zenodo record](https://zenodo.org/records/18792459)
- [MOSES project site](https://mos2es.io)
- [ClawHub skill page](https://clawhub.ai/sunrisesillneversee/skills/moses-governance-single)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands and JSON-backed state and audit files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can persist governance state and audit ledger files under ~/.openclaw when its commands are run.]

## Skill Version(s):

1.0.4 (source: server release evidence; artifact metadata openclaw version 0.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
