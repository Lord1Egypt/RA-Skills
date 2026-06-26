## Description: <br>
Image generation helper for OpenClaw that calls OpenRouter image models such as Seedream and supports prompt, model, size, aspect ratio, and output path configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goforu](https://clawhub.ai/user/goforu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to generate or transform images from prompts through OpenRouter-backed image models. It is intended for OpenClaw-style workflows that need configurable model selection, resolution tiers, aspect ratios, and local image output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload any readable local file path passed as --input-image to OpenRouter. <br>
Mitigation: Use only intentional, non-confidential input images and avoid arbitrary local paths until file type, path, and size validation are added. <br>
Risk: The skill requires an OpenRouter API key and may incur provider charges when generating images. <br>
Mitigation: Use a dedicated OpenRouter key with spending limits and install only in environments that are trusted with that credential. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/goforu/phoenixclaw-image-gen) <br>
- [OpenRouter Seedream 4.5 Model Page](https://openrouter.ai/bytedance-seed/seedream-4.5) <br>
- [OpenRouter Image Generation Guide](https://openrouter.ai/docs/guides/overview/multimodal/image-generation) <br>
- [CLI Contract](references/cli-contract.md) <br>
- [Configuration Specification](references/configuration.md) <br>
- [Resolution Guide](references/resolution-guide.md) <br>
- [Extension Guide](references/extension-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, API Calls, Shell commands, Configuration instructions] <br>
**Output Format:** [PNG image file with structured JSON success or error payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENROUTER_API_KEY; optional model, input image, size, aspect ratio, and output path parameters are supported.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
