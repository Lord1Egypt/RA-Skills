## Description:

LiveClaw streams an OpenClaw agent's reasoning flow, tool activity, TTS status narration, virtual avatar overlay, and viewer interactions to a Tencent TRTC room with a public viewer page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerryang-cool](https://clawhub.ai/user/jerryang-cool)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to configure, start, monitor, publish, and stop a livestream that makes an agent's work visible to viewers. It is intended for TRTC-backed live dashboards with optional TTS narration and bidirectional viewer messaging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Viewer traffic may expose prompts, intermediate reasoning, tool activity, and agent outputs.

Mitigation: Run only for intended audiences, protect viewer and gateway access with authentication, and avoid public exposure of port 19000 or the OpenClaw gateway.

Risk: Tencent TRTC, IM callback, and CAM credentials are sensitive and can expand access beyond the local agent session.

Mitigation: Use isolated, least-privileged Tencent credentials, keep secrets out of files and logs, and rotate credentials after testing or demos.

Risk: Enabling the callback token or bundled helper skills can allow remote viewers to trigger agent actions.

Mitigation: Enable remote interaction only when intended, review bundled skills before deployment, and scope the agent environment to the minimum required permissions.

## Reference(s):

- [LiveClaw on ClawHub](https://clawhub.ai/jerryang-cool/skills/liveclaw)
- [OpenClaw](https://openclaw.ai)
- [OpenClaw Skills documentation](https://docs.openclaw.ai/zh-CN/tools/skills)
- [Tencent Cloud TRTC console](https://console.cloud.tencent.com/trtc/app)
- [Tencent Cloud TRTC documentation](https://cloud.tencent.com/document/product/647/102957)
- [Tencent Cloud TRTC Web SDK documentation](https://cloud.tencent.com/document/product/647/116544)
- [Tencent Cloud IM console](https://console.cloud.tencent.com/im)
- [Tencent Cloud CAM API key management](https://console.cloud.tencent.com/cam/capi)
- [Tencent TLSSigAPIv2 Python reference](https://github.com/tencentyun/tls-sig-api-v2-python/blob/master/TLSSigAPIv2.py)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline shell commands and generated runtime configuration/viewer files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and external Tencent TRTC credentials; optional IM callback and CAM credentials enable bidirectional interaction and TTS.]

## Skill Version(s):

1.0.2 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
