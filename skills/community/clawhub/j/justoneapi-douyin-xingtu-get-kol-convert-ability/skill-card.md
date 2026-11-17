## Description:

Call GET /api/douyin-xingtu/get-kol-convert-ability/v1 for Douyin Creator Marketplace (Xingtu) Conversion Analysis through JustOneAPI with kolId and range.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to call JustOneAPI for Douyin Creator Marketplace conversion analysis by KOL ID and time range. It supports creator evaluation, campaign planning, commercial performance review, and marketplace research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI credential is sent as a URL query parameter, which can expose the token through request URLs, logs, screenshots, or telemetry.

Mitigation: Use a narrowly scoped or disposable token when available, avoid logging full request URLs, and rotate the token if it may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-xingtu-get-kol-convert-ability)
- [JustOneAPI API homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_convert_ability&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_convert_ability&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with a Node.js command and JSON API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN, kolId, and range; the helper prints formatted JSON returned by the provider endpoint.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
