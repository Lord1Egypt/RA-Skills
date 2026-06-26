## Description: <br>
医疗大健康采招雷达-医疗招标采购网，当搜索词包含医院、医疗、卫生、体检时触发，重点提取采购方（医院）和中标方（医药公司/代理商），分析特定医院的Top供应商体系。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thuanlynham-stack](https://clawhub.ai/user/thuanlynham-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and procurement analysts use this skill to search medical and healthcare bidding data, inspect purchaser and supplier patterns, and compare companies, brands, prices, expiring projects, and market activity through the Zhiliaobiaoxun API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends procurement searches and API credentials to an external Zhiliaobiaoxun service. <br>
Mitigation: Install only if that provider is trusted for the intended searches, and use a limited API key through ZLBX_API_KEY. <br>
Risk: Broad company or subsidiary matching can produce ambiguous business analysis. <br>
Mitigation: Confirm ambiguous company matches before relying on subsidiary-wide analysis or downstream conclusions. <br>
Risk: Returned project contact details may contain sensitive business or personal information. <br>
Mitigation: Handle contact data according to the user's privacy, compliance, and retention requirements. <br>
Risk: Confidential procurement strategy could be exposed through submitted queries. <br>
Mitigation: Avoid submitting confidential strategy or sensitive internal plans unless that use is acceptable under the provider's terms. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thuanlynham-stack/medical-health-bid-radar-yiliaozhaobiaocaigouwang) <br>
- [Bid search API reference](references/api-search.md) <br>
- [Company analysis API reference](references/api-company.md) <br>
- [Market analysis API reference](references/api-market.md) <br>
- [Zhiliaobiaoxun API endpoint](https://mcp-server.zhiliaobiaoxun.com/api_v2/{工具名}) <br>
- [Zhiliaobiaoxun API key portal](https://ai.zhiliaobiaoxun.com/?ch=s36) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown and structured API request or response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZLBX_API_KEY for authenticated Zhiliaobiaoxun API access.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
