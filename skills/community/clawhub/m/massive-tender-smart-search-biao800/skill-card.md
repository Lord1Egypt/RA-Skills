## Description: <br>
海量标讯智搜助手-标800 helps agents search Biao800/Zhiliaobiaoxun tender data with complex keywords, exclusions, amount ranges, company analysis, and market analysis filters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pkuycl](https://clawhub.ai/user/pkuycl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and business development analysts use this skill to retrieve and analyze Biao800/Zhiliaobiaoxun bid notices, company profiles, competitors, potential suppliers, market rankings, and price trends. It is useful when precise tender search requires multiple keywords, match modes, exclusion terms, amount filters, geographic filters, or follow-up market analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive Biao800/Zhiliaobiaoxun API key and consumes service quota. <br>
Mitigation: Use a dedicated revocable API key, monitor quota usage, and rotate or revoke the key when access is no longer needed. <br>
Risk: Search terms, company names, and analysis requests are sent to an external tender-intelligence API. <br>
Mitigation: Avoid confidential searches unless external API sharing is approved for the user's organization. <br>
Risk: Company-name matching and contact lookup can affect the scope and sensitivity of downstream analysis. <br>
Mitigation: Ask the agent to confirm company matches before analysis or contact lookup when exact scope matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pkuycl/massive-tender-smart-search-biao800) <br>
- [Biao800 API key application](https://ai.zhiliaobiaoxun.com/?ch=s30) <br>
- [Biao800 API base endpoint](https://mcp-server.zhiliaobiaoxun.com/api_v2/{工具名}) <br>
- [标讯搜索类工具 API 详情](references/api-search.md) <br>
- [企业分析类工具 API 详情](references/api-company.md) <br>
- [市场分析类工具 API 详情](references/api-market.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown or text analysis based on JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the ZLBX_API_KEY credential and may consume Biao800/Zhiliaobiaoxun API quota.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
