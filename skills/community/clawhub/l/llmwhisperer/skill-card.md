## Description:

Extract text and layout from images and PDFs using LLMWhisperer API. Good for handwriting and complex forms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gumadeiras](https://clawhub.ai/user/gumadeiras)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to extract layout-preserving text from PDFs and images, including handwritten notes and complex forms, through the LLMWhisperer API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected files are uploaded to the LLMWhisperer/Unstract API for processing.

Mitigation: Use the skill only for documents that are permitted for third-party processing under the user's privacy and compliance requirements.

Risk: The documented API-key storage path is basic and may expose credentials if local permissions are loose.

Mitigation: Store the API key with restrictive permissions, and prefer an environment variable or secret manager when available.

## Reference(s):

- [LLMWhisperer API](https://unstract.com/llmwhisperer/)
- [ClawHub skill page](https://clawhub.ai/gumadeiras/skills/llmwhisperer)
- [ClawHub publisher profile](https://clawhub.ai/user/gumadeiras)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text or layout-preserving text returned by the LLMWhisperer API, with Markdown usage examples in the skill documentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an LLMWHISPERER_API_KEY and uploads the selected input file to the LLMWhisperer/Unstract API for processing.]

## Skill Version(s):

0.0.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
