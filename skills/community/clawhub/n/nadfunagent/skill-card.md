## Description: <br>
Autonomous Nad.fun trading agent that scans markets via API and indexer, analyzes tokens, executes trades, and shares profits with MMIND token holders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[encipher88](https://clawhub.ai/user/encipher88) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to run an autonomous Nad.fun trading workflow on Monad, including market scanning, token scoring, trade execution, position monitoring, and MMIND profit distribution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for wallet private keys and stores sensitive trading configuration. <br>
Mitigation: Use a dedicated low-balance wallet, keep secrets in a protected environment file, and never paste a production private key into chat. <br>
Risk: The skill can run unattended live crypto trades and may lose funds. <br>
Mitigation: Start with dry-run or manual review, avoid enabling cron until the strategy is understood, and keep strict position-size limits. <br>
Risk: The security scan reports unsafe shell-command construction. <br>
Mitigation: Review and fix command construction before using the skill with meaningful funds, and run it in an isolated environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/encipher88/nadfunagent) <br>
- [README.md](README.md) <br>
- [DEPENDENCIES.md](DEPENDENCIES.md) <br>
- [INSTALL.md](INSTALL.md) <br>
- [Trading README](trading/README.md) <br>
- [P&L documentation](trading/HOW_PNL_WORKS.md) <br>
- [Entry price tracking](trading/ENTRY_PRICE_TRACKING.md) <br>
- [Nad.fun](https://nad.fun) <br>
- [Nad.fun API](https://api.nadapp.net) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration values, script invocations, and JSON report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local token and position report files when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
