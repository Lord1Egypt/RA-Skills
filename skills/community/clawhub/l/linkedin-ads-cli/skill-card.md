## Description: <br>
LinkedIn Ads data analysis and reporting via linkedin-ads-cli for querying ad accounts, campaign analytics, creatives, audiences, lead forms, forecasts, and budget recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bin-huang](https://clawhub.ai/user/bin-huang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing operators, analysts, and developers use this skill to inspect LinkedIn ad account structure, retrieve read-only reporting data, and guide CLI-based analysis of campaigns, creatives, audiences, lead forms, forecasts, and budgets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help retrieve authorized LinkedIn Marketing data, including lead form submissions that may contain personal information. <br>
Mitigation: Use least-privileged OAuth credentials, request lead submissions only when needed, filter by account, form, and date range, and avoid displaying unnecessary personal information. <br>
Risk: Commands rely on the user's LinkedIn OAuth token and may fail or expose broader account data if credentials are over-scoped. <br>
Mitigation: Verify authentication with `linkedin-ads-cli me`, use only the OAuth scopes required for the requested task, and keep tokens out of shared output. <br>


## Reference(s): <br>
- [linkedin-ads-cli documentation](https://github.com/Bin-Huang/linkedin-ads-cli) <br>
- [LinkedIn Marketing API overview](https://learn.microsoft.com/en-us/linkedin/marketing/) <br>
- [LinkedIn Ad Accounts API](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/account-structure/create-and-manage-accounts) <br>
- [LinkedIn Ad Analytics API](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/ads-reporting) <br>
- [LinkedIn Campaign Management](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/account-structure/create-and-manage-campaigns) <br>
- [LinkedIn Lead Gen Forms API](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/advertising-targeting/lead-generation) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, json, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require authorized LinkedIn OAuth credentials and should be scoped to the requested account, form, and date range.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
