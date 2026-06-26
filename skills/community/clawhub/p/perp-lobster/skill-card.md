## Description: <br>
Trade on Hyperliquid DEX with simple commands. Place market/limit orders on perps, or run automated bots (market making, grid trading) with a web dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ThisNewMark](https://clawhub.ai/user/ThisNewMark) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users use this skill to operate Hyperliquid perpetual trading workflows from an agent, including one-time market or limit orders and continuous market-making or grid-trading bots. It is intended for users who can review trading commands, manage local credentials, and accept leveraged crypto trading risk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place leveraged crypto trades and run trading bots that may lose funds. <br>
Mitigation: Use only dedicated limited subaccounts or trading keys, start with minimum-size test trades, and require explicit user confirmation before each trade, test trade, fee approval, or bot start. <br>
Risk: Setup runs code from an external repository and local scripts before trading. <br>
Mitigation: Review and pin the repository code before setup, show setup scripts before first execution, and avoid running unreviewed updates. <br>
Risk: Wallet private keys and trading credentials are needed locally. <br>
Mitigation: Never paste private keys into chat, never display or read credential files in the agent transcript, and keep credentials in the local environment file only. <br>
Risk: Automated bots can continue trading in the background during market or configuration errors. <br>
Mitigation: Verify that stop and emergency-stop commands work before running bots, monitor logs after startup, and keep exposure limits conservative. <br>


## Reference(s): <br>
- [Perp Lobster GitHub homepage](https://github.com/ThisNewMark/perplobster) <br>
- [ClawHub skill page](https://clawhub.ai/ThisNewMark/perp-lobster) <br>
- [Config Parameter Reference](references/CONFIG_REFERENCE.md) <br>
- [Strategy Selection Guide](references/STRATEGIES.md) <br>
- [Troubleshooting Guide](references/TROUBLESHOOTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or execute local commands for setup, fee approval, trading, bot control, dashboard launch, and emergency stop when the user confirms the relevant action.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
