## Description: <br>
Klaviyo API integration with managed OAuth for managing profiles, lists, segments, campaigns, flows, events, metrics, templates, catalogs, and webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xspeter](https://clawhub.ai/user/0xspeter) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and marketing operations teams use this skill to access Klaviyo through Maton-managed OAuth, manage customer data and audiences, and automate campaign, flow, event, catalog, and webhook workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Maton brokers OAuth access to the user's Klaviyo account. <br>
Mitigation: Install only when Maton is trusted, use least-privilege Klaviyo access where possible, and keep MATON_API_KEY scoped and protected. <br>
Risk: API calls can change customer data, subscriptions, suppressions, webhooks, campaigns, flows, catalogs, and templates. <br>
Mitigation: Require explicit human review before deletes, campaign sends, webhook changes, bulk imports, or subscription and suppression changes. <br>
Risk: Multiple active Klaviyo connections can route requests to the wrong account. <br>
Mitigation: Specify the intended Maton connection when more than one Klaviyo account is connected. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/0xspeter/klaviyo-1-0-4) <br>
- [Klaviyo API documentation](https://developers.klaviyo.com) <br>
- [Klaviyo API reference](https://developers.klaviyo.com/en/reference/api_overview) <br>
- [Klaviyo developer portal](https://developers.klaviyo.com/en) <br>
- [Maton account settings](https://maton.ai/settings) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, API Calls, Configuration] <br>
**Output Format:** [Markdown with Python, JavaScript, HTTP, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a Klaviyo API revision header.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
