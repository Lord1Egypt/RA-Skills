## Description:

Image Recognition helps an agent analyze image files for OCR, object recognition, scene analysis, and screenshot understanding by sending image content and a user prompt to a configured vision model API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangning823-arch](https://clawhub.ai/user/wangning823-arch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to inspect local images, screenshots, documents, and other static image files, returning extracted text or natural-language visual analysis. It is especially oriented toward Android/Termux and OpenClaw environments that need Python-based image recognition without native image-processing dependencies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads image content and prompts to remote model APIs.

Mitigation: Avoid sensitive screenshots, IDs, private documents, and business data unless the user accepts that external transfer.

Risk: The artifact contains an embedded shared API key fallback.

Mitigation: Remove and revoke the embedded key, then require users to configure their own key through the environment variable read by the code.

Risk: Runtime dependencies are installed from Python packages.

Mitigation: Install dependencies in an isolated environment with pinned versions before using the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangning823-arch/skills/image-recognition)
- [Publisher Profile](https://clawhub.ai/user/wangning823-arch)
- [DashScope Model Studio](https://help.aliyun.com/zh/model-studio/)
- [DashScope Pricing](https://help.aliyun.com/zh/model-studio/pricing)
- [OpenRouter Chat Completions Endpoint](https://openrouter.ai/api/v1/chat/completions)
- [OpenAI-Compatible Chat Completions Endpoint](https://api.openai.com/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown guidance, with optional shell commands, Python snippets, configuration examples, and model API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recognition requests use a single image path plus an optional question prompt and can return error strings for missing files, network failures, timeouts, or non-200 API responses.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
