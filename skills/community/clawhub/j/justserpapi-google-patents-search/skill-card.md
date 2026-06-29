## Description: <br>
Call GET /api/v1/google/patents/search for Google SERP Patents Search through Just Serp API with query. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justserpapi](https://clawhub.ai/user/justserpapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and patent researchers use this skill to query Google patent search data through Just Serp API, including filters for patent discovery and portfolio monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Patent search queries, filters, and API key use are sent to Just Serp API. <br>
Mitigation: Use only intended search terms and filters, avoid unrelated private data, and pass JUST_SERP_API_KEY through the environment or CLI rather than chat messages or logs. <br>
Risk: Authenticated requests can fail because of invalid credentials, insufficient credits, quota limits, or upstream service errors. <br>
Mitigation: Surface the returned status, payload, and operation ID, then verify the API key and account quota before retrying. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justserpapi/justserpapi-google-patents-search) <br>
- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_patents_search&utm_content=project_link) <br>
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_patents_search&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY; preserves user-provided query and filter parameters; summarizes results before raw JSON.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
