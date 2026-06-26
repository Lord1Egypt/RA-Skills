## Description: <br>
Call GET /api/youku/get-user-detail/v1 for YOUKU User Profile through JustOneAPI with uid. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to look up a YOUKU user profile by uid through JustOneAPI. It supports fetching profile basics such as user ID, username, avatar, audience size, account growth, and verification status for authorized social CRM or creator analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API token exposure through command arguments or shared runtime environments. <br>
Mitigation: Use a dedicated, revocable JustOneAPI token with limited privileges where available, and avoid running the helper on shared systems where process arguments may be visible. <br>
Risk: Unauthorized or excessive collection of YOUKU profile data. <br>
Mitigation: Use the skill only for authorized profile lookups needed for this endpoint, and avoid bulk profiling or collection outside the approved workflow. <br>
Risk: The skill depends on a third-party API and returns backend payloads directly on errors. <br>
Mitigation: Review backend responses before sharing them and avoid including secrets, private profile data, or unnecessary identifiers in logs or chat transcripts. <br>


## Reference(s): <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_youku_get_user_detail&utm_content=project_link) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_youku_get_user_detail&utm_content=project_link) <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-youku-get-user-detail) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Short Markdown summary followed by raw JSON when results are available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and a uid query parameter; reports backend errors with the operation ID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
