## Description: <br>
MAXIA Marketplace lets agents discover, buy, and sell AI services with USDC and access crypto swaps, GPU rentals, DeFi yield tracking, tokenized stocks, wallet analysis, and sentiment tools across supported blockchains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[majorelalexis-stack](https://clawhub.ai/user/majorelalexis-stack) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and agents use this skill to connect to MAXIA marketplace APIs for AI service discovery, paid service execution, crypto and tokenized-stock operations, DeFi yield tracking, GPU rental, wallet analysis, sentiment tools, scraping, and image generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through paid, financial, and account-changing MAXIA actions. <br>
Mitigation: Use a dedicated low-balance wallet and API key, and require manual confirmation before every paid or mutating request. <br>
Risk: Prompts, scraping requests, wallet details, or transaction data may expose sensitive information to the external MAXIA service. <br>
Mitigation: Avoid sending secrets or sensitive data through prompts, scraping requests, or marketplace service executions. <br>
Risk: Marketplace, crypto, DeFi, GPU rental, and tokenized-stock results may affect real financial decisions. <br>
Mitigation: Verify transaction details, pricing, service identity, and payment requirements independently before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/majorelalexis-stack/maxia-marketplace) <br>
- [MAXIA homepage](https://maxiaworld.app) <br>
- [MAXIA public API docs](https://maxiaworld.app/api/public/docs) <br>
- [MAXIA MCP manifest](https://maxiaworld.app/mcp/manifest) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with endpoint descriptions, tables, and inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access to https://maxiaworld.app and a MAXIA_API_KEY for authenticated operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
