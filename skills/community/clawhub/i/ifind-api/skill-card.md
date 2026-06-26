## Description: <br>
同花顺 iFinD (51ifind.com) 金融数据查询，支持 A 股、基金、债券、期货、指数的实时行情、历史行情、财务指标、宏观经济数据等 18 个 API 接口。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sinabs](https://clawhub.ai/user/sinabs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and financial-data users use this skill to configure iFinD access and query Chinese market data through supported iFinD API endpoints. It can return market, financial, macroeconomic, fund, announcement, and portfolio-related API results for agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires durable iFinD credential handling through IFIND_REFRESH_TOKEN and may create local .env or .data token files. <br>
Mitigation: Configure IFIND_REFRESH_TOKEN through a secure local secret or environment mechanism, avoid pasting credentials into chat, and protect or delete local token files when finished. <br>
Risk: The supported iFinD API surface includes portfolio-changing actions. <br>
Mitigation: Restrict normal use to read-only endpoints unless the user explicitly intends to modify iFinD portfolio records. <br>


## Reference(s): <br>
- [iFinD API Reference](references/API_REFERENCE.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/sinabs/ifind-api) <br>
- [iFinD Official Site](https://www.51ifind.com) <br>
- [iFinD Quant API](https://quantapi.51ifind.com) <br>
- [iFinD Quant Terminal](https://ft.10jqka.com.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and raw JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires IFIND_REFRESH_TOKEN; API output depends on the selected iFinD endpoint and request body.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
