## Description:

调用海康云眸开放平台设备通道管理接口，包括查询设备下通道列表、同步设备下通道、修改通道名称和同步设备通道名称。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hik-cloud-open](https://clawhub.ai/user/hik-cloud-open)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to list, synchronize, rename, and synchronize names for Hik-Cloud device channels through the supported OpenAPI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential and token handling is broadly scoped enough that automatic installation is not appropriate for shared or production environments.

Mitigation: Review the skill before installation, protect or disable token caching where possible, avoid passing bearer tokens on the command line, and rotate credentials after any untrusted run.

Risk: A custom base URL could send credentials or bearer tokens to an untrusted endpoint.

Mitigation: Use only trusted HTTPS Hik-Cloud endpoints and rotate credentials if the skill has been run with an untrusted custom base URL.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hik-cloud-open/skills/hik-cloud-open-device-channel-management)
- [认证说明](artifact/references/auth.md)
- [设备通道管理文档摘要](artifact/references/device-channel-management.md)
- [设备通道管理](https://pic.hik-cloud.com/opencustom/apidoc/online/open/a5982b796d354b33b8b740ba3fb98c11.html)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text summaries or JSON command results, with Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and Hik-Cloud credentials through HIK_OPEN_CLIENT_ID and HIK_OPEN_CLIENT_SECRET; token values should not be exposed to users.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
