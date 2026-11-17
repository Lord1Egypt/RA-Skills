## Description:

Microsoft Ads data analysis and reporting via microsoft-ads-cli for campaign, ad group, keyword, audience, conversion goal, and performance report workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bin-huang](https://clawhub.ai/user/bin-huang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and advertising operations teams use this skill to query Microsoft Ads account structure, inspect campaign entities, and pull performance reporting through microsoft-ads-cli.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to install an unpinned third-party npm CLI that handles Microsoft Ads credentials and account reporting data.

Mitigation: Use a pinned, reviewed local install of microsoft-ads-cli, avoid elevated privileges, and keep Microsoft Ads credentials tightly permissioned.

Risk: Microsoft Ads OAuth access tokens, developer tokens, customer IDs, and account IDs may expose advertising account data if stored or shared insecurely.

Mitigation: Prefer per-command credential files or environment variables with least necessary access, restrict file permissions, and avoid including credentials in logs or shared transcripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bin-huang/skills/microsoft-ads-cli)
- [microsoft-ads-cli documentation](https://github.com/Bin-Huang/microsoft-ads-cli)
- [Bing Ads API Getting Started](https://learn.microsoft.com/en-us/advertising/guides/get-started)
- [Authentication with OAuth](https://learn.microsoft.com/en-us/advertising/guides/authentication-oauth)
- [Campaign Management Service](https://learn.microsoft.com/en-us/advertising/campaign-management-service/campaign-management-service-reference)
- [Reporting Service](https://learn.microsoft.com/en-us/advertising/reporting-service/reporting-service-reference)
- [Customer Management Service](https://learn.microsoft.com/en-us/advertising/customer-management-service/customer-management-service-reference)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands query Microsoft Ads through microsoft-ads-cli and usually return pretty-printed JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
