## Description: <br>
医疗器械与耗材寻源-医疗器械招标网用于查询医疗器械品牌、设备型号或耗材的招中标价格趋势、品牌分析、采购单位和供应商明细。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thuanlynham-stack](https://clawhub.ai/user/thuanlynham-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Procurement, sourcing, and market-analysis users can use this skill to query Chinese bidding data for medical devices and consumables, compare historical unit prices, review brands and models, and inspect purchaser or supplier activity. It is most useful when an agent needs structured bid-search, company-analysis, and market-aggregation guidance backed by the ZhiLiaoBiaoXun API. <br>

### Deployment Geography for Use: <br>
Global; data and workflows are centered on Chinese procurement and bidding sources. <br>

## Known Risks and Mitigations: <br>
Risk: The API surface is broader than the medical-device sourcing description and includes business intelligence and contact lookup workflows. <br>
Mitigation: Keep the agent focused on the user's stated sourcing task and require confirmation before expanding company scope or retrieving contact information. <br>
Risk: The skill requires a sensitive third-party API key and may send sourcing queries or business plans to the provider. <br>
Mitigation: Use a dedicated ZLBX_API_KEY, avoid confidential sourcing plans unless the provider is trusted, and monitor quota and usage. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/thuanlynham-stack/medical-device-sourcing-yiliaoqixiezhaobiaowang) <br>
- [Bid search API reference](references/api-search.md) <br>
- [Company analysis API reference](references/api-company.md) <br>
- [Market analysis API reference](references/api-market.md) <br>
- [ZhiLiaoBiaoXun API key signup](https://ai.zhiliaobiaoxun.com/?ch=s37) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Configuration, Guidance] <br>
**Output Format:** [Markdown summaries with JSON API request examples and structured procurement analysis.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZLBX_API_KEY; outputs may include price trends, brand and model comparisons, purchaser and supplier details, and suggested follow-up analyses.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
