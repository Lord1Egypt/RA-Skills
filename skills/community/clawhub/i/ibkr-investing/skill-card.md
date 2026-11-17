## Description:

Invest on Interactive Brokers stocks and ETFs via IB Gateway with a human-in-the-loop confirmation gate for balances, quotes, trade proposals, confirmed executions, DCA setup, and portfolio snapshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vm-development](https://clawhub.ai/user/vm-development)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect Interactive Brokers account state, gather market context, create gated stock or ETF trade proposals, execute only user-confirmed proposals, and maintain DCA or portfolio snapshot workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real Interactive Brokers orders.

Mitigation: Start in paper mode, switch to live mode only after deliberate review, and keep per-trade and daily notional caps low.

Risk: Broker credentials and 2FA flow are handled by the local IB Gateway setup outside the skill package.

Mitigation: Pin and verify the gateway container and dependency versions before supplying IBKR credentials.

Risk: Execution depends on local pending proposal files that contain agent-readable confirmation tokens.

Mitigation: Keep pending files permission-restricted, use the printed absolute pending-file path, require explicit user confirmation, and let pending proposals expire quickly.

Risk: Scheduled workflows can broaden trading exposure if configured too aggressively.

Mitigation: Use schedules only for read-only checks or proposal creation, avoid broad unattended execution, and require human confirmation for each order.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vm-development/skills/ibkr-investing)
- [amuletxheart/ibkr-openclaw](https://clawhub.ai/amuletxheart/ibkr-openclaw)
- [gnzsnz/ib-gateway-docker](https://github.com/gnzsnz/ib-gateway-docker)
- [ib_async](https://github.com/ib-api-reloaded/ib_async)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also produce or reference local JSON proposal, audit, notional, snapshot, and strategy-state files during use.]

## Skill Version(s):

0.1.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
