## Description: <br>
Kalshi-native paper trading ledger and CLI for binary prediction contracts. Use for paper opens, marks, reconciliation, valuation, and review without relying on the generic spot-style paper trader. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BRS999](https://clawhub.ai/user/BRS999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-system builders use this skill to manage Kalshi-specific paper execution, account state, marks, reconciliation, valuation, and performance review for binary prediction contracts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paper-trading outputs may be mistaken for real trading instructions or financial advice. <br>
Mitigation: Keep the workflow limited to paper execution and ledger review, verify market tickers and quotes before acting on any analysis, and use separate controls for real trading. <br>
Risk: The local SQLite ledger may contain sensitive strategy, account, or market-research data. <br>
Mitigation: Use an explicit database path when needed, restrict file access, and remove test or temporary ledgers after review. <br>


## Reference(s): <br>
- [Kalshi Paper Ledger Proposal](references/kalshi-paper-ledger.md) <br>
- [Kalshi Documentation](https://docs.kalshi.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/BRS999/kalshi-paper-trading) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON CLI output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and stores paper-trading state in a local SQLite ledger.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
