## Description: <br>
Google Ads API integration with managed OAuth for querying campaigns, ad groups, keywords, and performance metrics with GAQL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to query and work with Google Ads account data through Maton-managed OAuth, including campaign, ad group, keyword, and reporting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Google Ads account data and OAuth-authorized access flow through Maton's service. <br>
Mitigation: Use the intended Google Ads account and specify the correct Maton connection when multiple connections exist. <br>
Risk: Create, update, or delete operations can change advertising resources or account state. <br>
Mitigation: Require explicit confirmation of the target resource and intended effect before any write or delete action. <br>
Risk: Requests made through a manager account can target the wrong client account if identifiers are mixed up. <br>
Mitigation: Use the correct client customer ID and login-customer-id for manager-account workflows. <br>


## Reference(s): <br>
- [ClawHub Google Ads Skill Page](https://clawhub.ai/byungkyu/skills/google-ads-api) <br>
- [Related API Gateway Skill](https://clawhub.ai/byungkyu/api-gateway) <br>
- [Google Ads API Overview](https://developers.google.com/google-ads/api/docs/start) <br>
- [GAQL Reference](https://developers.google.com/google-ads/api/docs/query/overview) <br>
- [GAQL Fields Reference](https://developers.google.com/google-ads/api/fields/v24/overview) <br>
- [Google Ads Search Method](https://developers.google.com/google-ads/api/reference/rpc/v24/GoogleAdsService/Search) <br>
- [Maton CLI Manual](https://cli.maton.ai/manual) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown guidance with shell, Python, JavaScript, and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a Google Ads OAuth connection.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
