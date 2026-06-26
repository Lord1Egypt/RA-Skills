## Description: <br>
Use PoYo AI GPT-4o Image to generate or edit media by preparing PoYo-compatible payloads, submitting jobs, and polling task status for `gpt-4o-image` or `gpt-4o-image-edit`. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare PoYo GPT-4o Image generation or edit requests, submit authenticated jobs, and report the returned task ID for polling or webhook follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill submits user-provided prompts, image URLs, and optional callback URLs to PoYo. <br>
Mitigation: Review the JSON payload before submission and avoid sending private prompts, sensitive images, internal image URLs, or callback URLs unless sharing them with PoYo is acceptable. <br>
Risk: API keys can be exposed if passed directly in shell history or shared command text. <br>
Mitigation: Set `POYO_API_KEY` in the environment and avoid placing credentials in command-line arguments or saved payload files. <br>


## Reference(s): <br>
- [PoYo GPT 4O Image API Reference](references/api.md) <br>
- [PoYo GPT-4o Image documentation](https://docs.poyo.ai/api-manual/image-series/gpt-4o-image) <br>
- [PoYo GPT-4o Image OpenAPI JSON](https://docs.poyo.ai/api-manual/image-series/gpt-4o-image.json) <br>
- [PoYo task status documentation](https://docs.poyo.ai/api-manual/task-management/status) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown with JSON payloads and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a returned task_id when the agent submits a request.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
