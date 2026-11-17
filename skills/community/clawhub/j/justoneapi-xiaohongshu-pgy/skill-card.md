## Description:

Analyze Xiaohongshu Creator Marketplace (Pugongying) workflows with JustOneAPI, including creator Profile, data Summary, and follower Growth History across 24 operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call JustOneAPI endpoints for Xiaohongshu Creator Marketplace creator discovery, profile review, follower analytics, engagement summaries, note details, and campaign planning workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles the JustOneAPI token in URLs and command arguments.

Mitigation: Use a scoped or short-lived token when available, avoid environments that log command arguments or full URLs, and rotate the token if it may have been exposed.

Risk: API responses depend on authenticated JustOneAPI Xiaohongshu/Pugongying data and caller-supplied identifiers or filters.

Mitigation: Confirm required parameters before execution and review returned fields before using them for creator vetting, benchmarking, or campaign decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-xiaohongshu-pgy)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy&utm_content=project_link)
- [Generated Operations Documentation](artifact/generated/operations.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with endpoint-specific JSON results and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and node; API responses come from JustOneAPI GET operations.]

## Skill Version(s):

1.0.4 (source: server release evidence, created 2026-04-23)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
