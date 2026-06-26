## Description: <br>
Run a structured paper-trading loop with SQLite-backed event logging, position tracking, and PnL review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BRS999](https://clawhub.ai/user/BRS999) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to record simulated trades, market snapshots, thesis notes, stop/take levels, and periodic portfolio reviews before committing live capital. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Simulated trades, strategy notes, and review data persist in a local SQLite database. <br>
Mitigation: Use --db to choose a controlled storage location and avoid recording sensitive real-account details unless local persistence is intended. <br>
Risk: Paper-trading status and review output depends on user-supplied snapshots and does not execute or verify live trades. <br>
Mitigation: Treat outputs as journaling and review aids; verify market data and decisions separately before using real capital. <br>


## Reference(s): <br>
- [Paper Trader on ClawHub](https://clawhub.ai/BRS999/paper-trader) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; CLI output as text or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates a local SQLite paper-trading database when commands are run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
