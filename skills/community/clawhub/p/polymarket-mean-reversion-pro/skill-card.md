## Description: <br>
Generates mean-reversion trading signals for Polymarket markets using price-deviation thresholds and technical filters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[themsquared](https://clawhub.ai/user/themsquared) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-automation operators use this skill to configure and run a Polymarket mean-reversion signal engine that can monitor markets, emit alerts, and optionally route signals to an execution flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Real-money trading automation can place Polymarket orders with unclear safety boundaries. <br>
Mitigation: Review before installing, use only an isolated low-balance wallet, and keep live mode disabled until per-trade approval controls are in place. <br>
Risk: Fixed Telegram and SQS destinations can send signals or queue messages to unintended external services. <br>
Mitigation: Replace or remove the hardcoded destinations and verify all notification and queue accounts before running the skill. <br>
Risk: Dry-run mode still routes signals to SQS according to the artifact behavior. <br>
Mitigation: Disable SQS publishing or use an isolated test queue before dry-run testing any downstream automation. <br>
Risk: The authoritative security guidance identifies a technical-indicator bug. <br>
Mitigation: Fix and test the indicator logic before using live mode or relying on generated trading signals. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/themsquared/polymarket-mean-reversion-pro) <br>
- [Publisher profile](https://clawhub.ai/user/themsquared) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; runtime text logs and structured signal dictionaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The artifact can send Telegram alerts, push messages to SQS, and place live Polymarket orders when configured; dry-run mode still pushes signals to SQS according to the artifact behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
