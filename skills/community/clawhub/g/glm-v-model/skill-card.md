## Description:

Uses Zhipu GLM-4V and GLM-4.6V vision models for image understanding, video analysis, multimodal conversation, and chart interpretation tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baokui](https://clawhub.ai/user/baokui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call Zhipu vision models for image and video understanding, OCR-style extraction, object or scene recognition, chart analysis, and multi-image comparison.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images, screenshots, charts, video URLs, and prompts provided to the skill are sent to Zhipu's external vision API.

Mitigation: Use the skill only when that data may be shared with the provider, and avoid submitting confidential or restricted media without approval.

Risk: The skill requires a Zhipu API key in the execution environment.

Mitigation: Set ZHIPU_API_KEY only in environments where that credential should be available, and manage it as a secret.

## Reference(s):

- [Zhipu AI Open Platform](https://open.bigmodel.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, API Calls, Guidance]

**Output Format:** [Markdown with Python code examples and model response text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a ZHIPU_API_KEY environment variable and sends supplied images, video URLs, and prompts to Zhipu's external vision API.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
