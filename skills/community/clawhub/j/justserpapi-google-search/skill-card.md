## Description: <br>
Call GET /api/v1/google/search for Google SERP Search through Just Serp API with query. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justserpapi](https://clawhub.ai/user/justserpapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and search analysts use this skill to call Just Serp API's Google SERP search endpoint for keyword tracking, SERP analysis, and localized result inspection. It requires a Just Serp API key and a search query, with optional localization and filtering parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, optional localization fields, and the Just Serp API key are sent to Just Serp API. <br>
Mitigation: Use the skill only when that disclosure is acceptable, keep the key in JUST_SERP_API_KEY, and avoid pasting key values into chat, screenshots, or logs. <br>
Risk: Queries involving secrets, private investigations, regulated data, or precise locations may expose sensitive context to an external API. <br>
Mitigation: Do not use the skill for those searches unless the disclosure has been approved; omit precise localization parameters when they are not needed. <br>
Risk: The optional html parameter can request raw Google results HTML alongside structured data. <br>
Mitigation: Prefer structured results unless raw HTML is required, and review or sanitize returned content before sharing it outside the intended workflow. <br>


## Reference(s): <br>
- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_search&utm_content=project_link) <br>
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_search&utm_content=project_link) <br>
- [ClawHub Skill Page](https://clawhub.ai/justserpapi/justserpapi-google-search) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with optional raw JSON from the Just Serp API response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses operation search on GET /api/v1/google/search; required query parameter plus optional localization, filtering, paging, and raw HTML controls.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
