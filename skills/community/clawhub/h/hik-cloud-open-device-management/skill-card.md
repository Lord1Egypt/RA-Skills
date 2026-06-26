## Description: <br>
Manages Hik-Cloud Open Platform devices by registering, deleting, renaming, querying, counting, checking status, and rebooting devices while handling OAuth token acquisition and refresh internally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hik-cloud-open](https://clawhub.ai/user/hik-cloud-open) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations staff use this skill to manage Hik-Cloud devices through the supported Open Platform device-management APIs, including create, delete, rename, query, list, count, status, and reboot workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delete or reboot Hik-Cloud devices. <br>
Mitigation: Verify target device serial numbers and confirm business impact before delete or reboot actions. <br>
Risk: The helper caches API tokens locally. <br>
Mitigation: Protect or clear the local token cache on shared machines and use least-privileged Hik credentials where possible. <br>
Risk: Credentials and API traffic depend on the configured Hik endpoint. <br>
Mitigation: Keep the base URL pointed at a trusted Hik endpoint and avoid injecting credentials into untrusted sessions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hik-cloud-open/hik-cloud-open-device-management) <br>
- [Publisher profile](https://clawhub.ai/user/hik-cloud-open) <br>
- [认证说明](references/auth.md) <br>
- [设备基础管理文档摘要](references/device-management.md) <br>
- [Hik-Cloud device-management API documentation](https://pic.hik-cloud.com/opencustom/apidoc/online/open/d1856283d9d944719474b24b6374e351.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text summaries or structured JSON from the helper script, with Markdown guidance and shell command examples in the skill instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and Hik-Cloud credentials via HIK_OPEN_CLIENT_ID and HIK_OPEN_CLIENT_SECRET or an explicit access token.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
