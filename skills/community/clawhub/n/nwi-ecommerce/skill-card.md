## Description: <br>
NWi诺舟智数提供的跨境电商数据洞察（Amazon/Shopee/Lazada/TikTok）。触发词：电商数据、销量、销额、品类分布、品牌排行、店铺排行、东南亚市场 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nwi-official](https://clawhub.ai/user/nwi-official) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and commerce analysts use this skill to query NWi/Nint e-commerce analytics for Amazon, Shopee, Lazada, and TikTok Shop by marketplace, category, brand, store, and product. It helps an agent construct API requests, interpret JSON responses, validate returned metrics, and summarize sales and ranking insights. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an NWi/Nint API key and may store it locally. <br>
Mitigation: Treat the API key as a secret, avoid sharing logs or screenshots that expose requests, and delete or rotate the local key when the analysis is complete. <br>
Risk: Requests are sent to the documented NWi backend and may contain sensitive business queries. <br>
Mitigation: Use the skill only when sharing the relevant query details with NWi is acceptable, and review the documented API behavior before using sensitive competitive or commercial data. <br>
Risk: The release evidence flags under-scoped data-sharing and contact-collection behavior. <br>
Mitigation: Review the contact-upgrade and anomaly-reporting flows before enabling them, and require user authorization before sending anomaly reports or contact details. <br>


## Reference(s): <br>
- [API Reference](references/api.md) <br>
- [Platform ID Reference](references/platform_ids.md) <br>
- [Skill page](https://clawhub.ai/nwi-official/nwi-ecommerce) <br>
- [NWi official website](https://nuozhoushuzhi.com/) <br>
- [Nint official website](https://www.nint.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, API Calls, Shell commands, Markdown, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with tables, summaries, JSON interpretation, and inline curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use locally stored API keys and NWi/Nint API responses; returned metrics may require numeric conversion before analysis.] <br>

## Skill Version(s): <br>
0.0.7 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
