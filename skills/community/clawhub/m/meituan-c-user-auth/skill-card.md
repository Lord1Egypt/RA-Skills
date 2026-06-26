## Description: <br>
为需要美团用户身份的 Agent Skill 提供手机号验证码登录、Token 校验、账号切换和退出登录支持。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meituan-zhengchang](https://clawhub.ai/user/meituan-zhengchang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and downstream Meituan-related skills use this skill as a prerequisite authentication module to obtain and verify a user's Meituan login token before calling account-dependent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reusable Meituan account tokens and device identifiers are stored in local shared files. <br>
Mitigation: Treat mt_auth_tokens.json as sensitive credential storage, use an isolated workspace where possible, and clear persisted state with logout and clear-device-token when access is no longer needed. <br>
Risk: Downstream skills may receive the user's authentication token. <br>
Mitigation: Install and run this skill only with trusted downstream Meituan skills, and do not expose user_token or device_token in normal conversation output. <br>
Risk: Environment overrides for SKILL_CACHE_CLI_PATH or SKILL_CACHE_PYTHON can change which local code executes. <br>
Mitigation: Avoid untrusted environment values for those variables and review the resolved script paths before use in shared or automated environments. <br>
Risk: The artifact includes scheduled coupon automation behavior in addition to login authentication. <br>
Mitigation: Review cron-related commands and generated schedule configuration before enabling automated tasks. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/meituan-zhengchang/meituan-c-user-auth) <br>
- [EDS Claw SMS login API configuration](references/api-config.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown instructions with shell commands and JSON command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce authentication status, masked phone numbers, redirect URLs for security verification, and local token-management command results.] <br>

## Skill Version(s): <br>
1.0.8 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
