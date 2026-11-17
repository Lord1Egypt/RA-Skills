## Description:

Add a native Olvid channel in OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jmartel-olvid](https://clawhub.ai/user/jmartel-olvid)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw operators use this skill to add an Olvid messaging channel so agents can exchange direct or group messages through an Olvid daemon without exposing the OpenClaw instance on the web.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Olvid daemon credentials and client keys that may be stored in OpenClaw configuration.

Mitigation: Use only a local daemon or an HTTPS daemon you control, protect configuration storage, and rotate client keys if exposure is suspected.

Risk: Untrusted senders may push large attachments before attachment limits and cleanup are addressed.

Mitigation: Enable the channel only for trusted Olvid contacts or groups, apply attachment limits at the deployment layer, and monitor attachment cleanup.

Risk: Stopping the account may not fully stop message processing until the plugin process exits.

Mitigation: Restart the plugin process after disabling the account and confirm message monitoring has stopped before relying on shutdown.

## Reference(s):

- [Olvid OpenClaw documentation](https://doc.bot.olvid.io/openclaw)
- [ClawHub Olvid Channel listing](https://clawhub.ai/jmartel-olvid/skills/olvid-channel)

## Skill Output:

**Output Type(s):** [text, configuration, shell commands, guidance]

**Output Format:** [Olvid messages and Markdown setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outbound text is chunked for Markdown messages with a 4000-character limit; media attachments may be sent when configured.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
