## Description:

海康云眸设备控制帮助代理通过海康云眸开放平台执行设备布撤防、云台控制、远程抓图、OSD 配置、设备校时、NTP 配置和存储卡初始化操作。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hik-cloud-open](https://clawhub.ai/user/hik-cloud-open)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and support agents use this skill to prepare and run Hik-Cloud device-control actions when a user provides device serials, channel numbers, and requested operations. It is intended for workflows involving arm or disarm state, PTZ movement, remote capture, OSD changes, time or NTP settings, and storage-card initialization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A custom base URL can receive Hik-Cloud credentials or tokens.

Mitigation: Use the default Hik-Cloud endpoint or a fully trusted endpoint, and review any HIK_OPEN_BASE_URL or --base-url value before execution.

Risk: Device actions such as capture, arm/disarm, PTZ movement, OSD changes, time or NTP changes, and storage-card initialization can affect real equipment.

Mitigation: Require explicit human confirmation of the target device, channel, and operation before running these commands.

Risk: Stored or exposed credentials and cached tokens can broaden account access.

Mitigation: Use narrowly scoped Hik-Cloud application permissions, protect or disable the token cache where possible, and avoid displaying raw tokens.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hik-cloud-open/skills/hik-cloud-open-device-control)
- [Authentication and token handling](references/auth.md)
- [Device arm and disarm](references/device-arm-disarm.md)
- [PTZ control](references/ptz-control.md)
- [Remote capture](references/remote-capture.md)
- [Device OSD](references/device-osd.md)
- [Time sync and NTP configuration](references/time-sync.md)
- [Storage-card initialization](references/storage-card-init.md)
- [Hik-Cloud time sync API reference](https://pic.hik-cloud.com/opencustom/apidoc/online/open/7093bbc2db7a427ca5b60001caff338d.html)
- [Hik-Cloud storage initialization API reference](https://pic.hik-cloud.com/opencustom/apidoc/online/open/a9efdfc48a2f4ab5bd7c44ba325b6642.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; the helper script can return text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and Hik-Cloud credentials via HIK_OPEN_CLIENT_ID and HIK_OPEN_CLIENT_SECRET.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
