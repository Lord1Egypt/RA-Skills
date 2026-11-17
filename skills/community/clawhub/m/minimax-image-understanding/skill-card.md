## Description:

Minimax Image Understanding analyzes local images with MiniMax VLM, OpenAI GPT-4o, or Anthropic Claude Vision and returns a business-focused text description.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aidescend](https://clawhub.ai/user/aidescend)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to describe screenshots, charts, and document photos with emphasis on content, data, and business meaning rather than visual element positions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload selected local images and prompts to external MiniMax, OpenAI, or Anthropic APIs.

Mitigation: Use it only with images approved for those providers, and avoid confidential screenshots, credentials, regulated documents, or private files unless policy permits that upload.

Risk: A custom MINIMAX_API_HOST can send MiniMax requests, image data, and credentials to an unintended host.

Mitigation: Keep MINIMAX_API_HOST set to the intended trusted MiniMax endpoint and review host configuration before execution.

Risk: The release was marked suspicious by the authoritative security evidence because file upload scope and image validation controls need review.

Mitigation: Review the selected image path, file type, file size, and destination provider before running the script.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aidescend/skills/minimax-image-understanding)
- [Publisher profile](https://clawhub.ai/user/aidescend)
- [MiniMax API endpoint](https://api.minimaxi.com)
- [OpenAI Chat Completions API endpoint](https://api.openai.com/v1/chat/completions)
- [Anthropic Messages API endpoint](https://api.anthropic.com/v1/messages)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text image description, with Markdown setup and command examples in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output focuses on business meaning, data content, and business logic. The script requests up to 1000 tokens for OpenAI and Anthropic responses.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
