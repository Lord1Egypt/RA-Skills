## Description: <br>
Call GET /api/douyin/share-url-transfer/v1 for Douyin (TikTok China) Share Link Resolution through JustOneAPI with shareUrl. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to resolve a Douyin share URL through JustOneAPI and retrieve canonical data that can support downstream video or comment workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token and submitted Douyin share links are sent to the third-party API provider, and the security summary notes that the token is sent in the URL query string. <br>
Mitigation: Install only if you trust JustOneAPI with these values, avoid sharing logs or traces that may contain full request URLs, and prefer a header-based token option if the provider supports one. <br>


## Reference(s): <br>
- [JustOneAPI API Homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_share_url_transfer&utm_content=project_link) <br>
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_share_url_transfer&utm_content=project_link) <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-douyin-share-url-transfer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JustOneAPI token and a Douyin shareUrl.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
