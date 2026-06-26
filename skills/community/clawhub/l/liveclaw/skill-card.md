## Description: <br>
LiveClaw streams an OpenClaw Agent's reasoning, tool use, and results to a Tencent TRTC live room with a browser viewer, avatar overlay, TTS status narration, and two-way IM interaction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerryang-cool](https://clawhub.ai/user/jerryang-cool) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use LiveClaw to publish an agent's live work session as a TRTC stream, expose a public viewer page, and let viewers interact with the agent through IM-backed chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says the skill exposes public live-streaming and live-control functions that need review before installation. <br>
Mitigation: Install first on an isolated host or test workspace, keep the viewer and gateway behind firewall or authentication controls, and expose it publicly only after review. <br>
Risk: The security guidance notes broad persistent platform changes, persistent daemons, and shared OpenClaw configuration changes. <br>
Mitigation: Confirm the stop and uninstall process, monitor daemon status, and avoid installing it in a shared production workspace until the operational behavior is accepted. <br>
Risk: The skill requires sensitive Tencent Cloud credentials for TRTC, IM callback handling, and optional TTS. <br>
Mitigation: Use dedicated least-privilege Tencent Cloud keys, keep secrets out of client-side code and logs, and rotate credentials after testing or suspected exposure. <br>
Risk: The security guidance calls out bundled email and music sub-skills that can extend the runtime's external-service access. <br>
Mitigation: Review the bundled email and music sub-skills before enabling them, and configure only the providers and credentials required for the deployment. <br>


## Reference(s): <br>
- [ClawHub LiveClaw release page](https://clawhub.ai/jerryang-cool/liveclaw) <br>
- [ClawHub publisher profile: jerryang-cool](https://clawhub.ai/user/jerryang-cool) <br>
- [Tencent Cloud TRTC console](https://console.cloud.tencent.com/trtc/app) <br>
- [Tencent Cloud IM callback settings](https://console.cloud.tencent.com/im/callback-setting) <br>
- [Tencent Cloud CAM API keys](https://console.cloud.tencent.com/cam/capi) <br>
- [Tencent Cloud TRTC RTMP publishing documentation](https://cloud.tencent.com/document/product/647/102957) <br>
- [Tencent Cloud TRTC web SDK documentation](https://cloud.tencent.com/document/product/647/116544) <br>
- [OpenClaw skills documentation](https://docs.openclaw.ai/zh-CN/tools/skills) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown instructions with bash commands and configuration parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational steps for configuring, starting, viewing, monitoring, and stopping a live TRTC stream.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
