## Description: <br>
全国采招大数据中心-采招网 helps agents search procurement and bid records across regions and industries, combine company profile data with market analysis, and present procurement intelligence to users. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pkuycl](https://clawhub.ai/user/pkuycl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and business analysts use this skill to search procurement notices, retrieve bid details, profile companies, analyze buyers, suppliers, brands, and prices, and identify renewal or bidding opportunities through the Zhiliaobiaoxun procurement data API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Procurement queries, company names, and bid-related search terms are sent to the zhiliaobiaoxun.com API. <br>
Mitigation: Use the skill only for data you are comfortable sharing with that third-party API, and avoid confidential strategy, secrets, or personal data. <br>
Risk: The skill requires the sensitive ZLBX_API_KEY credential. <br>
Mitigation: Store the key in the configured environment variable and avoid pasting it into prompts, logs, or shared outputs. <br>
Risk: Company matching can include affiliates or subsidiaries and may broaden the scope of analysis. <br>
Mitigation: Confirm the intended company scope before relying on aggregated search, supplier, or purchaser analysis. <br>
Risk: Returned project contact details may include sensitive business contact information. <br>
Mitigation: Use contact details only for authorized business purposes and handle them according to applicable privacy and procurement rules. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pkuycl/national-procurement-data-center-caizhaowang) <br>
- [API overview and usage guide](artifact/SKILL.md) <br>
- [Bid search API reference](artifact/references/api-search.md) <br>
- [Company analysis API reference](artifact/references/api-company.md) <br>
- [Market analysis API reference](artifact/references/api-market.md) <br>
- [Zhiliaobiaoxun API key setup](https://ai.zhiliaobiaoxun.com/?ch=s32) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with JSON request examples when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include procurement search results, company profiles, market summaries, and follow-up analysis suggestions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
