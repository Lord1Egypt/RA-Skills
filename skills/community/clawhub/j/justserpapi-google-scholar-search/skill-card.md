## Description: <br>
Call GET /api/v1/google/scholar/search for Google SERP Scholar Search through Just Serp API with query. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justserpapi](https://clawhub.ai/user/justserpapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call Just Serp API's Google Scholar search endpoint for academic search results, citation filters, publication-year filters, patents, legal documents, versions, and cited-by links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Just Serp API key. <br>
Mitigation: Store the key in JUST_SERP_API_KEY and avoid exposing it in chats, screenshots, logs, or shared command history. <br>
Risk: Google Scholar search queries are sent to Just Serp API. <br>
Mitigation: Use the skill only when sending the query terms and filters to Just Serp API is acceptable for the intended workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justserpapi/justserpapi-google-scholar-search) <br>
- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_scholar_search&utm_content=project_link) <br>
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_scholar_search&utm_content=project_link) <br>
- [Just Serp API Base URL](https://api.justserpapi.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and API response summaries; raw JSON may be returned after a short summary.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the JUST_SERP_API_KEY environment variable and Node.js.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
