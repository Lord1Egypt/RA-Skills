## Description:

Live NFT market and NFT lending data from GONDI, an NFT marketplace with peer-to-peer lending on Ethereum, Hyperliquid (HyperEVM) and Robinhood Chain. Use when the user asks for a collection's floor price or top bid, one NFT's listing, top bid, last sale or estimated value, the cheapest NFTs for sale, recent sales, floor history, top or trending collections, GONDI's fees against OpenSea, what a wallet's NFTs are worth, how much an NFT can borrow, what buying with a loan costs, a borrower's open loans, loan offers and lending APRs, or the top lenders and their returns. Read-only. It calls the hosted GONDI MCP server at https://api.gondi.xyz/mcp with no API key and no wallet, and never signs or sends a transaction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mishuagopian](https://clawhub.ai/user/mishuagopian)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent for live NFT market, wallet, lending, and borrowing data across GONDI-supported chains. The agent summarizes read-only results to help users understand prices, fees, offers, and loan terms; answers are not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on GONDI's hosted service for market and lending data; the security scan rated it benign with medium confidence and noted partial scanner coverage.

Mitigation: Use the skill only if you trust GONDI to receive the requests, and confirm important figures or terms on GONDI before acting.

## Reference(s):

- [GONDI MCP server documentation](https://docs.gondi.xyz/gondi-v3/mcp-server/)
- [GONDI](https://www.gondi.xyz)
- [GONDI MCP endpoint](https://api.gondi.xyz/mcp)
- [GONDI MCP server repository and issue tracker](https://github.com/gondixyz/mcp)

## Skill Output:

**Output Type(s):** [Text, Analysis]

**Output Format:** [Natural-language answers with linked market data, prices, fees, and loan terms]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live read-only results; USD values may be unavailable when exchange rates are missing.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
