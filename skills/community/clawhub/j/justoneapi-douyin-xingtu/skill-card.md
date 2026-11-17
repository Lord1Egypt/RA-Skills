## Description:

Analyze Douyin Creator Marketplace (Xingtu) workflows with JustOneAPI, including creator Profile, creator Link Structure, and creator Visibility Status across 46 operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and marketers use this skill to query JustOneAPI for Douyin Creator Marketplace (Xingtu) creator profile, link structure, visibility, channel, audience, and campaign planning data. It helps agents select a narrow GET operation, request missing identifiers or filters, and return decision-relevant fields before raw JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required JustOneAPI token may be exposed through command lines or request URLs that are logged by the host environment.

Mitigation: Use a scoped, revocable token, avoid shared or heavily monitored hosts, limit log retention, and rotate the token if it may have appeared in logs.

Risk: The skill issues authenticated API requests across 46 operations, so choosing an overly broad or wrong operation can return irrelevant creator or campaign data.

Mitigation: Review the generated operations, choose the smallest matching operation, ask for missing required parameters, and echo user-supplied filters in the answer.

## Reference(s):

- [Generated Douyin Creator Marketplace (Xingtu) Operations](generated/operations.md)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu&utm_content=project_link)
- [ClawHub Skill Listing](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-xingtu)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with operation IDs, selected fields, and optional JSON response excerpts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a JUST_ONE_API_TOKEN for authenticated JustOneAPI requests.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
