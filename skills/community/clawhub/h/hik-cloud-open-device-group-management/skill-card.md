## Description: <br>
调用海康云眸开放平台设备分组管理接口，包括新增组、删除组、更新组、查询组织详情、查询所有组织、查询下级组和设备转移分组。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hik-cloud-open](https://clawhub.ai/user/hik-cloud-open) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Hik-Cloud device organizations, child groups, and device transfers through the Hik-Cloud OpenAPI while relying on the bundled script for token retrieval, caching, and retry behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, delete, update, and transfer Hik-Cloud device group data. <br>
Mitigation: Manually review exact group and device identifiers before delete, update, create, or transfer commands. <br>
Risk: The skill handles OAuth credentials and access tokens, including a local token cache. <br>
Mitigation: Use least-privilege Hik credentials, avoid passing access tokens on the command line, and protect or periodically clear the token cache. <br>
Risk: A custom base URL can redirect requests away from the default Hik-Cloud endpoint. <br>
Mitigation: Keep base URL overrides limited to trusted Hik-compatible endpoints. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hik-cloud-open/hik-cloud-open-device-group-management) <br>
- [Publisher profile](https://clawhub.ai/user/hik-cloud-open) <br>
- [Authentication notes](references/auth.md) <br>
- [Device group management API summary](references/device-group-management.md) <br>
- [Default Hik-Cloud OpenAPI base URL](https://api2.hik-cloud.com) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, JSON, text] <br>
**Output Format:** [Markdown guidance with shell commands; the bundled script returns text summaries or JSON responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and Hik-Cloud credentials in HIK_OPEN_CLIENT_ID and HIK_OPEN_CLIENT_SECRET.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
