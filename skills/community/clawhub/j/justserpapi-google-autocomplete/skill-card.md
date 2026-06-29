## Description: <br>
Call GET /api/v1/google/autocomplete for Google SERP Autocomplete through Just Serp API with query. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justserpapi](https://clawhub.ai/user/justserpapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SEO analysts, and marketing teams use this skill to call Just Serp API's Google autocomplete endpoint for keyword expansion and search intent research with optional country and language targeting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires JUST_SERP_API_KEY, which is a sensitive credential. <br>
Mitigation: Provide the key through the environment or the helper's API key argument, and avoid sharing key values in chat messages, screenshots, or logs. <br>
Risk: Search queries are sent to Just Serp API and may be subject to that service's terms, quotas, and billing limits. <br>
Mitigation: Use the skill only for intended Just Serp API workflows, review the service terms and billing limits before deployment, and keep user-provided keywords and targeting filters unchanged. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justserpapi/justserpapi-google-autocomplete) <br>
- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_autocomplete&utm_content=project_link) <br>
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_autocomplete&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown summary followed by raw JSON from the Just Serp API response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY; accepts a required query and optional country and language query parameters.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
