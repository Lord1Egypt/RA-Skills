## Description: <br>
Mx Data provides natural-language access to East Money-backed financial market, financial statement, relationship, and business operations data through the Meixiang API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xpmars](https://clawhub.ai/user/xpmars) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve current market quotes, financial indicators, company details, shareholder and executive information, and related business data for finance-focused queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries are sent to a disclosed third-party financial data API with a user-provided API key. <br>
Mitigation: Install only if the Meixiang financial data service is trusted, keep MX_APIKEY out of chat and committed files, and avoid sending confidential portfolio, client, or business information unless approved. <br>
Risk: Broad financial queries can return large raw data sets that may exceed context limits or be hard to review. <br>
Mitigation: Use specific securities, indicators, and time ranges, and summarize only the relevant fields for the user. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xpmars/mx-data) <br>
- [Meixiang financial data API endpoint](https://mkapi2.dfcfs.com/finskillshub/api/claw/query) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries or tables with optional JSON API response excerpts and curl command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided MX_APIKEY. Broad or long-range financial queries can return large responses, so users should provide specific securities, indicators, or time ranges.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
