## Description: <br>
Call GET /api/v1/google/maps/posts for Google SERP Maps Posts through Just Serp API with data_id. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justserpapi](https://clawhub.ai/user/justserpapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve Google Maps business posts from Just Serp API for local business monitoring and promotion tracking. It requires a Google Maps location data_id and returns endpoint results for summary or raw JSON review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive Just Serp API key. <br>
Mitigation: Provide the key through JUST_SERP_API_KEY or the helper's --api-key argument only for intended tasks, and do not paste key values into chat messages, screenshots, or logs. <br>
Risk: API requests can fail because of invalid credentials, insufficient credits, quota limits, upstream errors, or network failures. <br>
Mitigation: Check the returned backend payload, status, and operationId before retrying or summarizing results. <br>


## Reference(s): <br>
- [Just Serp API project site](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_maps_posts&utm_content=project_link) <br>
- [Just Serp API documentation](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_maps_posts&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown summary with optional raw JSON from the API response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the mapsPosts operation on /api/v1/google/maps/posts and requires JUST_SERP_API_KEY plus a data_id query parameter.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
