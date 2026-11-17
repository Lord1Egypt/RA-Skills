## Description:

Execute multimodal tasks using Novita AI for text-to-image, image-to-image, text-to-video, image-to-video, text-to-speech, and speech-to-text workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ximasadila](https://clawhub.ai/user/ximasadila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to call Novita AI endpoints for image generation or editing, video generation, text-to-speech, and speech-to-text tasks. It helps agents prepare API requests, surface progress, poll asynchronous jobs, and return generated media URLs or transcribed text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed if pasted directly into chat or stored in plain text.

Mitigation: Use a scoped Novita API key through managed secrets or the NOVITA_API_KEY environment variable, and avoid sharing credentials in conversation text.

Risk: Private prompts, images, audio recordings, or documents are sent to Novita AI for processing.

Mitigation: Only submit content approved for third-party processing and exclude confidential or sensitive media unless that data handling is accepted.

Risk: Generated media tasks can incur API charges and asynchronous jobs may take time to complete.

Mitigation: Review estimated cost before execution, monitor polling status for async jobs, and handle insufficient balance, rate limit, and failed-task responses.

## Reference(s):

- [Novita AI API Reference](references/api-reference.md)
- [Usage Examples](references/examples.md)
- [Test Cases](references/test-cases.md)
- [Novita AI API Key Management](https://novita.ai/settings/key-management)
- [Novita AI Model Catalog](https://novita.ai/models)
- [Novita AI Pricing](https://novita.ai/pricing)
- [Novita AI Documentation](https://docs.novita.ai)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, text, markdown]

**Output Format:** [Markdown guidance with inline shell commands, JSON request examples, and generated media URLs or transcribed text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return image, video, or audio URLs from Novita AI; video and TTS workflows may require asynchronous task polling.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
