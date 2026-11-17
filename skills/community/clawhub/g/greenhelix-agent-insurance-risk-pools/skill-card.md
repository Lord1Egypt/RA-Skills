## Description:

A markdown playbook for designing agent-native insurance infrastructure, including risk pools, liability bonds, automated claims processing, regulatory compliance, disputes, trust verification, ledger reconciliation, and SLA enforcement with detailed code examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators of commercial agent systems use this guide to design insurance-style risk pools, underwriting, policy lifecycle, claims adjudication, reinsurance, and compliance workflows for autonomous commerce agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples can involve live authenticated insurance and finance workflows that may send sensitive policy, identity, wallet, or claims data.

Mitigation: Use sandbox credentials and synthetic data, and do not paste real API tokens or regulated claims, identity, wallet, or policy data without approval.

Risk: Webhook examples can create persistent outbound integrations for insurance events.

Mitigation: Register webhooks only to approved HTTPS endpoints with signing, ownership verification, monitoring, and a revocation plan.

Risk: Misconfigured hosts, amounts, identifiers, or policy parameters could affect live insurance or finance workflows.

Mitigation: Lock the API host to trusted GreenHelix domains and validate all amounts, identifiers, and policy parameters before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mirni/skills/greenhelix-agent-insurance-risk-pools)
- [GreenHelix Sandbox](https://sandbox.greenhelix.net)
- [GreenHelix A2A Commerce API](https://api.greenhelix.net/v1)
- [Agent Production Hardening Guide](https://clawhub.ai/skills/greenhelix-agent-production-hardening)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guide with inline Python code examples and API request patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executing guide; examples should be reviewed before use with credentials, regulated data, or live financial workflows.]

## Skill Version(s):

1.3.1 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
