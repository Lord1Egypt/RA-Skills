## Description: <br>
Trade Polymarket strike/action markets using military aircraft ADS-B positioning via pref.trade. Fires when tracked mil aircraft cluster in a target region. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[simmer](https://clawhub.ai/user/simmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external traders use this skill to monitor military aircraft cluster signals and evaluate Polymarket strike/action market opportunities through Simmer and pref.trade. It defaults to dry-run or paper-trading workflows unless live trading is explicitly enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can execute real-money trades and cause financial loss. <br>
Mitigation: Start in dry-run or TRADING_VENUE=sim, review dollar caps and kill switches, and avoid --no-safeguards unless intentionally accepting the added trading risk. <br>
Risk: The skill requires sensitive Simmer and pref.trade credentials. <br>
Mitigation: Keep API keys private, store pref.trade credentials in the documented credentials file or environment variables, and avoid placing secrets in logs, issues, pull requests, or prompts. <br>
Risk: Military aircraft clustering is a heuristic signal and may not predict market outcomes. <br>
Mitigation: Treat outputs as strategy exploration, review market context before live execution, and use conservative position sizing limits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/simmer/polymarket-mil-aircraft-tracker) <br>
- [pref.trade MCP endpoint](https://pref.trade/mcp) <br>
- [pref.trade agent registration endpoint](https://pref.trade/v1/agents/register) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions and console text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run by default; live trading requires the --live flag, configured credentials, and a linked wallet.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
