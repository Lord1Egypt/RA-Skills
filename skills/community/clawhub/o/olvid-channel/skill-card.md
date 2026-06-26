## Description: <br>
Add a native Olvid channel in OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jmartel-olvid](https://clawhub.ai/user/jmartel-olvid) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to let an agent exchange direct and group messages through an Olvid daemon without exposing the OpenClaw instance on the web. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The plugin requires an Olvid daemon URL and client key, which can grant messaging access if exposed. <br>
Mitigation: Use a dedicated, least-privileged Olvid bot key, protect daemon access, and store credentials only in approved secret-management or environment configuration paths. <br>
Risk: Inbound attachments may be downloaded to local temporary storage with limited visible cleanup or retention controls. <br>
Mitigation: Treat attachments as sensitive, restrict who can message the bot, and define operational cleanup and retention controls before handling confidential media. <br>
Risk: The channel runs a reconnecting background listener that can continue processing messages until the account or service is stopped. <br>
Mitigation: Run it under supervised service controls, monitor connection and error logs, and disable or remove the account configuration when the channel is not needed. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/jmartel-olvid/olvid-channel) <br>
- [Olvid OpenClaw documentation](https://doc.bot.olvid.io/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown text messages and OpenClaw channel configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outbound text is chunked for Olvid delivery; inbound media may be represented as local attachment paths.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
