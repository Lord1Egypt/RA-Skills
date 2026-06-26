## Description: <br>
High-frequency paper trading framework for crypto with multi-indicator TA scoring, Kelly position sizing, stop-loss management, and trade ledger support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JamieRossouw](https://clawhub.ai/user/JamieRossouw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and trading-system builders use this skill to simulate crypto paper trading workflows, backtest trading logic, inspect portfolio performance, and generate autonomous trading-agent guidance without connecting live exchange credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paper-trading instructions could be mistaken for live trading or connected to real exchange credentials. <br>
Mitigation: Keep usage paper-only unless a separate audit approves live trading, and do not provide real exchange credentials during normal runs. <br>
Risk: Stateful files such as PORTFOLIO.json, LEDGER.csv, and lessons.md may carry stale simulated results between runs. <br>
Mitigation: Review or reset local portfolio, ledger, and lessons files before runs where clean state matters. <br>
Risk: Autonomous watchlist scans can run broader or longer simulated trading activity than intended. <br>
Mitigation: Explicitly set symbols, time window, maximum trade count, and whether local files may be updated before invocation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/JamieRossouw/hft-paper-trader) <br>
- [JamieRossouw Publisher Profile](https://clawhub.ai/user/JamieRossouw) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with trading-analysis summaries, paper-trading actions, and file-update guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference or update local paper-trading state files such as PORTFOLIO.json, LEDGER.csv, and lessons.md when permitted by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
