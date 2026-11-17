## Description:

调用海康云眸开放平台设备报警能力管理接口，包括获取常规报警能力列表、修改报警能力状态和设置智能检测开关。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hik-cloud-open](https://clawhub.ai/user/hik-cloud-open)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to query Hik-Cloud device alarm capabilities, update channel alarm ability status, and control supported intelligence detection switches without manually handling token acquisition.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change live Hik-Cloud alarm monitoring and intelligence detection settings.

Mitigation: Review target device serials, channel IDs, ability codes, status values, and enable/type settings before running update commands in production.

Risk: Hik-Cloud credentials and access tokens are required, and token-cache safeguards are weak.

Mitigation: Inject credentials through the agent environment, avoid passing tokens on the command line, and restrict or disable the token cache when local persistence is not acceptable.

Risk: Custom base URLs can redirect authentication and business API calls away from the default Hik-Cloud endpoint.

Mitigation: Use the default HTTPS endpoint unless a controlled, trusted Hik-Cloud endpoint is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hik-cloud-open/skills/hik-cloud-open-device-alarm-capability-management)
- [设备报警能力管理文档摘要](references/device-alarm-capability-management.md)
- [认证说明](references/auth.md)
- [Hik-Cloud device alarm capability API documentation](https://pic.hik-cloud.com/opencustom/apidoc/online/open/f8cbf864c4ca4395909dad225902a6ee.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON or text command output from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live Hik-Cloud API response fields such as code, message, data, success, abilityCode, status, channelId, deviceSerial, enable, and type.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
