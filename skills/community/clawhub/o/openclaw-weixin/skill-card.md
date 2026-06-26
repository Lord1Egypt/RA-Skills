## Description: <br>
OpenClaw Weixin Channel connects OpenClaw to WeChat through QR-code login and supports receiving WeChat messages and sending text, image, file, voice, and video replies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alichor](https://clawhub.ai/user/alichor) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw operators use this channel plugin to connect WeChat accounts to an OpenClaw gateway, receive WeChat messages, and send text or media replies through the gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The plugin has ongoing access to a WeChat account, local OpenClaw state, saved tokens, logs, and network media URLs. <br>
Mitigation: Install only for approved accounts, restrict access to local state and logs, and revoke or rotate account authorization when access is no longer needed. <br>
Risk: Under-documented debug and log-upload features could expose sensitive log data if used with untrusted destinations. <br>
Mitigation: Review debug and log-upload behavior before broad use, upload logs only to trusted HTTPS endpoints, and redact sensitive content before sharing logs. <br>
Risk: Broad remote media URL handling can be abused for unexpected downloads or large and slow transfers. <br>
Mitigation: Add or enforce URL validation, file size limits, and request timeouts before allowing arbitrary remote media downloads. <br>
Risk: Pre-authorization slash command handling needs review before broad deployment. <br>
Mitigation: Require authorization checks around slash command paths and test command behavior before enabling the plugin for production accounts. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/alichor/openclaw-weixin) <br>
- [OpenClaw install documentation](https://docs.openclaw.ai/install) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, API calls, Shell commands, Configuration] <br>
**Output Format:** [OpenClaw channel messages, JSON API payloads, and Markdown installation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OpenClaw CLI and a WeChat account authorized through QR login; plugin version 2.0.x supports OpenClaw >=2026.3.22.] <br>

## Skill Version(s): <br>
2.0.1 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
