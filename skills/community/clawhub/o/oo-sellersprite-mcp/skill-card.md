## Description:

SellerSprite MCP (open.sellersprite.com). Use this skill for ANY SellerSprite MCP request — reading, creating, and updating data. Whenever a task involves SellerSprite MCP, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, brand owners, and developers can use the skill to research Amazon products, keywords, markets, reviews, trends, and trademarks through SellerSprite MCP. It guides the agent to inspect action schemas before making requests and to obtain approval before write or destructive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup may run an unverified installer and make lasting changes to other agents' skill directories.

Mitigation: Review the setup and install a verified oo release yourself; explicitly approve installation changes. Set OO_SKILLS_SYNC_DISABLED=1 before running oo if you do not want other agents' skill directories changed.

Risk: Write or destructive connector actions can change SellerSprite MCP state.

Mitigation: Keep write approvals enabled and confirm the exact payload and effect before running a write; explicitly approve the target before a destructive action.

## Reference(s):

- [SellerSprite MCP](https://open.sellersprite.com/mcp)
- [SellerSprite MCP API documentation](https://open.sellersprite.com/mcp/16)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Analysis, Text]

**Output Format:** [JSON responses with concise research summaries as text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results and available fields depend on the selected action and its live schema.]

## Skill Version(s):

1.0.5 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
