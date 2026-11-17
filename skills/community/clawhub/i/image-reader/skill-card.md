## Description:

Image Reader uses a multimodal OpenAI-compatible model API to analyze images, extract OCR text, and generate image descriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simonjoe246](https://clawhub.ai/user/simonjoe246)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to process screenshots or image files when they need OCR text extraction, scene description, or general image analysis through a configured multimodal model API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send local image contents to a configured external model API.

Mitigation: Use it only with images approved for external processing and avoid credentials, private keys, sensitive documents, or internal screenshots unless that sharing is explicitly allowed.

Risk: The command accepts any readable local path and does not enforce strong type or size validation before upload.

Mitigation: Run it through a wrapper or agent policy that restricts inputs to confirmed image files and applies size limits before invocation.

Risk: The artifact relies on API configuration and a placeholder API key in config.yaml.

Mitigation: Configure credentials through an approved secret-management process and review the endpoint before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/simonjoe246/skills/image-reader)
- [Configured OpenAI-compatible API endpoint](https://ark.cn-beijing.volces.com/api/coding/v3)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown returned by the model, with command-line examples and configuration guidance in the skill documentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include extracted text, visual descriptions, mixed OCR and description content, or an error string from the API call.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
