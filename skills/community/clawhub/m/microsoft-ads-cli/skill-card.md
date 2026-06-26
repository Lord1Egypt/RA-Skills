## Description: <br>
Microsoft Ads data analysis and reporting via microsoft-ads-cli for checking Microsoft/Bing ad performance, account structure, audiences, conversion goals, and reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bin-huang](https://clawhub.ai/user/bin-huang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and analysts use this skill to query Microsoft Ads accounts, inspect campaign structure, retrieve performance reports, and troubleshoot advertising setup with microsoft-ads-cli. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Microsoft Ads access tokens, developer tokens, and local credentials can be exposed through chat, logs, shell history, or permissive file permissions. <br>
Mitigation: Use least-privileged credentials, avoid pasting tokens into chat or logs, avoid storing secrets in shell history, and protect credential files with restrictive permissions. <br>
Risk: Installing an unverified global npm package can introduce supply-chain risk. <br>
Mitigation: Verify the microsoft-ads-cli npm package before installation and pin a trusted version when possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bin-huang/microsoft-ads-cli) <br>
- [microsoft-ads-cli documentation](https://github.com/Bin-Huang/microsoft-ads-cli) <br>
- [Bing Ads API Getting Started](https://learn.microsoft.com/en-us/advertising/guides/get-started) <br>
- [Authentication with OAuth](https://learn.microsoft.com/en-us/advertising/guides/authentication-oauth) <br>
- [Campaign Management Service](https://learn.microsoft.com/en-us/advertising/campaign-management-service/campaign-management-service-reference) <br>
- [Reporting Service](https://learn.microsoft.com/en-us/advertising/reporting-service/reporting-service-reference) <br>
- [Customer Management Service](https://learn.microsoft.com/en-us/advertising/customer-management-service/customer-management-service-reference) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and summarized JSON results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses microsoft-ads-cli commands that require Microsoft Ads OAuth2 access and developer tokens.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
