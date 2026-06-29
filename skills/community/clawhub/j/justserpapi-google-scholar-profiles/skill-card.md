## Description: <br>
Call GET /api/v1/google/scholar/profiles for Google SERP Scholar Profiles through Just Serp API with mauthors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justserpapi](https://clawhub.ai/user/justserpapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query Just Serp API for Google Scholar profile search results, affiliations, citation counts, and pagination tokens. It supports researcher discovery and academic directory building workflows that need the required mauthors query parameter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Just Serp API key and sends it to the Just Serp API provider. <br>
Mitigation: Keep JUST_SERP_API_KEY in the environment, pass it through the documented command flag, and do not paste the key into chat messages, screenshots, or logs. <br>
Risk: Scholar profile search queries are sent to Just Serp API. <br>
Mitigation: Install and use the skill only when the workflow is intended to use Just Serp API and the query terms are appropriate to share with that provider. <br>
Risk: Backend error payloads may be surfaced when a request fails. <br>
Mitigation: Review backend payloads before sharing transcripts or logs outside the trusted workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justserpapi/justserpapi-google-scholar-profiles) <br>
- [Just Serp API project site](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_scholar_profiles&utm_content=project_link) <br>
- [Just Serp API docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_scholar_profiles&utm_content=project_link) <br>
- [Generated operation reference](artifact/generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the ScholarProfiles operation for GET /api/v1/google/scholar/profiles and requires JUST_SERP_API_KEY plus a mauthors query value.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
