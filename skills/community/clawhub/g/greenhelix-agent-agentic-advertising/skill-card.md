## Description:

Build autonomous ad-buying agents with publisher discovery, trust verification, escrow-based ad spend, real-time ROAS tracking, compliance guardrails, and fleet-scale campaign management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and advertising engineers use this guide to design autonomous media-buying agents that can discover publishers, manage escrow-backed budgets, track campaign performance, and apply compliance guardrails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples can target production GreenHelix APIs and create real ad-spend commitments.

Mitigation: Use explicitly sandboxed endpoints, dry-run behavior, spend limits, and human approvals before any payment or escrow operation.

Risk: Credentials and funded wallets could be exposed or misused if tutorial examples are run in a production environment.

Mitigation: Store AGENT_SIGNING_KEY securely and avoid using real credentials, funded wallets, or production campaign data until the workflow has been reviewed.

Risk: Automated campaign workflows may continue changing remote state after critical SLA or compliance failures.

Mitigation: Prove that critical SLA violations halt or pause real remote state before enabling autonomous execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirni/skills/greenhelix-agent-agentic-advertising)
- [GreenHelix sandbox](https://sandbox.greenhelix.net)
- [GreenHelix API endpoint](https://api.greenhelix.net/v1)
- [GreenHelix production hardening guide](https://clawhub.ai/skills/greenhelix-agent-production-hardening)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guide with Python examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executing tutorial content; examples reference AGENT_SIGNING_KEY and GreenHelix API endpoints.]

## Skill Version(s):

1.3.1 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
