## Description: <br>
Call GET /api/v1/google/trends/autocomplete for Google SERP Trends Autocomplete through Just Serp API with query. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justserpapi](https://clawhub.ai/user/justserpapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to call Just Serp API for Google Trends autocomplete suggestions, including topic IDs for trend discovery and topic expansion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Just Serp API key and sends it to api.justserpapi.com for authenticated requests. <br>
Mitigation: Provide the key through JUST_SERP_API_KEY or the documented command argument, and avoid pasting key values into chat, screenshots, or logs. <br>
Risk: Autocomplete queries are sent to Just Serp API and may reveal search intent or topic research interests. <br>
Mitigation: Use the skill only when sending those query terms to Just Serp API is acceptable for the user's workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justserpapi/justserpapi-google-trends-autocomplete) <br>
- [Just Serp API homepage](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_trends_autocomplete&utm_content=project_link) <br>
- [Just Serp API documentation](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_trends_autocomplete&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, JSON] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON API response payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Just Serp API key supplied through JUST_SERP_API_KEY or the helper command's api-key argument.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
