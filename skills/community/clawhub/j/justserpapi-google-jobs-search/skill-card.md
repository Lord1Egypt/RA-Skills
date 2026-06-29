## Description: <br>
Call GET /api/v1/google/jobs/search for Google SERP Jobs Search through Just Serp API with query. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justserpapi](https://clawhub.ai/user/justserpapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query Just Serp API's Google Jobs search endpoint for job titles, companies, locations, hiring trends, and recruitment monitoring workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a Just Serp API key. <br>
Mitigation: Provide the key through JUST_SERP_API_KEY or the helper's api-key argument, and do not paste key values into chat messages, screenshots, or logs. <br>
Risk: Job search terms, localization settings, location filters, and pagination tokens are sent to Just Serp API. <br>
Mitigation: Review inputs before use and avoid submitting sensitive or confidential search terms unless that disclosure is acceptable. <br>
Risk: API usage may consume credits or quota. <br>
Mitigation: Monitor Just Serp API usage and quota costs when running repeated searches or paginated requests. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justserpapi/justserpapi-google-jobs-search) <br>
- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_jobs_search&utm_content=project_link) <br>
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_jobs_search&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with optional raw JSON response data and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY and Node.js; sends job search parameters to Just Serp API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
