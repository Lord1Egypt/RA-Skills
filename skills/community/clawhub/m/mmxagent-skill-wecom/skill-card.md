## Description:

Connects OpenClaw to WeCom by guiding users through link-based authorization, then saving the returned bot credentials after the user confirms authorization is complete.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oreoandyuumi](https://clawhub.ai/user/oreoandyuumi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they need to bind a WeCom bot to OpenClaw and enable WeCom chat connectivity through an explicit authorization flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow stores a WeCom bot secret in ~/.openclaw/openclaw.json.

Mitigation: Install only when connecting OpenClaw to WeCom is intended, restrict access to the OpenClaw configuration file, and avoid sharing the stored secret.

Risk: The workflow contacts work.weixin.qq.com and restarts the OpenClaw gateway after authorization.

Mitigation: Run it only in an environment where WeCom network access and gateway restart are expected, and wait for explicit user confirmation before polling or changing configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oreoandyuumi/skills/mmxagent-skill-wecom)
- [WeCom authorization generation endpoint](https://work.weixin.qq.com/ai/qc/generate?source=wecom-cli&plat=3)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with bash commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before polling; stores WeCom bot credentials in OpenClaw configuration and restarts the gateway after successful authorization.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
