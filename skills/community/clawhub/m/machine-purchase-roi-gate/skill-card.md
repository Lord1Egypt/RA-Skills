## Description:

Machine Purchase ROI Gate: Decide whether an agent should buy one machine service call before any payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this workflow as a pre-payment decision gate for a single machine-service purchase. It validates price, fee, failure probability, retry cost, output value, and budget assumptions before returning a buy, defer, or reject decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned setup commands or installer routes could create supply-chain exposure.

Mitigation: Prefer the OpenClaw or ClawHub route, or pin and verify any skills.sh or npx installer and AgentPMT skill source before installation.

Risk: The workflow could be misused to proceed from economic approval into payment authority.

Mitigation: Use the skill only as a pre-payment decision gate and do not grant it wallet, signing, payment, broadcast, or broad filesystem privileges.

Risk: Stale endpoints, schemas, setup steps, or examples could affect the purchase decision workflow.

Mitigation: Reinstall or refresh the skill from ClawHub or skills.sh when freshness guidance indicates the artifact is outdated.

Risk: Incorrect or incomplete purchase assumptions could produce a misleading buy, defer, or reject decision.

Mitigation: Require explicit bounded assumptions and stop on malformed JSON, missing values, non-finite numbers, negative money values, invalid failure probability, zero outlay, or excessive capital recovery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/machine-purchase-roi-gate)
- [AgentPMT workflow page](https://www.agentpmt.com/agent-workflow-skills/machine-purchase-roi-gate)
- [AgentPMT workflows](https://www.agentpmt.com/agent-workflow-skills)
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [Data Format Validation](https://clawhub.ai/agentpmt/data-format-validation)
- [Complex Mathematics Engine](https://clawhub.ai/agentpmt/complex-mathematics-engine)
- [Data Format Validation marketplace](https://www.agentpmt.com/marketplace/data-format-validation)
- [Complex Mathematics Engine marketplace](https://www.agentpmt.com/marketplace/complex-mathematics-engine)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON snippets and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a compact machine-readable purchase decision with expected net value, finite financial ROI, total outlay, capital at risk, maximum rational service price, and binding reason.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
