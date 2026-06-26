## Description: <br>
Hong Kong IPO research assistant that gathers public IPO data on margin financing, cornerstone investors, ratings, grey-market activity, A+H discounts, and allotment odds for agent-assisted analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Marvae](https://clawhub.ai/user/Marvae) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to collect and summarize public Hong Kong IPO data before analysis. It supports IPO screening, sponsor-history checks, A+H discount calculations, allotment-odds estimates, and optional user-profile-aware research prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes public financial-data network requests while collecting IPO information. <br>
Mitigation: Use it only in environments where those outbound requests are acceptable and review collected data before relying on it. <br>
Risk: The optional profile feature can store capital, risk preference, margin preference, and broker information locally. <br>
Mitigation: Skip the profile feature unless local storage is intended, and delete scripts/config/user-profile.yaml when those details should no longer be retained. <br>
Risk: IPO analysis and allotment estimates can be incomplete or stale and are not investment advice. <br>
Mitigation: Cross-check results against current source documents and market data before making investment decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Marvae/hk-ipo-research-assistant) <br>
- [AiPO API documentation](references/aipo-api.md) <br>
- [IPO analysis guide](references/analysis-guide.md) <br>
- [API guide](references/api-guide.md) <br>
- [Hong Kong IPO mechanism guide](references/ipo-mechanism.md) <br>
- [Risk preference guide](references/risk-preferences.md) <br>
- [AiPO data source](https://aipo.myiqdii.com) <br>
- [AASTOCKS IPO data source](https://www.aastocks.com/tc/stocks/market/ipo/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON, formatted text tables, Markdown guidance, shell commands, and optional YAML configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some commands make public financial-data network requests; the profile flow can save local capital, risk preference, margin preference, and broker settings.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
