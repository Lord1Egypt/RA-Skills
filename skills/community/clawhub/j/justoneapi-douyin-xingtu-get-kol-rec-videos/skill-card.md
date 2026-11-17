## Description:

Call GET /api/douyin-xingtu/get-kol-rec-videos/v1 for Douyin Creator Marketplace (Xingtu) Recommended Videos through JustOneAPI with kolId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query JustOneAPI for Douyin Creator Marketplace (Xingtu) recommended video data by KOL ID, supporting creator evaluation, campaign planning, and marketplace research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token can be exposed through command arguments, process listings, logs, or query URLs.

Mitigation: Use a narrowly scoped or short-lived token when available, avoid shared process-monitoring environments, keep tokens out of chat and logs, and rotate the token if exposure is suspected.

Risk: The skill sends KOL lookup parameters to a third-party API endpoint.

Mitigation: Use the skill only where sending the requested Douyin Xingtu lookup data to JustOneAPI is acceptable under the user's policy and data-handling requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-xingtu-get-kol-rec-videos)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_rec_videos&utm_content=project_link)
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_rec_videos&utm_content=project_link)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command examples and endpoint JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JustOneAPI token and a kolId query parameter; acceptCache is optional.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
