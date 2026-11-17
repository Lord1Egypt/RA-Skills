## Description:

Call GET /api/douyin-xingtu/get-kol-marketing-info/v1 for Douyin Creator Marketplace (Xingtu) Marketing Metrics through JustOneAPI with kolId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and marketing operations users use this skill to retrieve Douyin Creator Marketplace (Xingtu) marketing metrics for a specific creator KOL ID. It supports creator evaluation, campaign planning, and marketplace research through the JustOneAPI endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token can be exposed through process arguments or full request URLs.

Mitigation: Use a short-lived, scoped token when possible, avoid environments that log command lines or full URLs, and rotate the token if exposure is suspected.

Risk: The endpoint can return creator or commercial service data that may be sensitive.

Mitigation: Call the endpoint only for authorized creator research or campaign planning, and avoid sharing raw response payloads in chat, screenshots, or logs unless necessary.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-xingtu-get-kol-marketing-info)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_marketing_info&utm_content=project_link)
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_marketing_info&utm_content=project_link)
- [Generated operation reference](artifact/generated/operations.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the getKolMarketingInfoV1 operation with required kolId and optional platformChannel and acceptCache query parameters.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
