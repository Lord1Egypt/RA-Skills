## Description: <br>
Prediction markets data - Polymarket, Kalshi markets, prices, positions, and trades <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aisadocs](https://clawhub.ai/user/aisadocs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query Polymarket and Kalshi market data, prices, orderbooks, trades, wallet positions, and matching sports markets through the AIsa API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API-key-backed billing and prediction-market queries are sent to AIsa endpoints. <br>
Mitigation: Use a scoped or low-balance AISA_API_KEY when available and avoid exposing the key in logs, prompts, or screenshots. <br>
Risk: Public wallet addresses queried through the skill can reveal trading behavior when analyzed by a third-party service. <br>
Mitigation: Only query wallet addresses that are appropriate to share with AIsa and avoid mixing sensitive wallet analysis with unrelated workflows. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aisadocs/pred-polymarket) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [AIsa API Reference](https://docs.aisa.one/reference/) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and uses read-only GET requests to AIsa prediction-market endpoints.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
