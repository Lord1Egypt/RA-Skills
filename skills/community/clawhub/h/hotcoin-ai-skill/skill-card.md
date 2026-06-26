## Description: <br>
Queries BTC/ETH perpetual contract market data, discovers newly listed tokens, and retrieves structured listing research reports from Hotcoin Exchange. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xss4755](https://clawhub.ai/user/xss4755) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and AI agents use this skill to retrieve Hotcoin public BTC/ETH perpetual market data, discover newly listed tokens, and summarize listing research. Outputs should be treated as informational market context rather than financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat market data or listing research outputs as financial advice. <br>
Mitigation: Present outputs as informational context, avoid trade recommendations, and encourage independent verification before making financial decisions. <br>
Risk: Users may provide exchange API keys even though the skill only needs public read-only endpoints. <br>
Mitigation: Do not provide API keys or private exchange credentials when using this skill. <br>
Risk: Hotcoin public API responses may be unavailable, rate limited, or time-sensitive. <br>
Mitigation: Check response status and timestamps, retry rate limits conservatively, and state when data could not be refreshed. <br>


## Reference(s): <br>
- [Hotcoin Exchange](https://www.hotcoin.com) <br>
- [Hotcoin Learn Research Index](https://www.hotcoin.com/zh_CN/learn/index/) <br>
- [Hotcoin Spot Market Public API Base](https://api.hotcoinfin.com) <br>
- [Hotcoin Perpetual Contract Public API Base](https://api-ct.hotcoin.fit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown summaries with JSON-shaped market and listing data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only public market data and research guidance; no trading actions or API keys are required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
