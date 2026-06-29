## Description: <br>
Helps agents write a Bollinger-band mean-reversion trading strategy for Superior Trade using the validated 4h Bollinger Bands and ADX<25 variant. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[superior-ai](https://clawhub.ai/user/superior-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-strategy authors use this skill to draft a Freqtrade-style Bollinger-band mean-reversion strategy, including strategy code, reference configuration, and risk framing for range-bound markets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The strategy examples involve futures, margin, and short positions, which can cause financial losses. <br>
Mitigation: Use the skill only as a strategy-writing reference, understand liquidation, margin, short-position, fee, and slippage risks, and avoid live trading until those risks are reviewed. <br>
Risk: Backtest results may not generalize to future market regimes or to unsupported pairs. <br>
Mitigation: Backtest independently on the intended pairs and time windows, then begin with dry-run or paper trading before considering live deployment. <br>
Risk: Connecting exchange keys or enabling live bot execution without explicit safeguards could create unintended trades. <br>
Mitigation: Add an explicit dry_run setting before any bot use and do not connect exchange keys until live-trading readiness has been reviewed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with Python strategy code and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Trading-strategy guidance should be reviewed, independently backtested, and tested in dry-run or paper-trading mode before live use.] <br>

## Skill Version(s): <br>
0.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
