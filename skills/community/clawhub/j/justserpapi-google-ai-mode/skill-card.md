## Description: <br>
Google SERP Ai Mode API helps an agent call Just Serp API's Google AI Mode endpoint for a query and summarize the returned generated answers, follow-up prompts, cited links, and related response data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justserpapi](https://clawhub.ai/user/justserpapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Use this skill when an agent needs to retrieve Google AI Mode search data through Just Serp API, using the required query parameter and optional localization, SafeSearch, UULE, and raw HTML options. <br>

### Deployment Geography for Use: <br>
Global, subject to Just Serp API availability and the user's selected Google localization parameters. <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Just Serp API key. <br>
Mitigation: Store JUST_SERP_API_KEY in an environment variable, pass it only to the local helper, and avoid sharing key values in chat, screenshots, or logs. <br>
Risk: User-supplied search queries and localization parameters are sent to an external API. <br>
Mitigation: Review query text and filters before execution, especially when they may contain sensitive or regulated information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justserpapi/justserpapi-google-ai-mode) <br>
- [Just Serp API homepage](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_ai_mode&utm_content=project_link) <br>
- [Just Serp API docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_ai_mode&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [An endpoint-specific summary followed by raw JSON from the Just Serp API response when requested or useful.] <br>
**Output Parameters:** [Requires operation aiMode, JUST_SERP_API_KEY, and params-json with query; optional parameters include html, country, uule, location, and safe.] <br>
**Other Properties Related to Output:** [Calls GET /api/v1/google/ai-mode with query parameters and no request body; backend errors should include the operation ID and returned payload.] <br>

## Skill Version(s): <br>
1.0.1 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
