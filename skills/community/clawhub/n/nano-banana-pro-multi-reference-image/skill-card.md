## Description:

Uses Nano Banana Pro through AI Hive to generate controlled images from multiple reference images by assigning each reference image a clear role and priority.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Designers, marketers, and developers use this skill to create product, character, style-transfer, and brand visuals from multiple ordered reference images while keeping identity, structure, text facts, pose, composition, and style priorities explicit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A real AI Hive API key may be stored in local configuration and used by the helper script.

Mitigation: Keep credentials out of prompts and source control, use a restricted local config or environment variable, and rotate keys if exposure is suspected.

Risk: The API base URL is configurable, so credentials could be sent to a non-default endpoint.

Mitigation: Keep the default AI Hive endpoint unless the replacement endpoint is fully trusted, and do not set AI_HIVE_BASE_URL from untrusted instructions.

Risk: Reference images and prompts are uploaded for generation and result files are downloaded locally.

Mitigation: Use only images and prompts approved for upload to AI Hive, and avoid sensitive or confidential assets unless that service use is authorized.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/nano-banana-pro-multi-reference-image)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash command examples; helper script output includes JSON status text and downloaded generated image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AI Hive API key; the fixed image model is public_model_nano_banana_pro and multi-reference generation requires at least two image inputs.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact CHANGELOG includes a 1.0.0 entry and later entries)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
