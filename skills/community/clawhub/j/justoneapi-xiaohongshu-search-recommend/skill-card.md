## Description:

Helps agents query JustOneAPI's Xiaohongshu (RedNote) keyword suggestions endpoint using a keyword.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve Xiaohongshu (RedNote) suggested queries, keyword variants, and related metadata for content research, SEO, pSEO, and search coverage workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API tokens may be exposed through command lines or logged URLs.

Mitigation: Use a dedicated low-privilege JustOneAPI token, redact `--token` and `token=` values from logs, and rotate any token that may already have been logged.

Risk: Paid quota, broad account access, or long-lived credentials increase the impact of token exposure.

Mitigation: Review the skill before installing and avoid using high-privilege or long-lived tokens.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-xiaohongshu-search-recommend)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_search_recommend&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_search_recommend&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown summary with raw JSON response payload when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JustOneAPI token and a keyword query parameter.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
