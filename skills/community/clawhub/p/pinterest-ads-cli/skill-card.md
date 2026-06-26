## Description: <br>
Pinterest Ads data analysis and reporting via pinterest-ads-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bin-huang](https://clawhub.ai/user/bin-huang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing analysts, advertisers, and developers use this skill to run read-only Pinterest Ads CLI commands for campaign reporting, account inspection, billing review, catalog checks, trend discovery, and analytics with attribution windows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Pinterest OAuth2 access token and can access advertising, billing, audience, catalog, lead-form, or customer-list data. <br>
Mitigation: Use a least-privilege token with only the read scopes needed for the task and avoid exposing token values in prompts, logs, or command output. <br>
Risk: The skill instructs agents to install and run an external npm CLI package. <br>
Mitigation: Verify the npm package before global installation and install it only when the user intends to use pinterest-ads-cli for Pinterest Ads reporting. <br>


## Reference(s): <br>
- [pinterest-ads-cli documentation](https://github.com/Bin-Huang/pinterest-ads-cli) <br>
- [Pinterest API v5 overview](https://developers.pinterest.com/docs/api/v5/) <br>
- [Pinterest OAuth authentication](https://developers.pinterest.com/docs/getting-started/authentication/) <br>
- [Pinterest Analytics API](https://developers.pinterest.com/docs/api/v5/#tag/ad_accounts) <br>
- [Pinterest Catalogs API](https://developers.pinterest.com/docs/api/v5/#tag/catalogs) <br>
- [Pinterest Trends API](https://developers.pinterest.com/docs/api/v5/#tag/trends) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples; CLI commands return JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Pinterest OAuth2 access token; commands are described as read-only and may access advertising, billing, audience, catalog, and lead-form data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
