## Description: <br>
帮助代理通过海康云眸开放平台查询、同步和重命名设备通道，并自动处理 access_token 获取、缓存和刷新。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hik-cloud-open](https://clawhub.ai/user/hik-cloud-open) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and support agents use this skill to list Hik-Cloud device channels, synchronize channels, rename channels, and synchronize channel names through the Hik-Cloud OpenAPI workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses sensitive Hik-Cloud credentials and OAuth tokens. <br>
Mitigation: Use least-privilege credentials, avoid passing tokens on the command line, and protect or periodically remove the local token cache. <br>
Risk: Sync and rename operations can change channel state or labels. <br>
Mitigation: Verify device serials, channel numbers, and channel names before running state-changing commands. <br>
Risk: Custom base URLs can redirect credentialed API calls. <br>
Mitigation: Use only trusted base URLs and prefer the default Hik-Cloud production endpoint unless an approved environment requires otherwise. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hik-cloud-open/hik-cloud-open-device-channel-management) <br>
- [hik-cloud-open publisher profile](https://clawhub.ai/user/hik-cloud-open) <br>
- [Authentication notes](references/auth.md) <br>
- [Device channel management reference](references/device-channel-management.md) <br>
- [Hik-Cloud device channel management API](https://pic.hik-cloud.com/opencustom/apidoc/online/open/a5982b796d354b33b8b740ba3fb98c11.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; helper script output can be text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and Hik-Cloud credentials; can use HIK_OPEN_BASE_URL or an explicit base URL for approved non-default environments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
