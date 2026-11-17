## Description:

Call GET /api/douyin-xingtu/get-kol-audience-distribution/v1 for Douyin Creator Marketplace (Xingtu) Audience Distribution through JustOneAPI with kolId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and marketing analysts use this skill to call JustOneAPI's Douyin Creator Marketplace (Xingtu) audience distribution endpoint for a specified KOL ID. It supports creator evaluation, campaign planning, and marketplace research by summarizing demographic and interest-based audience segmentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token can be exposed through process arguments, shell history, URL query logging, proxy logs, telemetry, or error reports.

Mitigation: Use a short-lived, least-privileged token, avoid verbose command logging, and rotate the token if it may have appeared in logs, shell history, telemetry, or reports.

Risk: Backend error handling may surface service payloads while troubleshooting failed API calls.

Mitigation: Review and redact any returned payloads or logs before sharing them outside the operational context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-xingtu-get-kol-audience-distribution)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_audience_distribution&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_audience_distribution&utm_content=project_link)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summary with raw JSON payloads and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and JUST_ONE_API_TOKEN; endpoint requires kolId and optionally accepts acceptCache.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
