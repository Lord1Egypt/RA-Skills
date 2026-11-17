## Description:

Build automated contract lifecycle management for AI agents with machine-readable SLAs, escrow-backed execution, real-time obligation tracking, automated penalty enforcement, renewal workflows, and detailed Python examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this guide to design agent contract lifecycle workflows with machine-readable SLAs, escrow-backed execution, monitoring, penalties, renewal, termination, and audit trails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Production-style examples can automate escrow funding, penalty deductions, reputation changes, and contract termination without enough safeguards if copied directly.

Mitigation: Treat the guide as illustrative, require explicit approval thresholds for fund movement and termination, and test with sandbox credentials before any live use.

Risk: Contract automation can fund escrow or enforce penalties before both parties have clearly accepted the same agreement state.

Mitigation: Require bilateral signature verification before escrow funding and keep an auditable record of the signed contract fingerprint.

Risk: Repeated breach processing or unsafe API routing could duplicate enforcement actions or expose bearer tokens.

Mitigation: Add idempotency and breach deduplication, and validate API destinations before sending bearer tokens.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/mirni/skills/greenhelix-agent-contract-lifecycle)
- [GreenHelix sandbox](https://sandbox.greenhelix.net)
- [GreenHelix API endpoint](https://api.greenhelix.net/v1)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guide with Python and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executing guide; examples reference GreenHelix sandbox and API workflows.]

## Skill Version(s):

1.3.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
