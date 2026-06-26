## Description: <br>
Place manual trades on Polymarket by telling your agent what to bet on, with support for FAK instant-fill orders, GTC limit orders, Simmer market IDs, Polymarket URLs, import, and price discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DjDyll](https://clawhub.ai/user/DjDyll) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to place or cancel manual Polymarket orders after resolving a market by Simmer market ID or Polymarket URL. It supports dry-run previews, FAK market-style orders, GTC limit orders, and basic order cancellation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place or cancel live Polymarket orders with wallet authority. <br>
Mitigation: Use only with explicit human review of market, side, amount, price, order type, venue, and cancellation intent before running non-dry-run commands. <br>
Risk: Wallet credentials and API keys are required for execution. <br>
Mitigation: Use a dedicated low-balance wallet and restrict access to SIMMER_API_KEY and WALLET_PRIVATE_KEY. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/DjDyll/polymarket-manual-trade) <br>
- [Publisher Profile](https://clawhub.ai/user/DjDyll) <br>
- [Simmer Markets](https://www.simmer.markets/) <br>
- [Polymarket](https://polymarket.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text with JSON status output and Markdown usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY, WALLET_PRIVATE_KEY, and simmer-sdk; dry-run mode previews an order without placing it.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
