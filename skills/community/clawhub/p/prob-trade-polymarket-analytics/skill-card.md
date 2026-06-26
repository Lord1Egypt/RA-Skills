## Description: <br>
Polymarket prediction markets: analytics, trading, hot markets, price movements, top traders, and market search. Powered by prob.trade. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vlprosvirkin](https://clawhub.ai/user/vlprosvirkin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill in OpenClaw agents to inspect Polymarket prediction-market data, monitor market movement and trader activity, and place or manage trades through prob.trade API credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place or cancel real Polymarket trades using configured API credentials without built-in confirmation or spending limits. <br>
Mitigation: Require explicit confirmation outside the skill for every buy, sell, or cancel action, and avoid enabling credentials in unattended or broad automation workflows. <br>
Risk: Configured prob.trade credentials can expose account data and trading capability if mishandled. <br>
Mitigation: Use revocable or least-privilege API keys when available and keep ~/.openclaw/skills/probtrade/config.yaml and related environment variables private. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vlprosvirkin/prob-trade-polymarket-analytics) <br>
- [prob.trade dashboard](https://app.prob.trade) <br>
- [prob.trade public API overview](https://api.prob.trade/api/public/overview) <br>
- [prob.trade public API documentation](https://prob.trade/docs/public-api) <br>
- [prob.trade trading API reference](https://github.com/vlprosvirkin/probtrade-openclaw-skill/blob/main/docs/trading-api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and prob.trade API credentials via environment variables or ~/.openclaw/skills/probtrade/config.yaml.] <br>

## Skill Version(s): <br>
2.0.5 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
