## Description: <br>
Call GET /api/xiaohongshu/share-url-transfer/v1 for Xiaohongshu (RedNote) Share Link Resolution through JustOneAPI with shareUrl. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to resolve Xiaohongshu (RedNote) share links through JustOneAPI, including extracting note IDs for downstream note and comment workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Access tokens may be exposed through command-line arguments or request URLs. <br>
Mitigation: Use environment variables or a secret store where possible, avoid logging commands or URLs that contain tokens, and rotate the token if exposure is suspected. <br>
Risk: RedNote share URLs are sent to JustOneAPI for resolution. <br>
Mitigation: Use the skill only for share URLs that are permitted to be sent to JustOneAPI under the user's data handling requirements. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-xiaohongshu-share-url-transfer) <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_share_url_transfer&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Endpoint-specific summary followed by raw JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and a shareUrl query parameter; backend errors should include the backend payload and operation ID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
