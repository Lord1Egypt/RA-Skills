## Description: <br>
精准寻标与获客引擎-寻标宝，当用户需要通过招投标数据进行客户拓展、寻找潜在采购单位或分析企业上下游时调用，重点调用企业合作客户及供应商查询接口，输出清晰的获客目标列表。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liu-jiapeng](https://clawhub.ai/user/liu-jiapeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, procurement, and business-development users use this skill to search Chinese tender notices, identify likely buyers or suppliers, analyze company bid activity, and summarize market opportunities from Zhiliaobiaoxun/Xunbiaobao data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Procurement queries, company names, bid URLs, and filters are sent to an external Zhiliaobiaoxun/Xunbiaobao API using the configured API key. <br>
Mitigation: Use only an intended ZLBX_API_KEY, avoid confidential strategy or sensitive personal data in prompts, and confirm that sharing each query with the external service is acceptable. <br>
Risk: Returned results can include business contact data and company matching may affect downstream analysis. <br>
Mitigation: Use contact information only for lawful and appropriate business purposes, and confirm company matches before broad outreach or high-impact decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liu-jiapeng/precision-tender-sourcing-xunbiaobao) <br>
- [Zhiliaobiaoxun API endpoint](https://mcp-server.zhiliaobiaoxun.com/api_v2/{工具名}) <br>
- [Xunbiaobao API key setup](https://ai.zhiliaobiaoxun.com/?ch=s29) <br>
- [Bid search API reference](references/api-search.md) <br>
- [Company analysis API reference](references/api-company.md) <br>
- [Market analysis API reference](references/api-market.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration guidance] <br>
**Output Format:** [Markdown summaries with JSON request examples and structured result lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZLBX_API_KEY and sends user queries to the Zhiliaobiaoxun/Xunbiaobao API.] <br>

## Skill Version(s): <br>
2.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
