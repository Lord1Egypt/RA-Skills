## Description:

Trade Polymarket BTC 5-minute and 15-minute fast markets using CEX price momentum signals via Simmer API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leogordon2004](https://clawhub.ai/user/leogordon2004)

### License/Terms of Use:


## Use Case:

External developers and trading agents use this skill to configure and run short-window Polymarket trading cycles driven by Binance or CoinGecko price momentum signals. It supports dry-run analysis, live trade execution, position checks, smart sizing, and configuration updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary reports that dry-run mode can still make an authenticated remote Simmer market-import/share request before stopping short of a trade.

Mitigation: Use a controlled account and API key, test with strict limits, and do not treat dry-run as side-effect free.

Risk: Live or scheduled runs can execute automated Polymarket trades with real USDC.

Mitigation: Require explicit live-mode approval, set conservative max_position and smart-sizing limits, and review any cron or heartbeat setup as live automated trading.

Risk: The security guidance warns about untrusted tradejournal modules on the Python import path.

Mitigation: Run the skill in an isolated Python environment and keep untrusted modules off the import path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leogordon2004/skills/poly)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with CLI commands, JSON configuration, and Python script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY for authenticated Simmer API access.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.0.6)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
