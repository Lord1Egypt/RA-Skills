## Description:

Teach OpenClaw how to work in Feishu (Lark) group chats by recognizing senders, applying group and DM etiquette, preserving multi-user privacy, and formatting messages for the platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[4ier](https://clawhub.ai/user/4ier)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw administrators use this skill to configure Feishu group-chat and DM behavior, including sender identification, reply etiquette, privacy boundaries, and platform-specific text formatting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may persist a full Feishu contact directory, including names and open_ids, into agent prompt context.

Mitigation: Install only with administrator approval, treat the stored directory as personal data, keep USER.md private, and prefer restricted or allowlisted contact syncing.

Risk: Weekly automatic sync can repeatedly refresh directory data before scoping and retention policies are settled.

Mitigation: Avoid enabling the weekly cron until contact scope, data retention, and operational ownership are reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/4ier/skills/openclaw-feishu-group-chat)
- [ClawHub publisher profile](https://clawhub.ai/user/4ier)
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu contact user lookup API](https://open.feishu.cn/open-apis/contact/v3/users/find_by_department?department_id=0&page_size=50)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with inline shell commands and a Python helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent instructions and a USER.md contact table containing Feishu names and open_ids.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
