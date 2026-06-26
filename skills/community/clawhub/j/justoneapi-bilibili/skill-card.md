## Description: <br>
Analyze Bilibili workflows with JustOneAPI, including video Details, user Published Videos, and user Profile across 9 operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to answer Bilibili video, creator, comment, caption, search, and share-link questions through JustOneAPI-backed read-only operations. It is best suited when the user can provide Bilibili identifiers such as bvid, aid, cid, uid, page, or search keywords. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a JustOneAPI token and the token could be exposed through chat, logs, screenshots, command lines, or request URLs. <br>
Mitigation: Use a dedicated low-privilege token, avoid pasting or logging it, and rotate the token if exposure is suspected. <br>
Risk: Returned Bilibili profiles, comments, danmaku, and captions may contain personal or user-generated content. <br>
Mitigation: Handle retrieved content as potentially sensitive user-generated data and share only the fields needed for the user's task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-bilibili) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili&utm_content=project_link) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili&utm_content=project_link) <br>
- [Bilibili operations](artifact/generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown answer with selected endpoint fields and optional raw JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and user-supplied Bilibili identifiers or filters.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
