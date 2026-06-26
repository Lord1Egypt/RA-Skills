## Description: <br>
Analyze YOUKU workflows with JustOneAPI, including video Search, video Details, and user Profile. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to run API-backed YOUKU video searches, retrieve video details, and inspect user profiles through JustOneAPI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a JUST_ONE_API_TOKEN for authenticated JustOneAPI requests. <br>
Mitigation: Use a limited or dedicated token when available, keep it out of chat messages and logs, and rotate it if exposure is possible. <br>
Risk: YOUKU lookup inputs such as search terms, user IDs, and video IDs are sent to JustOneAPI. <br>
Mitigation: Avoid confidential search terms or identifiers and use the skill only when sharing those lookup inputs with JustOneAPI is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-youku) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_youku&utm_content=project_link) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_youku&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown answer with selected JSON API results and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and operation parameters such as keyword, page, uid, or videoId.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
