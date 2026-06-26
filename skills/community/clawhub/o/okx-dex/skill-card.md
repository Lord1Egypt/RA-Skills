## Description: <br>
OKX DEX aggregator (v6). Get swap quotes, swap/approve tx data, tokens, and chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ricky321u](https://clawhub.ai/user/ricky321u) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to work with the OKX DEX API for chain discovery, token lists, swap quotes, approval transaction data, and swap transaction data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses OKX API credentials for DEX quote and transaction-data requests. <br>
Mitigation: Keep OKX secrets out of chat and logs, use least-privilege credentials, and rotate credentials if exposure is suspected. <br>
Risk: Generated swap or approval transaction data may be unsafe if token addresses, chain, spender, amount, route, price impact, or slippage are wrong. <br>
Mitigation: Independently verify transaction details in the wallet and require explicit user confirmation before signing any approval or swap. <br>


## Reference(s): <br>
- [OKX DEX API Reference (v6)](https://web3.okx.com/build/dev-docs/wallet-api/dex-api-reference) <br>
- [ClawHub okx-dex Skill Page](https://clawhub.ai/ricky321u/okx-dex) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with bash and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces API request examples and transaction-data guidance; users must verify generated approval and swap details before signing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact _meta.json lists 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
