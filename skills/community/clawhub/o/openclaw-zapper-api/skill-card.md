## Description: <br>
Query DeFi portfolios, token holdings, NFTs, transactions, and prices via the Zapper API across 50+ chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zivhm](https://clawhub.ai/user/zivhm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to retrieve wallet portfolio, token, DeFi, NFT, transaction, claimable reward, and token price data through Zapper's API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried wallet addresses and lookup activity are sent to Zapper. <br>
Mitigation: Query only the intended address or wallet label, and avoid all-wallet lookups unless that is the intended action. <br>
Risk: The Zapper API key and configured wallet list can expose account access or private portfolio context if shared. <br>
Mitigation: Use a dedicated Zapper API key, keep ~/.config/zapper/addresses.json private, and do not commit API keys or wallet configuration. <br>


## Reference(s): <br>
- [Zapper GraphQL API Reference](references/API.md) <br>
- [Zapper API Documentation](https://build.zapper.xyz/docs/api/) <br>
- [Zapper Developers](https://zapper.xyz/developers) <br>
- [Zapper](https://zapper.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Plain text CLI summaries or raw JSON, with Markdown documentation and bash examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports optional limits, short totals, per-wallet breakdowns, and 24-hour price-change views.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
