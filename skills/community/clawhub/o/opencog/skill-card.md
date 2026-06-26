## Description: <br>
Trade on prediction markets. Create a local wallet, list markets, check prices, buy and sell outcome shares. Coming soon: create and fund markets directly from this skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xAstraea](https://clawhub.ai/user/0xAstraea) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users use this skill to browse Precog prediction markets, inspect probabilities and positions, quote trades, and buy or sell outcome shares through a local wallet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A plaintext private key in ~/.openclaw/.env can control funds held by the local wallet. <br>
Mitigation: Use a throwaway wallet, prefer Sepolia/testnet, avoid storing valuable mainnet keys, and set the key file to owner-only permissions. <br>
Risk: Mainnet commands can execute real prediction-market trades. <br>
Mitigation: Confirm the network, contract, market, outcome, shares, and final max/min trade bounds before any transaction; quote trades first and require explicit user confirmation. <br>
Risk: The security evidence flags broader contract-control surfaces than the trading instructions disclose. <br>
Mitigation: Review the wallet-handling and contract-interaction code before installation or use, and verify the repository source before running scripts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/0xAstraea/opencog) <br>
- [Skill Homepage](https://github.com/openclaw/precog-skill) <br>
- [Precog Documentation](https://learn.precog.markets) <br>
- [Precog App](https://core.precog.markets) <br>
- [MATE Token](https://matetoken.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands and verbatim command output blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation before executing trading transactions.] <br>

## Skill Version(s): <br>
0.1.4 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
