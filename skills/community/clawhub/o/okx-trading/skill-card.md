## Description: <br>
Trade crypto on OKX with a strict human-in-the-loop confirmation gate for balances, prices, trade proposals, confirmed execution, DCA, grid strategies, snapshots, and PnL digests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vm-development](https://clawhub.ai/user/vm-development) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to inspect OKX account state, prepare crypto trade proposals, execute only explicitly confirmed trades, and manage DCA or grid workflows with configured guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Confirmed grids can continue placing automatic restock orders, including with live OKX credentials. <br>
Mitigation: Use demo mode first, set strict OKX_ALLOWED_SYMBOLS and notional caps, and switch to live keys only after accepting the ongoing-order behavior. <br>
Risk: Stopping or rescaling a grid may delete local tracking even if some exchange cancellations fail. <br>
Mitigation: Verify open orders directly on OKX after any stop or rescale failure and cancel remaining orders on the exchange if needed. <br>
Risk: The skill requires sensitive OKX API credentials with trade permission. <br>
Mitigation: Keep credentials out of chat, use the narrowest practical OKX permissions, and prefer low notional limits for initial operation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vm-development/okx-trading) <br>
- [OKX website](https://www.okx.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local pending-trade, strategy, snapshot, audit, and notional-log files under ~/.aeon/okx when scripts run.] <br>

## Skill Version(s): <br>
0.3.3 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
