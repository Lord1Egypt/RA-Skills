## Description:

Call GET /api/douyin/share-url-transfer/v1 for Douyin (TikTok China) Share Link Resolution through JustOneAPI with shareUrl.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to resolve a Douyin short share URL through JustOneAPI and retrieve canonical IDs or related data for downstream video and comment workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token can be exposed through command-line process listings or URL/query logs.

Mitigation: Use a tightly scoped, revocable token; avoid long-lived or billing-privileged tokens; redact command, URL, and process logs.

Risk: Authentication is passed as an API query parameter for this endpoint.

Mitigation: Prefer a release that reads the token from the environment internally and sends authentication in a header where the service supports it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-share-url-transfer)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_share_url_transfer&utm_content=project_link)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, JSON, Guidance]

**Output Format:** [Markdown summary with raw JSON response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and a shareUrl query parameter; no request body is documented.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
