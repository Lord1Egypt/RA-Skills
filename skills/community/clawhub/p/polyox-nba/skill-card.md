## Description: <br>
Query the PolyOx API for NBA data, Polymarket predictions, and AI matchup analysis, with paid analysis handled through x402 payments in USDC on Base Sepolia. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jambocoder159](https://clawhub.ai/user/jambocoder159) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agents use this skill to query NBA teams, games, stats, injury reports, Polymarket market data, and matchup context from the PolyOx API. Agents can also follow the documented x402 payment flow to request paid AI matchup analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid analysis calls require wallet-mediated x402 signing and may spend USDC on Base Sepolia. <br>
Mitigation: Use the managed Coinbase Agentic Wallet flow or a dedicated low-balance Base Sepolia wallet, and verify the host, token, network, recipient, and maximum amount before signing. <br>
Risk: Private-key based integrations can expose wallet credentials if environment variables are logged or shared. <br>
Mitigation: Do not expose or log EVM_PRIVATE_KEY; prefer managed wallet tooling when private key handling is not required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jambocoder159/polyox-nba) <br>
- [PolyOx API base URL](https://api-hoobs.polyox.io) <br>
- [x402 protocol documentation](https://docs.x402.org) <br>
- [Coinbase Agentic Wallet quickstart](https://docs.cdp.coinbase.com/agentic-wallet/quickstart) <br>
- [Coinbase Agentic Wallet skills overview](https://docs.cdp.coinbase.com/agentic-wallet/skills/overview) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with curl commands, JSON examples, and TypeScript code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Free API calls return JSON; the paid analysis endpoint requires wallet-mediated x402 payment handling.] <br>

## Skill Version(s): <br>
0.2.0 (source: server-resolved release metadata; frontmatter lists 0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
