## Description:

Operate the Moltrade trading bot for configuration, backtesting, test-mode runs, Nostr signal broadcast, exchange adapters, and strategy integration in OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouhuihui008](https://clawhub.ai/user/zhouhuihui008)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading-bot operators use this skill to configure Moltrade, run backtests and test-mode sessions, integrate exchanges and strategies, and prepare live trading workflows with explicit human approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide live trading or public posting actions with financial or account-impacting consequences.

Mitigation: Use testnet, dry-run, or test mode first; restrict API permissions; and require explicit human confirmation before any live trade or Binance Square post.

Risk: Setup may involve wallet private keys, exchange API secrets, Nostr keys, or posting credentials.

Mitigation: Do not paste secrets into chat, prefer environment variables or a secret manager, have the human initialize secrets locally, and redact configs and logs before review.

Risk: Dependency installation and upstream code changes can affect trading behavior.

Mitigation: Review the upstream repository in an isolated environment and pin dependencies before running the bot.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhouhuihui008/skills/moltrade-1-0-9)
- [Moltrade Homepage](https://github.com/hetu-project/moltrade.git)
- [Moltrade Website](https://www.moltrade.ai/)
- [Binance Spot Authentication Reference](artifact/binance/spot/references/authentication.md)
- [Binance Testnet](https://testnet.binance.vision)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include redacted configuration diffs, backtest summaries, validation checklists, and explicit confirmation prompts before live trading or posting.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact _meta.json reports 1.0.9)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
