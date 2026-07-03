## Description: <br>
Grocery Shopping Kroger helps agents find nearby Kroger-family stores, search products with dietary and nutrition filters, retrieve product details, and add selected items to a connected Kroger cart. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents use this skill to support grocery shopping workflows for Kroger-family stores, including store lookup, product search, dietary filtering, product detail review, and cart updates for connected Kroger accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use location-derived zip code data for store lookup. <br>
Mitigation: Keep tool inputs scoped to the grocery task and review any location-dependent store selection before use. <br>
Risk: The skill can change a live Kroger cart when a connected Kroger account is available. <br>
Mitigation: Before cart updates, show the exact items, quantities, store, and account action, then proceed only after user confirmation. <br>
Risk: Security evidence notes unclear confirmation boundaries for cart-changing actions. <br>
Mitigation: Treat add_to_cart as a confirmation-gated action and preserve request parameters when retrying only after fixing schema, authentication, or payment errors. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/grocery-shopping-kroger) <br>
- [AgentPMT marketplace product page](https://www.agentpmt.com/marketplace/grocery-shopping-kroger) <br>
- [AgentPMT MCP server](https://api.agentpmt.com/mcp/) <br>
- [AgentPMT REST invoke endpoint](https://api.agentpmt.com/products/purchase) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with JSON examples and tool-call schemas] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces action guidance and structured request examples for find_stores, search_products, get_product_details, and add_to_cart.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
