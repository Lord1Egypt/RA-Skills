## Description: <br>
Trade on Phemex for USDT-M futures, Coin-M futures, and spot markets by checking market data, managing balances and positions, placing or canceling orders, setting leverage, and transferring funds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bubble501](https://clawhub.ai/user/bubble501) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Phemex trading workflows through the phemex-cli tool, including market-data lookup, account review, order management, leverage changes, and spot/futures fund transfers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place or cancel orders, change leverage, inspect positions, and transfer funds with Phemex API credentials. <br>
Mitigation: Use a dedicated key with minimum permissions, disable withdrawals, prefer testnet or read-only access first, and require explicit approval before each order, cancellation, leverage change, position-mode change, or transfer. <br>
Risk: Persistent credentials in ~/.phemexrc can expose high-impact exchange access if the file is mishandled. <br>
Mitigation: Protect or avoid ~/.phemexrc, use environment variables or a secret store when appropriate, and restrict file access to the local user. <br>
Risk: Installing and running the npm CLI package gives local code access to trading credentials and exchange actions. <br>
Mitigation: Pin and verify the package version before installation, review command output before acting, and keep manual approval in the loop for trading operations. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/bubble501/phemex-trade) <br>
- [Project homepage from skill metadata](https://github.com/betta2moon/phemex-trade-mcp) <br>
- [Phemex](https://phemex.com) <br>
- [Phemex production API endpoint](https://api.phemex.com) <br>
- [Phemex testnet API endpoint](https://testnet-api.phemex.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses phemex-cli with PHEMEX_API_KEY and PHEMEX_API_SECRET, optionally stored in ~/.phemexrc.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
