## Description: <br>
Call GET /api/kuaishou/share-url-transfer/v1 for Kuaishou Share Link Resolution through JustOneAPI with shareUrl. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to resolve Kuaishou share links through JustOneAPI and retrieve the resolved content identifier and target object data for automated content processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the JustOneAPI token as a URL query parameter, which may expose the token through URLs, logs, telemetry, or shared error output. <br>
Mitigation: Use a revocable token, avoid sharing command output or URLs that may contain the token, prefer a release that sends credentials in an Authorization or API-key header, and rotate the token if exposure is possible. <br>


## Reference(s): <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou_share_url_transfer&utm_content=project_link) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou_share_url_transfer&utm_content=project_link) <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-kuaishou-share-url-transfer) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown summary followed by raw JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and a Kuaishou shareUrl query parameter.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
