## Description: <br>
AI-native resale marketplace. Browse, list, buy, sell, negotiate, message, and manage orders. 49 MCP tools. 3% seller fee, 3.5% buyer fee ($0.99 min). No listing fees. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[douglashardman](https://clawhub.ai/user/douglashardman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to browse, list, buy, sell, negotiate, message, and manage orders on the Kabuzz resale marketplace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate marketplace actions that spend real money or affect shipping and payment workflows. <br>
Mitigation: Use low spending limits and require human approval for purchases, offer acceptance, shipping-label purchases, and payment-method changes. <br>
Risk: Purchase retries or price changes could cause unwanted transactions. <br>
Mitigation: Always use maxPrice and idempotencyKey for purchases, and re-check listings when price or sold-state errors occur. <br>
Risk: The required API key grants access to live Kabuzz account capabilities. <br>
Mitigation: Protect KABUZZ_API_KEY, scope operational access through account controls, and review or pin the npm MCP package before live use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/douglashardman/kabuzz-marketplace) <br>
- [Kabuzz Marketplace](https://kabuzz.com) <br>
- [Kabuzz API Docs](https://kabuzz.com/docs) <br>
- [Kabuzz MCP Server npm Package](https://www.npmjs.com/package/@kabuzz/mcp-server) <br>
- [Agent Skill File](https://kabuzz.com/agent-skill.md) <br>
- [OpenAPI Spec](https://kabuzz.com/docs-json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, API calls, Markdown, JSON] <br>
**Output Format:** [Markdown guidance with JSON configuration snippets and tool/API call names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npx and KABUZZ_API_KEY; marketplace actions may transact with live payment and shipping workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
