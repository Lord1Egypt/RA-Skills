## Description: <br>
Snipe Polymarket opportunities from your own signal sources. Monitors RSS feeds with Trading Agent-grade safeguards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simmer](https://clawhub.ai/user/simmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Traders and agent operators use this skill to monitor RSS feeds for Polymarket-relevant signals, match articles to target markets, inspect context warnings, and optionally run dry-run or live trade flows through Simmer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect a Simmer trading account and potentially place real Polymarket trades. <br>
Mitigation: Use dry-run or paper mode first, set conservative trade caps, and run live mode only when the operator accepts the financial risk. <br>
Risk: Live trading may use high-impact wallet or account authority, including sensitive credentials. <br>
Mitigation: Prefer a dedicated low-balance wallet, avoid production private keys, and provide credentials through environment variables or a secret store. <br>
Risk: The security review notes automatic account-level behavior and no per-trade confirmation for unattended live runs. <br>
Mitigation: Do not run --live unattended unless the operator has reviewed and accepted the auto-redeem behavior and missing per-trade confirmation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/simmer/polymarket-signal-sniper) <br>
- [Disclaimer](DISCLAIMER.md) <br>
- [Simmer API Base](https://api.simmer.markets) <br>
- [Simmer Dashboard](https://simmer.markets/dashboard) <br>
- [Simmer V2 Migration Guide](https://docs.simmer.markets/v2-migration) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, configuration variables, trading status output, and risk warnings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands that inspect a Simmer account or run dry-run, scan-only, or live Polymarket trading flows using user-provided credentials.] <br>

## Skill Version(s): <br>
1.5.3 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
