## Description: <br>
Guides users through Interactive Brokers CLI operations, including IB Gateway or TWS setup, ibkr-cli installation, account monitoring, market data retrieval, and stock order workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fatwang2](https://clawhub.ai/user/fatwang2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to set up ibkr-cli, connect to IB Gateway or TWS, retrieve account and market information, and prepare brokerage trading commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide actions against live Interactive Brokers accounts and the security summary notes a live-profile preference before explicit live trading selection. <br>
Mitigation: Prefer paper profiles until the user explicitly confirms live-account use, and require confirmation of the selected profile before any live command. <br>
Risk: Submitted or cancelled brokerage orders can affect real positions if symbol, quantity, order type, price, account, or profile is wrong. <br>
Mitigation: Preview every order first and verify symbol, quantity, order type, price, account, and profile before submitting or cancelling anything. <br>


## Reference(s): <br>
- [Setup and Connectivity](references/setup.md) <br>
- [Trading and Order Management](references/trading.md) <br>
- [Market Data, News, Options, Scanner, and Fundamentals](references/market-data.md) <br>
- [Account Monitoring and Utilities](references/account.md) <br>
- [IB Gateway download](https://www.interactivebrokers.com/en/trading/ibgateway-stable.php) <br>
- [Trader Workstation download](https://www.interactivebrokers.com/en/trading/tws-updateless-latest.php) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Text] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON command-output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include order preview, submission, account, market data, and troubleshooting commands for ibkr-cli.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
