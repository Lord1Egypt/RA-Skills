## Description: <br>
Analyzes options spreads across market regimes and returns conviction scores, strategy candidates, position sizing, and validation signals for vertical and multi-leg options strategies. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[AdamNaghs](https://clawhub.ai/user/AdamNaghs) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to evaluate options spread setups, compare strategy fit, and produce research-oriented conviction and sizing outputs for manual review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches market data, creates a local Python environment, and may cache options data. <br>
Mitigation: Install only in a trusted environment, inspect setup steps before use, and verify cached or fetched market data before acting on outputs. <br>
Risk: Installation guidance includes a sudo symlink step that may exceed what the finance-analysis workflow needs. <br>
Mitigation: Avoid the sudo symlink unless it has been reviewed and is necessary for the local PATH setup. <br>
Risk: EXECUTE and PREPARE labels can be mistaken for trading instructions. <br>
Mitigation: Treat conviction tiers and sizing outputs as research signals, not financial advice, and perform independent due diligence before any trade. <br>
Risk: Some options metrics rely on proxies, fallbacks, or market-data availability, which can reduce accuracy. <br>
Mitigation: Review live options data, implied volatility, liquidity, assignment, dividend, and pricing assumptions before relying on generated spread ideas. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/AdamNaghs/options-spread-conviction-engine) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Quant Scanner Documentation](artifact/QUANT_SCANNER.md) <br>
- [Multi-Leg Strategy Report](artifact/MULTI_LEG_REPORT.md) <br>
- [Code Review Report](artifact/CODE_REVIEW_REPORT.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text reports, Markdown guidance, and optional JSON output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include EXECUTE/PREPARE/WATCH/WAIT tiers, proposed strikes, market indicators, and position sizing signals that require human review.] <br>

## Skill Version(s): <br>
2.2.1 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
