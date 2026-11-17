## Description:

Kim Msg Account Skill helps OpenClaw users install and configure the Kim Channel plugin for Kuaishou/Kwai IM message interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leegodamn](https://clawhub.ai/user/leegodamn)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw operators use this skill to create or connect a Kim application, configure Kim credentials and webhook settings, restart the OpenClaw gateway, and verify message delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles appKey, secretKey, and verificationToken values during setup and troubleshooting.

Mitigation: Use a secure local secret store or masked input path, avoid pasting secrets into shared chats or recorded terminals, and rotate credentials if exposure is suspected.

Risk: The setup flow installs the mutable @ks-openclaw/kim plugin package.

Mitigation: Install only from a trusted package source, verify the intended package version before use, and review the installed plugin before deployment.

Risk: Webhook and gateway configuration can fail because of network isolation, incorrect paths, missing permissions, or token mismatches.

Mitigation: Run the diagnostic script, verify Kim event callback settings, confirm /openapi/v2/message/send permission, and check gateway status and logs after configuration changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leegodamn/skills/kim-msg-account)
- [Kim Open Platform](https://kim.kuaishou.com/)
- [OpenApi Service Platform](https://open.kuaishou.com/)
- [Full internal Kim setup document](https://docs.corp.kuaishou.com/d/home/fcAA_W4zGstwslCQxlwehh1d2)
- [AccessProxy IDC request guidance](https://wiki.corp.kuaishou.com/pages/viewpage.action?pageId=xxxxx)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke local shell scripts that install the Kim plugin, write OpenClaw channel configuration, restart the gateway, and diagnose webhook reachability.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
