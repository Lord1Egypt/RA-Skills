## Description: <br>
Unified crypto market data API and scripts for exchanges, markets, tickers, OHLCV, and orderbooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Kmasterrr](https://clawhub.ai/user/Kmasterrr) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, data engineers, analysts, and agent operators use this skill to query normalized crypto market data from Milaex for exchange coverage, markets, tickers, OHLCV candles, and orderbook snapshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MILAEX_API_KEY could be exposed if placed in prompts, logs, or shell history. <br>
Mitigation: Store the key in the configured secret location and use a revocable or limited API key if Milaex supports it. <br>
Risk: MILAEX_BASE_URL can redirect requests to a replacement endpoint. <br>
Mitigation: Leave MILAEX_BASE_URL unset unless the replacement endpoint is intentionally trusted. <br>
Risk: Installing Python dependencies from an untrusted environment can introduce supply-chain risk. <br>
Mitigation: Install dependencies from a trusted Python environment or package source. <br>


## Reference(s): <br>
- [Milaex API documentation](https://api.milaex.com/api-docs/index.html) <br>
- [Milaex service website](https://milaex.com) <br>
- [ClawHub skill page](https://clawhub.ai/Kmasterrr/milaex-crypto-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts print JSON to stdout and may print rate-limit or error details to stderr.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
