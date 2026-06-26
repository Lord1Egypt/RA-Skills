## Description: <br>
Nano Banana Skill guides agents through Monet API usage for Nano Banana image generation models, including character consistency, 1K-4K output, up to 14 reference images, and extreme aspect ratios up to 21:9 and 8:1. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seekton](https://clawhub.ai/user/seekton) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to create image generation tasks through the Monet API, including character-consistent image series, high-resolution outputs, reference-image workflows, and ultra-wide aspect ratios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, reference image URLs, uploaded images, and task history are sent to monet.vision. <br>
Mitigation: Use a dedicated API key where possible and avoid sending secrets, private documents, regulated data, or sensitive personal images unless authorized. <br>
Risk: The skill can upload local image files to an external service. <br>
Mitigation: Review file paths before upload and confirm that each selected file is appropriate to share with Monet. <br>
Risk: Image generation requests may be retried by agents or automation. <br>
Mitigation: Use a unique idempotency key for each intended task to reduce duplicate task creation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/seekton/nano-banana-skill) <br>
- [Monet API website](https://monet.vision) <br>
- [Monet API keys](https://monet.vision/skills/keys) <br>
- [Skill documentation](SKILL.md) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl commands, TypeScript examples, JSON request and response shapes, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for authenticated Monet API requests and asynchronous task polling; generated images and uploaded files are handled by the external Monet service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
