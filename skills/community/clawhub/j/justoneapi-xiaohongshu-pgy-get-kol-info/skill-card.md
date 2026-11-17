## Description:

Call GET /api/xiaohongshu-pgy/get-kol-info/v1 for Xiaohongshu Creator Marketplace (Pugongying) Creator Profile through JustOneAPI with kolId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to look up Xiaohongshu Creator Marketplace (Pugongying) creator profile data by KOL ID for influencer vetting, benchmark analysis, and campaign planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token can be exposed through process arguments or request URLs.

Mitigation: Run the skill only where process command lines and request URLs are not logged or visible to other users, and rotate the token if it was used in a monitored environment.

Risk: The token may carry billing, quota, or sensitive data access.

Mitigation: Use a narrowly scoped and revocable token when available, and review account permissions before installation or execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-xiaohongshu-pgy-get-kol-info)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_get_kol_info&utm_content=project_link)
- [Endpoint Operations](generated/operations.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The endpoint returns creator profile data for the requested kolId; backend errors include status details and operation ID.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
