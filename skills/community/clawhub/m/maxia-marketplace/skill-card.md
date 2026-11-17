## Description:

MAXIA Marketplace helps agents discover and call MAXIA services for AI-service marketplace tasks, crypto swaps and prices, DeFi yields, GPU rental, tokenized stocks, wallet analysis, sentiment, scraping, and image generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[majorelalexis-stack](https://clawhub.ai/user/majorelalexis-stack)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to discover MAXIA services, retrieve market and DeFi information, rent GPUs, and prepare calls to MAXIA marketplace and financial-operation APIs. Paid actions require user-managed API credentials and manual confirmation of payment details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents toward real financial actions through broad remote APIs.

Mitigation: Require manual confirmation for every paid action, trade, swap, stock transaction, or GPU rental before execution.

Risk: Payment requests may involve incorrect treasury address, chain, amount, or fee details.

Mitigation: Verify treasury address, blockchain, amount, fees, and transaction signature independently before submitting payment_tx.

Risk: A remote MCP manifest or API surface can change after installation.

Mitigation: Use tool allowlists, block unexpected schema changes, and prefer sandbox mode before enabling production operations.

Risk: Shared credentials or wallets increase blast radius for financial operations.

Mitigation: Use a dedicated wallet and dedicated MAXIA_API_KEY with limited funds and scope.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/majorelalexis-stack/skills/maxia-marketplace)
- [Publisher Profile](https://clawhub.ai/user/majorelalexis-stack)
- [MAXIA Homepage](https://maxiaworld.app)
- [MAXIA API Documentation](https://maxiaworld.app/api/public/docs)
- [MAXIA MCP Manifest](https://maxiaworld.app/mcp/manifest)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown with inline shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access to https://maxiaworld.app and a MAXIA_API_KEY for authenticated operations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
