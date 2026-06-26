## Description: <br>
Autonomous multi-strategy trading bot for Polymarket prediction markets that scans markets for parity arbitrage, tail-end trading, and logical arbitrage opportunities with paper mode, Kelly Criterion position sizing, circuit breakers, and optimizer integration via learned_config.json. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[georges91560](https://clawhub.ai/user/georges91560) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and operators use this skill to run an autonomous Polymarket market scanner and trading executor in paper mode, then live mode only after review and credential setup. It supports strategy scans, risk controls, portfolio and trade logs, Telegram alerts, and service setup guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can autonomously place real-money Polymarket trades. <br>
Mitigation: Keep PAPER_MODE=true until results are independently reviewed, then require human approval or strict caps before enabling live trading. <br>
Risk: Trading credentials and wallet access can expose real funds. <br>
Mitigation: Use a dedicated low-balance wallet and API key, avoid storing private keys on the server, and limit access to the environment that contains credentials. <br>
Risk: The artifact includes alerting and persistence patterns that can leak or misdirect operational information. <br>
Mitigation: Remove or explicitly set the Telegram chat destination and review workspace file permissions before running the executor. <br>
Risk: Long-running execution as root or without single-instance protection can increase operational impact. <br>
Mitigation: Avoid running as root, add single-instance protection, and monitor service restarts and logs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/georges91560/polymarket-executor-skill) <br>
- [Polymarket Executor Repository](https://github.com/georges91560/polymarket-executor) <br>
- [README](README.md) <br>
- [Configuration Guide](CONFIGURATION.md) <br>
- [Systemd Setup](SYSTEMD_SETUP.md) <br>
- [Polymarket CLOB API](https://clob.polymarket.com) <br>
- [Polymarket Gamma API](https://gamma-api.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, environment variable examples, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runtime execution can create JSON and JSONL trade, portfolio, performance, and configuration files in the configured workspace.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
