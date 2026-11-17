## Description:

调用海康云眸开放平台设备分组管理接口，包括新增组、删除组、更新组、查询组织详情、查询所有组织、查询下级组和设备转移分组。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hik-cloud-open](https://clawhub.ai/user/hik-cloud-open)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage Hik-Cloud device organizations, child groups, and device transfer workflows through the Hik-Cloud OpenAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Hik-Cloud administrative credentials and access tokens.

Mitigation: Use trusted HTTPS Hik-Cloud endpoints, store credentials in a controlled environment, avoid passing bearer tokens with --access-token, and restrict token cache file permissions.

Risk: Delete and device-transfer actions can make destructive device-group changes.

Mitigation: Require an explicit human check before delete or device-transfer operations.

## Reference(s):

- [认证说明](references/auth.md)
- [设备分组管理摘要](references/device-group-management.md)
- [ClawHub skill page](https://clawhub.ai/hik-cloud-open/skills/hik-cloud-open-device-group-management)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell command examples and optional JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and Hik-Cloud client credentials in HIK_OPEN_CLIENT_ID and HIK_OPEN_CLIENT_SECRET.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
