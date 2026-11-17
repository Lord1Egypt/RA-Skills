## Description:

Call GET /api/douyin-xingtu/get-kol-link-info/v1 for Douyin Creator Marketplace (Xingtu) Creator Link Metrics through JustOneAPI with kolId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and marketplace analysts use this skill to call a focused JustOneAPI endpoint for Douyin Creator Marketplace (Xingtu) creator link metrics. It supports creator evaluation, campaign planning, and marketplace research for a specified kolId.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required JustOneAPI token may be exposed through command-line arguments, process telemetry, shell logs, proxy logs, or API request logs.

Mitigation: Use a narrowly scoped, short-lived token when available; avoid shared machines and verbose telemetry; rotate the token if exposure is suspected.

## Reference(s):

- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_link_info&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_link_info&utm_content=project_link)
- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-xingtu-get-kol-link-info)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with a shell command example, endpoint-specific summary text, and raw JSON API response output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and the JUST_ONE_API_TOKEN environment variable; required lookup input is kolId, with optional industryTag and acceptCache query parameters.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
