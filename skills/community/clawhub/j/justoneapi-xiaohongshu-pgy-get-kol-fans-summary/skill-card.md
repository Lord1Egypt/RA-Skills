## Description:

Call GET /api/xiaohongshu-pgy/get-kol-fans-summary/v1 for Xiaohongshu Creator Marketplace (Pugongying) Follower Summary through JustOneAPI with kolId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and creator-analytics teams use this skill to call JustOneAPI's Xiaohongshu Creator Marketplace (Pugongying) follower-summary endpoint for a specified KOL ID, then summarize metrics and return raw JSON for creator evaluation, campaign planning, and benchmarking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends a JustOneAPI token and KOL ID to api.justoneapi.com.

Mitigation: Install only if you trust JustOneAPI, use a narrowly scoped token where possible, avoid logging full commands or URLs, and rotate the token if command history, process telemetry, or request logs may have exposed it.

## Reference(s):

- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_get_kol_fans_summary&utm_content=project_link)
- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-xiaohongshu-pgy-get-kol-fans-summary)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summary followed by raw JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and kolId; optional acceptCache query parameter defaults to false.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
