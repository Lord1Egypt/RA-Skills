## Description:

美团C端用户Agent认证工具为需要美团用户身份的 Skill 提供手机号短信验证码登录、Token 管理和前置认证支持。

This skill is ready for commercial/non-commercial use.

## Publisher:

[meituan-zhengchang](https://clawhub.ai/user/meituan-zhengchang)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and skills that need a Meituan C-side user session use this skill to guide SMS login, verify user tokens, and pass an authenticated user_token to downstream Meituan workflows such as coupon or order-related skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Meituan account credentials and reusable session tokens.

Mitigation: Install only from a trusted publisher, avoid shared or logged environments, and do not display user_token, device_token, phone numbers, or SMS codes except where required for authentication.

Risk: Security evidence flags under-disclosed scheduled coupon automation.

Mitigation: Review or remove cron coupon commands before allowing agent-driven execution, and require explicit user consent before any recurring task is enabled.

Risk: Security evidence flags unsafe local cache file access around authentication data.

Mitigation: Harden cache CLI path handling, keep token storage in a user-controlled workspace, and maintain restrictive local file permissions.

## Reference(s):

- [EDS Claw SMS Login API Configuration](references/api-config.md)
- [ClawHub Skill Page](https://clawhub.ai/meituan-zhengchang/skills/meituan-c-user-auth)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or consume sensitive authentication values including phone numbers, SMS codes, user_token, and device_token.]

## Skill Version(s):

1.0.8 (source: server release metadata; artifact frontmatter reports 1.0.14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
