## Description: <br>
Use PoYo AI Nano Banana for prompt-based image generation and reference-image editing across supported aspect ratios through the PoYo generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and image-generation users use this skill to prepare and submit PoYo Nano Banana generation or edit jobs, including prompts, reference image URLs, aspect ratios, and task tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided prompts or image URLs to PoYo's external API using a user-supplied API key. <br>
Mitigation: Use it only when external PoYo processing is intended, keep POYO_API_KEY private, and review payloads before submission. <br>
Risk: Requests can expose sensitive prompts, private image URLs, secrets, or callback URLs if those values are included. <br>
Mitigation: Avoid sending secrets, confidential prompts, private image URLs, or callback URLs you do not control. <br>


## Reference(s): <br>
- [PoYo Nano Banana API Reference](references/api.md) <br>
- [PoYo Nano Banana Docs](https://docs.poyo.ai/api-manual/image-series/nano-banana) <br>
- [PoYo Task Status Docs](https://docs.poyo.ai/api-manual/task-management/status) <br>
- [PoYo Nano Banana OpenAPI JSON](https://docs.poyo.ai/api-manual/image-series/nano-banana.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON payloads, text] <br>
**Output Format:** [Markdown with JSON payloads and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include the selected model id, request payload summary, task_id, and next polling or webhook step.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
