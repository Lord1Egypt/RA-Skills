## Description:

Call GET /api/douyin-xingtu/get-author-commerce-spread-info/v1 for Douyin Creator Marketplace (Xingtu) Author Commerce Spread Info through JustOneAPI with kolId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and commercial teams use this skill to query JustOneAPI for Douyin Creator Marketplace (Xingtu) author commerce spread metrics by KOL ID for creator evaluation, campaign planning, and media buying.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: JustOneAPI tokens may be exposed through command-line arguments or URL query logging.

Mitigation: Use environment-sourced tokens, avoid sharing command history or request logs, and prefer header-based authentication if the provider supports it.

Risk: A token with sensitive account access, billing impact, or broad quota can increase impact from misuse.

Mitigation: Review token scope, quota, billing exposure, and account permissions before installing or running the skill.

## Reference(s):

- [JustOneAPI API Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_author_commerce_spread_info&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_author_commerce_spread_info&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-xingtu-get-author-commerce-spread-info)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, json]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and JUST_ONE_API_TOKEN; the API call requires kolId and optionally accepts acceptCache.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
