## Description: <br>
Call GET /api/xiaohongshu-pgy/get-kol-data-summary/v2 for Xiaohongshu Creator Marketplace (Pugongying) Data Summary through JustOneAPI with business and kolId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operators use this skill to call JustOneAPI's Xiaohongshu Creator Marketplace data summary endpoint for a specific KOL and business type. It helps summarize activity, engagement, and audience growth signals for creator evaluation, campaign planning, and creator benchmarking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The API token can be exposed through command-line arguments and query-string request URLs. <br>
Mitigation: Use a limited-scope JUST_ONE_API_TOKEN where possible, avoid sharing logs or screenshots that include commands or request URLs, and run only where local users or diagnostics cannot capture process arguments. <br>
Risk: The skill calls a third-party JustOneAPI endpoint and returns external creator-marketplace data for evaluation and planning. <br>
Mitigation: Review returned JSON and any summaries before relying on them for campaign decisions, and preserve backend error payloads with the operation ID for troubleshooting. <br>


## Reference(s): <br>
- [JustOneAPI API Homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_get_kol_data_summary&utm_content=project_link) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_get_kol_data_summary&utm_content=project_link) <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-xiaohongshu-pgy-get-kol-data-summary) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown summary with an optional shell command and raw JSON response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [States the operation ID and endpoint path, echoes business and kolId, summarizes relevant fields, and includes backend error payloads when requests fail.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
