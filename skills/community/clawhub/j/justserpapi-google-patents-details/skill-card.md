## Description: <br>
Call GET /api/v1/google/patents/details for Google SERP Patents Details through Just Serp API with patent_id. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justserpapi](https://clawhub.ai/user/justserpapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, patent researchers, and IP due diligence teams use this skill to retrieve Google Patents detail data, including abstracts, claims, and legal status, through Just Serp API for a specified patent_id. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Just Serp API key, which could be exposed if pasted into chat, screenshots, or logs. <br>
Mitigation: Provide the key only through the documented JUST_SERP_API_KEY environment variable and avoid sharing the key value in prompts or output. <br>
Risk: Patent lookup parameters are submitted to Just Serp API during endpoint execution. <br>
Mitigation: Submit only intended patent IDs and optional lookup parameters, and use the skill only when sharing those values with Just Serp API is acceptable. <br>
Risk: When requested, raw HTML or backend error payloads may be returned in the skill output. <br>
Mitigation: Review returned raw payloads before redistributing them and avoid including sensitive values in request parameters. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justserpapi/justserpapi-google-patents-details) <br>
- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_patents_details&utm_content=project_link) <br>
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_patents_details&utm_content=project_link) <br>
- [Generated Operations Reference](generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown summary with an inline shell command and raw JSON API response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY and patent_id; optional query parameters include language and html.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
