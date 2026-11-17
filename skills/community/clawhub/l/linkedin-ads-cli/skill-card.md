## Description:

LinkedIn Ads data analysis and reporting via linkedin-ads-cli for performance analytics, account structure review, creative inspection, audience analysis, lead form retrieval, delivery forecasting, and budget recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bin-huang](https://clawhub.ai/user/bin-huang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and analysts use this skill to query LinkedIn Ads accounts, campaigns, creatives, audiences, lead forms, analytics, forecasts, and budget recommendations through a read-only CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses LinkedIn OAuth credentials.

Mitigation: Grant only the LinkedIn OAuth scopes needed for the task and keep tokens out of chat, command history, and logs.

Risk: Lead form response commands can retrieve personal data.

Mitigation: Retrieve raw lead-form responses only when the user is authorized and the data is necessary for the task.

Risk: The artifact suggests installing an unpinned global npm package.

Mitigation: Prefer a pinned, reviewed, local installation of `linkedin-ads-cli` before use.

## Reference(s):

- [LinkedIn Marketing API overview](https://learn.microsoft.com/en-us/linkedin/marketing/)
- [Ad Accounts API](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/account-structure/create-and-manage-accounts)
- [Ad Analytics API](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/ads-reporting)
- [Campaign Management](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/account-structure/create-and-manage-campaigns)
- [Lead Gen Forms API](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/advertising-targeting/lead-generation)
- [ClawHub skill page](https://clawhub.ai/bin-huang/skills/linkedin-ads-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented analysis.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides read-only linkedin-ads-cli usage; command results are expected as JSON.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
