## Description: <br>
Analyze TikTok workflows with JustOneAPI, including user Published Posts, post Details, and user Profile across 7 operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external users use this skill to retrieve TikTok profile, post, comment, reply, and search data from JustOneAPI when they have the required identifiers and API token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token can authorize TikTok lookup requests if exposed in chat, logs, screenshots, or request URLs. <br>
Mitigation: Keep JUST_ONE_API_TOKEN private, avoid pasting it into conversations or screenshots, and redact request URLs and logs before sharing. <br>
Risk: Returned TikTok profile, comment, reply, and search data may be misused outside authorized or policy-compliant analysis. <br>
Mitigation: Use returned data only for authorized analysis and apply the user's stated identifiers or filters so the scope remains explicit. <br>


## Reference(s): <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok&utm_content=project_link) <br>
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok&utm_content=project_link) <br>
- [Generated TikTok Operations](generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown answer with optional shell command and JSON API payload excerpts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and operation-specific TikTok identifiers such as awemeId, postId, uniqueId, secUid, commentId, keyword, or cursor.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
