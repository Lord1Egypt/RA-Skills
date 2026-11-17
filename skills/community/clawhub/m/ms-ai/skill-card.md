## Description:

ModelScope AI skill for text-to-image generation, image-to-image editing, vision understanding, OCR-oriented image analysis, and text generation with model and API-key rotation on rate limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luhuiwang](https://clawhub.ai/user/luhuiwang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to route image generation, image editing, vision analysis, and text generation requests through ModelScope models from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, images, OCR targets, and chat history may be sent to ModelScope.

Mitigation: Use only with data approved for third-party processing, and avoid sensitive files unless the user has explicitly approved that transfer.

Risk: API-key prefix logging can expose credential fragments in terminal logs.

Mitigation: Patch logging to avoid printing any API-key prefix before using shared or persistent logs.

Risk: Remote image download URLs are trusted by the image-generation workflow.

Mitigation: Validate URL schemes, hosts, response sizes, and image dimensions before downloading or processing returned images.

Risk: Unpinned dependencies can change behavior or supply-chain exposure over time.

Mitigation: Install dependencies in an isolated environment with pinned versions reviewed for the deployment.

## Reference(s):

- [ModelScope Inference API](https://api-inference.modelscope.cn/)
- [ClawHub skill page](https://clawhub.ai/luhuiwang/skills/ms-ai)

## Skill Output:

**Output Type(s):** [text, image files, json, shell commands, configuration]

**Output Format:** [Generated image files, plain text, and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MODELSCOPE_API_KEY; text output can include conversation history files, and image or vision commands can write output files.]

## Skill Version(s):

1.2.1 (source: server release evidence; artifact _meta.json and changelog list 1.2.0, and SKILL.md frontmatter lists 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
