## Description: <br>
Build, evaluate, and tune a Polymarket BTC 1h Up/Down trading strategy using Binance BTCUSDT data as the resolution anchor for fair-probability modeling, regime filtering, and fill analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parkhyeongjoon](https://clawhub.ai/user/parkhyeongjoon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-system operators use this skill to analyze Polymarket BTC 1h Up/Down markets, estimate fair Up/Down probabilities from Binance BTCUSDT data, tune entry and exit parameters, and explain fills from local event logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence marks the release as suspicious. <br>
Mitigation: Install only in a trusted environment and review the artifact files and commands before running the skill. <br>
Risk: Bundled scripts make network requests to Binance and can use local trade-event logs. <br>
Mitigation: Run the scripts with the intended symbol, event-log path, and network access, and review outputs before using them to inform trading decisions. <br>


## Reference(s): <br>
- [Strategy reference](references/strategy.md) <br>
- [Binance API endpoint](https://api.binance.com) <br>
- [ClawHub skill page](https://clawhub.ai/parkhyeongjoon/polymarket-trader-1-0-0) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with Python script commands and JSON or tabular command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bundled scripts fetch public Binance market data and may read local events.jsonl files when explaining fills.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
