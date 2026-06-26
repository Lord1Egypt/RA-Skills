## Description: <br>
Audits cryptocurrency addresses and stock tickers from a local portfolio file, then reports estimated current holdings using public, read-only market data APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sahil1005](https://clawhub.ai/user/sahil1005) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and individual portfolio users can run the skill locally to review configured cryptocurrency and stock holdings without giving the agent private keys or exchange credentials. It is intended for read-only portfolio visibility, not trading or custody. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet addresses, stock symbols, and market-data queries may be sent to third-party API providers. <br>
Mitigation: Review portfolio.json before use and only include identifiers you are comfortable sending to services such as Etherscan, CoinGecko, or a configured stock data provider. <br>
Risk: Accidentally storing secrets in the portfolio file could expose sensitive financial access material to local tooling or downstream logs. <br>
Mitigation: Never place private keys, seed phrases, exchange credentials, account passwords, or broad-scope API keys in portfolio.json. <br>
Risk: Market data can be unavailable, rate-limited, delayed, or represented by placeholder values for stock prices. <br>
Mitigation: Treat the output as an informational estimate and verify values with authoritative financial systems before making financial decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sahil1005/local-portfolio-auditor) <br>
- [Publisher profile](https://clawhub.ai/user/sahil1005) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text portfolio summary with stderr warnings for missing API keys or unavailable data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a local JSON portfolio file and may query CoinGecko, Etherscan, or stock market data providers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
