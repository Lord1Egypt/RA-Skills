## Description:

Analyze images using vision-capable AI models through OATDA's unified API for descriptions, OCR, diagrams, charts, screenshots, and photos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devcsde](https://clawhub.ai/user/devcsde)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to route image-analysis requests to OATDA-supported vision models, including OCR, visual description, and chart or screenshot interpretation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image URLs and prompts are sent to OATDA and downstream model providers.

Mitigation: Avoid confidential screenshots, documents, or regulated data unless the user has approval for that transfer.

Risk: The shell command template can mix user-supplied prompt text with an API-key-bearing request.

Mitigation: Review commands before execution and prefer constructing JSON payloads with jq or a typed client.

Risk: The skill reads OATDA_API_KEY from the environment or local credentials.

Mitigation: Never print the full API key and verify only that a key is present before making requests.

## Reference(s):

- [OATDA](https://oatda.com)
- [OATDA image analysis endpoint](https://oatda.com/api/v1/llm/image)
- [ClawHub skill page](https://clawhub.ai/devcsde/skills/oatda-vision-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON examples and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include token usage and cost fields returned by the OATDA API.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
