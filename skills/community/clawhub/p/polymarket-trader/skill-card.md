## Description: <br>
Build, evaluate, and tune a Polymarket BTC 1h Up/Down trading strategy using Binance as the resolution anchor. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drakec48](https://clawhub.ai/user/drakec48) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and trading-system operators use this skill to analyze BTC 1h Up/Down Polymarket entries, exits, regime filters, and fill logs against Binance BTCUSDT data. It supports offline strategy review and parameter tuning; the evidence does not show direct order placement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can influence trading decisions even though the evidence does not show order placement. <br>
Mitigation: Use it as analysis support only and require explicit confirmation before any real Polymarket trade or account action. <br>
Risk: Local fill logs may contain sensitive trading history or account context. <br>
Mitigation: Run it only against the intended PaperBot events.jsonl file and avoid sharing logs or outputs that contain secrets or sensitive activity. <br>
Risk: Binance data requests can fail, be rate-limited, or become stale. <br>
Mitigation: Keep script sample sizes small, rerun analysis near decision time, and verify market data before relying on results. <br>


## Reference(s): <br>
- [Strategy Reference](references/strategy.md) <br>
- [Polymarket Trader on ClawHub](https://clawhub.ai/drakec48/polymarket-trader) <br>
- [Binance Public API Endpoint](https://api.binance.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, text, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands; bundled scripts emit JSON or tab-separated text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts fetch public Binance market data and may read a user-selected PaperBot events.jsonl file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
