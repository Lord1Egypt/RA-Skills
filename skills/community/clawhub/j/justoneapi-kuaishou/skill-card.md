## Description:

Analyze Kuaishou workflows with JustOneAPI, including user Search, user Published Videos, and video Details across 7 operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to query Kuaishou user, video, comment, and share-link endpoints through JustOneAPI when they need API-backed creator research, content monitoring, or video analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token can be exposed through process arguments or request URLs.

Mitigation: Use a limited-scope, low-quota token, avoid logging full commands or request URLs, and rotate the token if it may have appeared in shell history, process telemetry, or API logs.

Risk: Kuaishou query parameters and the JustOneAPI token are sent to api.justoneapi.com.

Mitigation: Install and run the skill only when that data flow is acceptable, and provide only the identifiers or filters needed for the selected operation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-kuaishou)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou&utm_content=project_link)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Shell commands, Guidance]

**Output Format:** [Markdown with summarized API results and selected JSON payload fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and operation-specific Kuaishou parameters such as keyword, page, pcursor, userId, videoId, or shareUrl.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
