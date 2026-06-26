## Description: <br>
Weather forecast analysis for Polymarket prediction markets using ensemble forecasts to compare forecast probabilities with market prices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lucasnocodo](https://clawhub.ai/user/Lucasnocodo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, prediction market traders, weather enthusiasts, and quantitative analysts use this skill to scan Polymarket weather markets, inspect ensemble forecasts, and identify potential pricing edge in temperature contracts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Forecast or weather-market scan requests, IP address, and any configured scanner API key are sent to the hosted scanner service. <br>
Mitigation: Use the skill only if that data sharing is acceptable, and use a dedicated POLYMARKET_SCANNER_API_KEY rather than unrelated credentials. <br>
Risk: POLYMARKET_SCANNER_HOST can redirect requests to a different host when defined in the environment. <br>
Mitigation: Check POLYMARKET_SCANNER_HOST before use and leave it unset unless intentionally using a trusted alternate endpoint. <br>
Risk: Market edge analysis may be incorrect, stale, or unsuitable for trading decisions. <br>
Mitigation: Treat outputs as analysis to review, not trading authority; do not provide wallet keys or allow automated trades based solely on the skill output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Lucasnocodo/polymarket-weather-scanner) <br>
- [Lucasnocodo publisher profile](https://clawhub.ai/user/Lucasnocodo) <br>
- [Scanner weather endpoint](https://polymarket-scanner.fly.dev/scan/weather) <br>
- [Forecast endpoint](https://polymarket-scanner.fly.dev/forecast/{city}) <br>
- [Cities endpoint](https://polymarket-scanner.fly.dev/cities) <br>
- [Tiers endpoint](https://polymarket-scanner.fly.dev/tiers) <br>
- [Free key endpoint](https://polymarket-scanner.fly.dev/keys/free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-formatted command output from shell scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; optional POLYMARKET_SCANNER_API_KEY enables expanded hosted API access.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
