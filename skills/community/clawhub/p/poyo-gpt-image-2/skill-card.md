## Description: <br>
GPT Image 2 generation and editing on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `gpt-image-2`, `gpt-image-2-edit`, text-to-image, multi-image editing with `image_urls`, single-image output, `auto` or aspect-ratio sizes, custom `WIDTHxHEIGHT`, and 1K/2K/4K resolution control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare and submit PoYo GPT Image 2 text-to-image, reference-guided generation, and image-editing requests with the correct model, payload fields, size, and resolution settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, referenced image URLs, job metadata, callbacks, and generated results are sent to PoYo and any configured callback endpoint. <br>
Mitigation: Avoid secrets, private internal URLs, confidential images, and proprietary prompts unless the user trusts PoYo and the callback receiver. <br>
Risk: The skill requires a PoYo API key. <br>
Mitigation: Use the POYO_API_KEY environment variable, avoid placing credentials in prompts or committed files, and rotate the key if it is exposed. <br>


## Reference(s): <br>
- [PoYo GPT Image 2 API documentation](https://docs.poyo.ai/api-manual/image-series/gpt-image-2) <br>
- [PoYo task status documentation](https://docs.poyo.ai/api-manual/task-management/status) <br>
- [PoYo GPT Image 2 model page](https://poyo.ai/models/gpt-image-2) <br>
- [PoYo GPT Image 2 OpenAPI JSON](https://docs.poyo.ai/api-manual/image-series/gpt-image-2.json) <br>
- [Bundled API reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON payloads and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May submit one PoYo image generation or edit job per API request and report a task_id for polling or callback follow-up.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
