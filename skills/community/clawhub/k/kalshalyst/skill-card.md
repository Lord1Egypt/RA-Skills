## Description: <br>
Kalshalyst scans Kalshi prediction markets for contrarian mispricings using Claude Sonnet analysis, tracks calibration with Brier scores, sizes opportunities with Kelly Criterion, and can feed automated trading workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingmadellc](https://clawhub.ai/user/kingmadellc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and traders use Kalshalyst to scan Kalshi markets, estimate directional edge, generate alerts and cache files, size positions, and optionally run an auto-trader with user-provided Kalshi credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release can trade and cancel Kalshi orders despite being partly described as a scanner. <br>
Mitigation: Install only when a full prediction-market trading stack is intended; start in dry-run and keep auto_trader_config disabled until risk limits are reviewed. <br>
Risk: Kalshi and Anthropic credentials may enable account access, trading, and paid model usage. <br>
Mitigation: Protect API keys and private key files, rotate exposed credentials, and configure only the services needed for the intended workflow. <br>
Risk: Slack or webhook exports can disclose trade details outside the local environment. <br>
Mitigation: Avoid enabling Slack or webhook exports unless external sharing of trading information is acceptable. <br>
Risk: Related local stack components can affect behavior when this skill is used with sibling tools. <br>
Mitigation: Inspect any sibling kalshi-command-center and prompt-lab code before enabling integrated trading workflows. <br>


## Reference(s): <br>
- [Kalshalyst README](artifact/README.md) <br>
- [Kalshalyst Skill Documentation](artifact/SKILL.md) <br>
- [Blocklist Reference](artifact/references/blocklist.md) <br>
- [Brier Score Schema and Methodology](artifact/references/brier-schema.md) <br>
- [Contrarian Estimation System Prompt](artifact/references/contrarian-prompt.md) <br>
- [Kelly Criterion Position Sizing](artifact/references/kelly-math.md) <br>
- [Kalshi](https://kalshi.com) <br>
- [Anthropic Console](https://console.anthropic.com) <br>
- [Polygon.io](https://polygon.io) <br>
- [Ollama](https://ollama.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline JSON, YAML, shell commands, and generated analysis text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local JSON cache, SQLite calibration data, logs, and trading-state files when its scripts are executed.] <br>

## Skill Version(s): <br>
1.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
