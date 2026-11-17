## Description:

Uses PPIO multimodal APIs to help an agent generate or edit images, generate videos, perform text-to-speech, and transcribe speech.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ximasadila](https://clawhub.ai/user/ximasadila)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route multimodal requests through PPIO for image generation, image editing, text-to-video, image-to-video, text-to-speech, and speech-to-text workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill normalizes API key handling patterns that could expose PPIO credentials if keys are pasted into chat or stored insecurely.

Mitigation: Use PPIO_API_KEY or a properly permissioned secret store, and do not paste API keys into chat messages or prompts.

Risk: The skill can send prompts, images, audio, faces, documents, or meeting recordings to an external PPIO service.

Mitigation: Avoid submitting private recordings, faces, documents, confidential prompts, or meeting audio unless the user accepts PPIO's handling of that data.

## Reference(s):

- [API reference](references/api-reference.md)
- [Examples](references/examples.md)
- [Test cases](references/test-cases.md)
- [PPIO API base URL](https://api.ppio.com)
- [PPIO API key management](https://ppio.com/settings/key-management)
- [PPIO models](https://ppio.com/models)
- [PPIO pricing](https://ppio.com/pricing)
- [PPIO documentation](https://docs.ppio.com)
- [ClawHub skill page](https://clawhub.ai/ximasadila/skills/ppio-multimodal)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and returned media or transcription URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include progress text, estimated cost, API request examples, task IDs, polling status, and generated media or transcript results.]

## Skill Version(s):

0.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
