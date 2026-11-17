## Description:

Call GET /api/xiaohongshu-pgy/get-kol-fans-portrait/v1 for Xiaohongshu Creator Marketplace (Pugongying) Follower Distribution through JustOneAPI with kolId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to call JustOneAPI for Xiaohongshu Creator Marketplace follower distribution data by KOL ID. It supports creator evaluation, campaign planning, and creator benchmarking workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token may be exposed through process arguments or URL query logs.

Mitigation: Use a narrowly scoped token, avoid shared systems where command-line arguments are monitored, and rotate the token if it may have appeared in process or URL logs.

Risk: The skill sends the JustOneAPI token and kolId to api.justoneapi.com.

Mitigation: Install and run the skill only when that data sharing is acceptable for the intended workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-xiaohongshu-pgy-get-kol-fans-portrait)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_get_kol_fans_portrait&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_get_kol_fans_portrait&utm_content=project_link)
- [Operations reference](artifact/generated/operations.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, JUST_ONE_API_TOKEN, and a kolId query parameter; backend errors include the backend payload and operation ID.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
