## Description:

Call GET /api/weibo/get-fans/v1 for Weibo User Fans through JustOneAPI with uid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call JustOneAPI's Weibo fans endpoint for a given UID. It supports audience analysis and influencer research by summarizing returned fan profile metadata and verification signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the JustOneAPI token and target Weibo UID to api.justoneapi.com.

Mitigation: Use a narrowly scoped or disposable token when available, confirm the lookup target before execution, and install only when that data transfer is acceptable.

Risk: Token values may be exposed if pasted into chat, screenshots, shell history, or command logs.

Mitigation: Pass the token through JUST_ONE_API_TOKEN, avoid sharing token values, and rotate the token if logs may have captured it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-weibo-get-fans)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_get_fans&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_get_fans&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown summary with optional raw JSON result and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and a Weibo uid; optional page defaults to 1.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
