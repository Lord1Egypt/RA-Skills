## Description: <br>
Nano Banana 2 helps agents generate and edit images through PoYo's Nano Banana 2 API, including text-to-image, image-to-image, multi-reference workflows, and 1K, 2K, or 4K output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to prepare PoYo Nano Banana 2 image generation or editing requests, choose the appropriate model, submit API payloads, and track the returned task id for polling or callbacks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts and image URLs to PoYo using a POYO_API_KEY, which can expose sensitive text, private image locations, or credentials if handled carelessly. <br>
Mitigation: Review payloads before submission, keep the API key in an environment variable instead of command arguments, and use temporary or access-controlled URLs for private images. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/coolhackboy/poyo-nano-banana-2) <br>
- [PoYo Nano Banana 2 API documentation](https://docs.poyo.ai/api-manual/image-series/nano-banana-2-new) <br>
- [PoYo task status documentation](https://docs.poyo.ai/api-manual/task-management/status) <br>
- [PoYo Nano Banana 2 model page](https://poyo.ai/models/nano-banana-2) <br>
- [API reference](references/api.md) <br>
- [Frontend notes](references/frontend-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON payload examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a selected model, summarized request parameters, reference-image usage, a returned task_id, and the next polling or webhook step.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
