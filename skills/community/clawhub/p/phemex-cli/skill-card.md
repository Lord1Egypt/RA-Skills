## Description: <br>
Trade on Phemex (USDT-M futures, Coin-M futures, Spot) - place orders, manage positions, check balances, stream real-time market data, and query historical data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phemex](https://clawhub.ai/user/phemex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to operate the Phemex CLI for exchange market data, account review, order management, position settings, fund transfers, and real-time market streams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make real financial account changes, including orders, cancellations, leverage changes, position-mode changes, and fund transfers. <br>
Mitigation: Use testnet until verified, require explicit confirmation before every financial action, and review account balance, open orders, and positions before acting. <br>
Risk: Phemex API credentials may be persisted locally or exposed through agent-assisted workflows. <br>
Mitigation: Use a dedicated least-privilege API key, disable withdrawals, restrict by IP when available, and avoid persistent credential files on shared machines. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/phemex/phemex-cli) <br>
- [Phemex website](https://phemex.com) <br>
- [Phemex production API endpoint](https://api.phemex.com) <br>
- [Phemex testnet API endpoint](https://testnet-api.phemex.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses phemex-cli and requires PHEMEX_API_KEY and PHEMEX_API_SECRET for authenticated account, trading, and transfer commands.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
