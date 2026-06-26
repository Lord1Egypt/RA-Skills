## Description: <br>
Google Ads data analysis and reporting via google-ads-open-cli for account structure, performance stats, conversion audits, and custom GAQL queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bin-huang](https://clawhub.ai/user/bin-huang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing analysts, account managers, and developers use this skill to inspect authorized Google Ads accounts, pull performance reports, audit conversions, and compose GAQL queries through a read-only CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can query sensitive Google Ads account data when local OAuth and developer tokens are available. <br>
Mitigation: Use least-privilege credentials, authorize only intended accounts, and avoid pasting or printing secrets in prompts or outputs. <br>
Risk: Reports or GAQL queries may target the wrong customer account, field set, or date range. <br>
Mitigation: Confirm the customer ID before running reports and keep queries limited to the fields and date ranges needed. <br>
Risk: The workflow depends on an external npm CLI package. <br>
Mitigation: Install and run google-ads-open-cli only from a trusted source in environments where querying Google Ads data is intended. <br>


## Reference(s): <br>
- [google-ads-open-cli documentation](https://github.com/Bin-Huang/google-ads-open-cli) <br>
- [Google Ads API overview](https://developers.google.com/google-ads/api/docs/start) <br>
- [GAQL reference](https://developers.google.com/google-ads/api/docs/query/overview) <br>
- [GAQL grammar](https://developers.google.com/google-ads/api/docs/query/grammar) <br>
- [Google Ads API field reference v23](https://developers.google.com/google-ads/api/fields/v23/overview) <br>
- [GAQL query cookbook](https://developers.google.com/google-ads/api/docs/query/cookbook) <br>
- [Google Ads segmentation rules](https://developers.google.com/google-ads/api/docs/reporting/segmentation) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Analysis] <br>
**Output Format:** [Markdown with inline shell commands and JSON result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Google Ads monetary values are returned in micros and should be converted to currency before presentation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
