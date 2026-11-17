## Description:

OpenClaw WeCom Channel lets an OpenClaw agent receive and send WeCom/WxWork text messages through a self-hosted enterprise application, with message encryption, token management, and access policy configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darrryz](https://clawhub.ai/user/darrryz)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw operators use this skill to connect agents to WeCom/WxWork for direct text conversations and outbound notifications through a WeCom custom application. It is suited for teams that can provide WeCom administrator credentials, a public HTTPS callback endpoint, and OpenClaw gateway operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documented pairing access control is not enforced before messages are authorized to the agent.

Mitigation: Use allowlist mode rather than pairing mode until pairing enforcement is fixed, and avoid routing privileged agents or sensitive tools through this channel.

Risk: The WeCom callback endpoint must be reachable from the public internet.

Mitigation: Expose only the intended callback endpoint and place it behind rate limits and request body-size limits.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/darrryz/skills/openclaw-wecom-channel)
- [OpenClaw Project](https://github.com/openclaw/openclaw)
- [WeCom Developer Documentation](https://developer.work.weixin.qq.com/document/)

## Skill Output:

**Output Type(s):** [Text, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline configuration and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces plain-text WeCom message guidance and channel configuration for OpenClaw; media, reactions, threads, polls, native commands, and block streaming are not supported.]

## Skill Version(s):

0.1.0 (source: server release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
