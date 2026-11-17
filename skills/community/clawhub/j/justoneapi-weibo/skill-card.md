## Description:

Track Weibo hot search boards, keyword results, creator profiles, fan or follower graphs, and post or video detail endpoints through JustOneAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Newsroom, research, and monitoring users use this skill to check Weibo trends, search posts by time window, review creator profiles and timelines, and inspect fan or follower graphs through JustOneAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token may be exposed through command lines or request URLs.

Mitigation: Use a scoped, revocable token, avoid environments that log process arguments or full URLs, and rotate the token if it may have appeared in logs or telemetry.

Risk: Weibo queries and identifiers are sent to api.justoneapi.com.

Mitigation: Install and use the skill only when sending those queries and the JustOneAPI token to api.justoneapi.com is acceptable for the intended workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-weibo)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo&utm_content=project_link)
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with API result summaries and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Weibo filters, operation IDs, engagement counts, author context, media references, and backend error payloads when relevant.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
