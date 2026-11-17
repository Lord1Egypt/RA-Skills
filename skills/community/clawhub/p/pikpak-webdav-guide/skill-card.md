## Description:

Guide users through enabling PikPak WebDAV, configuring supported clients, and understanding membership and connected-app quota limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pipiguai87-alt](https://clawhub.ai/user/pipiguai87-alt)

### License/Terms of Use:

MIT-0

## Use Case:

PikPak users can use this guide to enable WebDAV through the official account interface, configure clients such as Infuse, VidHub, or rclone, and troubleshoot access and quota limits. It also explains what the optional local account metadata checker can and cannot confirm.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WebDAV credentials allow file changes, including uploads, moves, and moving files to trash.

Mitigation: Store dedicated WebDAV credentials only in trusted clients, never share them in chat, and revoke and replace them if exposed.

Risk: The optional checker cannot confirm WebDAV connectivity or remaining transfer quota, and storage figures are not transfer-quota measurements.

Mitigation: Verify WebDAV access and transfer limits through the official account page and an authorized client before relying on them.

## Reference(s):

- [PikPak WebDAV setup](https://mypikpak.com/zh-CN/help-center/connected_apps/webdav/how_to)
- [PikPak connected-app limits](https://mypikpak.com/zh-CN/help-center/connected_apps/webdav/speed_limit)
- [rclone WebDAV configuration](https://rclone.org/webdav/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance with shell command examples; optional JSON account metadata report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The optional checker reports account metadata only; WebDAV connectivity and transfer quota remain unverified.]

## Skill Version(s):

1.1.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
