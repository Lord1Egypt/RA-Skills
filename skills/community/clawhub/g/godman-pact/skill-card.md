## Description:

PACT - Protocol for Agent Constitutional Trust is a five-chamber agent-to-agent trust and negotiation protocol that handles identity verification, intent analysis, constitutional negotiation, capability-locked session tokens, and audit trails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skingem1](https://clawhub.ai/user/skingem1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent-system operators use this skill to establish trust between agents from different systems before data exchange, payment, or secure sessions. It guides identity verification, intent analysis, constitutional negotiation, session ceilings, and capability-locked token creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A separate implementation of the referenced SDK may initiate signatures, payments, or on-chain attestations with lasting external effects.

Mitigation: Review and test the SDK implementation, and require explicit approval before signatures, payments, or attestations are executed.

Risk: Trust negotiation could be misused as a reason to bypass higher-priority safety constraints.

Mitigation: Enforce non-negotiable safety constraints outside the PACT session and treat them as overriding any negotiated session terms.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown guidance with TypeScript example code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Markdown-only skill text; no executable files are included in the artifact.]

## Skill Version(s):

0.3.0 (source: SKILL.md frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
