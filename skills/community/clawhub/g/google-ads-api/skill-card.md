## Description: <br>
Google Ads API integration with managed OAuth for querying campaigns, ad groups, keywords, and performance metrics with GAQL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to access Google Ads data through Maton-managed OAuth, run GAQL searches, inspect accounts, campaigns, ad groups, keywords, and performance metrics, and prepare approved account-management requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses sensitive Maton credentials and Google Ads OAuth connections to access account data. <br>
Mitigation: Install only if Maton is trusted for the connected account, keep MATON_API_KEY secret, connect only the intended Google Ads account, and specify the connection when multiple accounts exist. <br>
Risk: Create, update, or delete requests could change Google Ads account resources. <br>
Mitigation: Review the target resource and intended effect with the user before approving any write operation. <br>
Risk: Requests may run against the wrong client account or manager account context. <br>
Mitigation: Use listAccessibleCustomers first, provide the client customer ID, pass login-customer-id for manager account access, and avoid running metrics queries directly against manager accounts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/google-ads-api) <br>
- [Google Ads API Overview](https://developers.google.com/google-ads/api/docs/start) <br>
- [GAQL Reference](https://developers.google.com/google-ads/api/docs/query/overview) <br>
- [GAQL Grammar](https://developers.google.com/google-ads/api/docs/query/grammar) <br>
- [GAQL Cookbook](https://developers.google.com/google-ads/api/docs/query/cookbook) <br>
- [Google Ads API v24 Fields Reference](https://developers.google.com/google-ads/api/fields/v24/overview) <br>
- [Google Ads API v24 Metrics Reference](https://developers.google.com/google-ads/api/fields/v24/metrics) <br>
- [Google Ads API Search Reference](https://developers.google.com/google-ads/api/reference/rpc/v24/GoogleAdsService/Search) <br>
- [Maton CLI Manual](https://cli.maton.ai/manual) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash, Python, JavaScript, SQL, HTTP, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and an intended Google Ads OAuth connection.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
