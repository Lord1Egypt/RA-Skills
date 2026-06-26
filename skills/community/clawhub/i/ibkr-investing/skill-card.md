## Description: <br>
Invest on Interactive Brokers (stocks/ETFs) via IB Gateway with the same human-in-the-loop confirmation gate as okx-trading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vm-development](https://clawhub.ai/user/vm-development) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to inspect Interactive Brokers account state, retrieve market data, prepare stock or ETF trade proposals, and execute only proposals that receive explicit chat confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access brokerage account data and prepare orders through IB Gateway. <br>
Mitigation: Use paper mode until tested, protect IBKR Gateway credentials and local ~/.aeon/ibkr records, and grant access only where brokerage automation is intended. <br>
Risk: A confirmed proposal can place a real stock or ETF order when live mode is enabled. <br>
Mitigation: Require the proposal, explicit YES confirmation, confirmation token, allow-list, per-trade cap, and daily cap before execution. <br>
Risk: Scheduled DCA or drawdown workflows could create trade recommendations without a user present. <br>
Mitigation: Scheduled workflows are limited to read-only or proposal-generation behavior; execution still requires the user to review the proposal and confirm it in chat. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/vm-development/ibkr-investing) <br>
- [Publisher profile](https://clawhub.ai/user/vm-development) <br>
- [amuletxheart/ibkr-openclaw](https://clawhub.ai/amuletxheart/ibkr-openclaw) <br>
- [IB Gateway Docker](https://github.com/gnzsnz/ib-gateway-docker) <br>
- [ib_async](https://github.com/ib-api-reloaded/ib_async) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON or text command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create local pending-trade, audit, snapshot, notional-log, and strategy-state files under the user's aeon IBKR directory.] <br>

## Skill Version(s): <br>
0.1.1 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
