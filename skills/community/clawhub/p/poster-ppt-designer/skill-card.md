## Description:

使用灵雀AI设计产品推广海报、信息图和PPT页面，根据用户提供的文字描述和图片素材调用灵雀AI的广告平面设计功能生成营销海报、信息图和PPT页面。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lujiang-web](https://clawhub.ai/user/lujiang-web)

### License/Terms of Use:

MIT-0

## Use Case:

Marketers, creators, designers, and business teams use this skill to turn product descriptions, campaign copy, and optional logo or image URLs into generated poster, infographic, or PPT page designs through Lingque AI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lingque AI credentials and tokens are handled by local scripts and may be exposed through configuration files, logs, or command history.

Mitigation: Use tightly permissioned local configuration or environment variables, treat config.json as sensitive, and rotate credentials or tokens if exposure is suspected.

Risk: Prompts, text, logo/image URLs, and generated-design requests are sent to a third-party service.

Mitigation: Avoid submitting confidential assets, regulated data, or private campaign material unless the service is approved for that data.

Risk: The artifact describes collecting SMS verification codes during registration.

Mitigation: Complete login or registration directly on the official service and do not share SMS verification codes with the agent.

Risk: The saved password is only obfuscated and can be recovered from the included code.

Mitigation: Do not treat the encoded password as secure storage; restrict file access or use short-lived credentials where possible.

## Reference(s):

- [Lingque AI](https://lqai.net/)
- [ClawHub skill page](https://clawhub.ai/lujiang-web/skills/poster-ppt-designer)
- [Publisher profile](https://clawhub.ai/user/lujiang-web)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON payload examples and shell commands; successful generation returns an image URL.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Lingque AI credentials and sends prompts, text, logo/image URLs, and generated-design requests to server.pinza.com.cn.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
