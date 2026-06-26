## Description: <br>
Build Instacart recipe pages, shopping lists, and retailer lookups with MCP, REST, secure auth, and launch-ready integration rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent builders use this skill to create Instacart recipe pages, shopping-list pages, retailer lookups, and MCP handoffs while keeping API key handling, environment selection, and launch boundaries explicit. <br>

### Deployment Geography for Use: <br>
United States and Canada <br>

## Known Risks and Mitigations: <br>
Risk: Instacart API keys could be exposed if pasted into chat, markdown, screenshots, repository files, or local notes. <br>
Mitigation: Keep keys in environment variables or a secret manager, and store only non-secret operating context in ~/instacart/. <br>
Risk: Recipe, grocery, postal-code, retailer, and MCP payload data is sent to Instacart services when the documented REST or MCP workflows are used. <br>
Mitigation: Use the skill only for intended Instacart workflows, confirm the development or production endpoint before sending traffic, and avoid undeclared external destinations. <br>
Risk: Using production keys or public launch messaging before Instacart approval can result in nonfunctional keys or launch rejection. <br>
Mitigation: Complete development testing first, verify production approval status in the Instacart dashboard, and review messaging or trademark requirements before launch. <br>
Risk: Weak item normalization or routing to the wrong Instacart surface can produce poor matches, validation errors, or incorrect fulfillment expectations. <br>
Mitigation: Choose MCP, Developer Platform REST, or Connect before implementation; keep item names generic, put brand and health intent in filters, use supported units, and do not mix product_ids with upcs on the same item. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/instacart) <br>
- [Skill Homepage](https://clawic.com/skills/instacart) <br>
- [Instacart Developer Platform Development REST](https://connect.dev.instacart.tools) <br>
- [Instacart Developer Platform Production REST](https://connect.instacart.com) <br>
- [Instacart Development MCP Server](https://mcp.dev.instacart.tools/mcp) <br>
- [Instacart Production MCP Server](https://mcp.instacart.com/mcp) <br>
- [Instacart Dashboard](https://dashboard.instacart.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API request patterns] <br>
**Output Format:** [Markdown guidance with inline bash, curl, JSON payload, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local operating notes under ~/instacart/; does not store secrets by design.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
