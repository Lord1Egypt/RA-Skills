## Description:

Call GET /api/xiaohongshu-pgy/get-kol-cost-effective/v1 for Xiaohongshu Creator Marketplace (Pugongying) Cost Effectiveness Analysis through JustOneAPI with kolId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query JustOneAPI for Xiaohongshu Creator Marketplace (Pugongying) KOL cost effectiveness data, including pricing, reach, and engagement efficiency indicators for campaign evaluation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a JustOneAPI token in requests, and evidence.security warns that tokens could leak through command, URL, or request logs.

Mitigation: Use short-lived or restricted tokens where available, avoid environments that log process arguments or full URLs, and rotate the token if logs may have captured it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-xiaohongshu-pgy-get-kol-cost-effective)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_get_kol_cost_effective&utm_content=project_link)
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_get_kol_cost_effective&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown summary followed by raw JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and a kolId query parameter.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
