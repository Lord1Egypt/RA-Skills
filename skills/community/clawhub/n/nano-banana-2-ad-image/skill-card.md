## Description:

Uses Nano Banana 2 through AI Hive to turn audiences, product evidence, approved claims, and a single test variable into ad image candidates for pre-launch review and A/B testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, ecommerce, and creative operations teams use this skill to create ad image candidates from approved product references and claim boundaries. It is intended to support reviewable A/B creative workflows before platform-specific copy, pricing, and compliance language are added.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected reference images may be sent to AI Hive during generation.

Mitigation: Use only approved product images and prompts suitable for third-party processing, and avoid confidential or unlicensed reference material.

Risk: The helper can save an AI Hive API key locally.

Mitigation: Treat the key as sensitive, prefer environment variables or a protected config file, and rotate the key if it is exposed.

Risk: Generated ad images may imply unsupported claims or conflict with platform advertising rules.

Mitigation: Review every generated image against approved claims, SKU facts, and current platform policies before publishing.

Risk: The usage examples request a bare `pip3 install requests` dependency install.

Mitigation: Use a pinned dependency or locked environment for repeatable deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/nano-banana-2-ad-image)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline bash commands and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit AI Hive image generation tasks, return task status JSON, and download generated images to a local output directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
