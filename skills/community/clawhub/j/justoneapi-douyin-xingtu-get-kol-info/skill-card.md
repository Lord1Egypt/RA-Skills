## Description:

Call GET /api/douyin-xingtu/get-kol-info/v1 for Douyin Creator Marketplace (Xingtu) Creator Profile through JustOneAPI with kolId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and marketing operations teams use this skill to look up Douyin Creator Marketplace creator profile data by kolId for influencer vetting, benchmark analysis, and campaign planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends kolId lookups and the JustOneAPI token to api.justoneapi.com.

Mitigation: Use the skill only when that data transfer is acceptable for the workflow and account.

Risk: Tokens or request URLs may appear in command lines, logs, screenshots, or telemetry.

Mitigation: Use a least-privileged token with quotas or expiration when available, avoid sharing logs that include command lines or request URLs, and rotate the token if exposure is suspected.

## Reference(s):

- [JustOneAPI API homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_info&utm_content=project_link)
- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-xingtu-get-kol-info)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands and endpoint JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses kolId as the required creator lookup parameter and may include platformChannel and acceptCache query options.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
