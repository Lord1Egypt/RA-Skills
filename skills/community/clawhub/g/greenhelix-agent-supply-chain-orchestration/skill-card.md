## Description:

Guides agents and developers through building multi-agent supply chain orchestration workflows for supplier discovery, SLA monitoring, disruption rerouting, demand aggregation, and cross-border compliance using GreenHelix examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, procurement automation teams, and agent builders use this guide to plan and implement multi-agent supply chain networks that coordinate supplier discovery, monitoring, rerouting, demand planning, compliance checks, and escrow-protected transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copying the guide's examples into production can automate supplier changes and escrow or payment actions without sufficient approval controls.

Mitigation: Keep workflows in sandbox mode until explicit approvals, spend limits, compliance gates, rollback paths, and dispute procedures are added.

Risk: Using broad production credentials can increase the impact of erroneous supplier or payment actions.

Mitigation: Use least-privilege API keys, separate sandbox and production credentials, and audit every financial or supplier-routing action.

Risk: Automated rerouting can rely on incomplete delivery or compliance evidence.

Mitigation: Require trusted delivery evidence, idempotency controls, and audit logging before escrow, payment, or supplier migration steps proceed.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/mirni/skills/greenhelix-agent-supply-chain-orchestration)
- [GreenHelix sandbox](https://sandbox.greenhelix.net)
- [GreenHelix API](https://api.greenhelix.net/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guide with Python code examples and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executing guide content; examples reference GREENHELIX_API_KEY for full API access.]

## Skill Version(s):

1.3.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
