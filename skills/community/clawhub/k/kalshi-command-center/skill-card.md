## Description: <br>
Complete Kalshi trading command interface for OpenClaw agents, covering portfolio P&L, live market scanning with edge scoring, market lookup, order execution, order cancellation, and risk management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingmadellc](https://clawhub.ai/user/kingmadellc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an OpenClaw agent inspect Kalshi balances and positions, scan markets, retrieve live bid/ask data, place or cancel orders, and maintain an audit trail for prediction-market trading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place and cancel live Kalshi financial orders using account credentials. <br>
Mitigation: Install only for agents authorized to access the Kalshi account, protect KALSHI_KEY_ID and KALSHI_KEY_PATH as secrets, and require manual confirmation before live trades. <br>
Risk: The server security review says the release overstates some safety controls, including the advertised daily loss cutoff. <br>
Mitigation: Do not rely on the advertised $50 daily loss cutoff until enforcement is verified before every order; use external account limits and review audit logs. <br>
Risk: Order status reconciliation can be uncertain after submission. <br>
Mitigation: When the skill reports an unverified order, confirm resting orders, positions, and cancellations directly in Kalshi before continuing to trade. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kingmadellc/kalshi-command-center) <br>
- [Kalshi](https://kalshi.com) <br>
- [Market blocklist](references/blocklist.md) <br>
- [Risk limits](references/risk-limits.md) <br>
- [Scoring algorithm](references/scoring.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text command responses with concise status, market, portfolio, and order details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call the Kalshi API, read local OpenClaw configuration, and append trade audit records when trading commands run.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
