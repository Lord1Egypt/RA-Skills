## Description:

Generate captions and descriptions for images, videos, and documents using the Zhipu GLM-V multimodal model series.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaredforreal](https://clawhub.ai/user/jaredforreal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to caption, summarize, or interpret supported image, video, and document inputs through Zhipu GLM-V. It is suited for media understanding workflows that can send selected inputs or URLs to Zhipu's service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images, video URLs, document URLs, prompts, and API usage are sent to Zhipu's service.

Mitigation: Use only media that organizational policy allows to be processed by Zhipu, and avoid confidential, regulated, or secret-containing inputs unless that provider is approved.

Risk: Videos and documents are URL-only even though some documentation wording may imply local path support.

Mitigation: Provide URLs for video and document inputs, and use local paths or base64 only for supported image inputs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jaredforreal/skills/glmv-caption)
- [Skill Homepage](https://github.com/zai-org/GLM-V/tree/main/skills/glmv-caption)
- [Zhipu Chat Completions API Documentation](https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E5%AF%B9%E8%AF%9D%E8%A1%A5%E5%85%A8)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON responses containing caption text, status, optional usage data, warnings, or errors; Markdown guidance and shell commands in agent-facing use.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZHIPU_API_KEY. Images may use URLs, local paths, or base64; videos and documents are URL-only; image, video, and file inputs are mutually exclusive per request.]

## Skill Version(s):

1.0.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
