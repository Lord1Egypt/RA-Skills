## Description: <br>
Call GET /api/v1/google/videos/search for Google SERP Videos Search through Just Serp API with query. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justserpapi](https://clawhub.ai/user/justserpapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and SEO teams use this skill to call Just Serp API's Google Videos Search endpoint for query-based video result data, including titles, sources, dates, and localization filters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Google video search queries and optional localization filters are sent to Just Serp API under the user's account. <br>
Mitigation: Use the skill only when that data sharing is acceptable, and avoid entering sensitive personal, business, or investigative search terms. <br>
Risk: The skill requires a sensitive JUST_SERP_API_KEY credential. <br>
Mitigation: Keep the API key in the environment, pass it with --api-key, and avoid exposing key values in chat messages, screenshots, or logs. <br>


## Reference(s): <br>
- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_videos_search&utm_content=project_link) <br>
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_videos_search&utm_content=project_link) <br>
- [Just Serp API Base URL](https://api.justserpapi.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/justserpapi/justserpapi-google-videos-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY and Node.js; sends query and optional localization filters to Just Serp API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
