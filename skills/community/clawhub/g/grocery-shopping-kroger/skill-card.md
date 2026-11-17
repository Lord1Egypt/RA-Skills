## Description:

Search Kroger-family grocery products, find stores, inspect nutrition and allergen details, and add selected items to a connected Kroger cart through AgentPMT-hosted remote tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to find nearby Kroger-family stores, search products with dietary and nutrition filters, compare availability and pricing, and add selected items to a connected Kroger cart.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can share approximate location and shopping intent with AgentPMT and Kroger services.

Mitigation: Install only when that data sharing is acceptable for the intended user and workflow.

Risk: The skill can modify a connected Kroger cart.

Mitigation: Require user confirmation before any cart-changing action is executed.

Risk: The skill includes unpinned npx setup examples.

Mitigation: Prefer the ClawHub/OpenClaw install route or pinned, verified setup commands.

## Reference(s):

- [Grocery Shopping Kroger ClawHub Page](https://clawhub.ai/agentpmt/skills/grocery-shopping-kroger)
- [AgentPMT Marketplace Product](https://www.agentpmt.com/marketplace/grocery-shopping-kroger)
- [Action Schema](artifact/schema.md)
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [What AgentPMT Is](https://clawhub.ai/agentpmt/what-is-agentpmt)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration instructions, Shell commands]

**Output Format:** [Markdown instructions with JSON request examples and schema references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote calls return JSON product, store, detail, and cart-operation results.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
