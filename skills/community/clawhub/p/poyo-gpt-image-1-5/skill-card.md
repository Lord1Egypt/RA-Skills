## Description: <br>
Use PoYo AI GPT Image 1.5 through the `https://api.poyo.ai/api/generate/submit` endpoint to generate or edit media, prepare PoYo-compatible payloads, submit jobs, and poll task status for `gpt-image-1.5` and `gpt-image-1.5-edit`. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to build PoYo GPT Image 1.5 generation or editing payloads, submit authenticated image jobs, and track task status or callback-based completion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill submits prompts, image URLs, mask URLs, callback URLs, and API credentials to PoYo's API. <br>
Mitigation: Use `POYO_API_KEY` from an environment variable, review payloads before submission, and avoid sending confidential prompts, private image URLs, secrets in URLs, or untrusted callback URLs unless sharing them with PoYo is intended. <br>
Risk: Network requests and API-key use are required for job submission. <br>
Mitigation: Install and run the skill only when PoYo API access is intended, and inspect generated curl commands or payloads before execution. <br>


## Reference(s): <br>
- [PoYo GPT Image 1.5 documentation](https://docs.poyo.ai/api-manual/image-series/gpt-image-1.5) <br>
- [PoYo GPT Image 1.5 OpenAPI JSON](https://docs.poyo.ai/api-manual/image-series/gpt-image-1.5.json) <br>
- [PoYo task status documentation](https://docs.poyo.ai/api-manual/task-management/status) <br>
- [Local API reference](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/coolhackboy/poyo-gpt-image-1-5) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON payloads and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include selected model id, payload summary or final payload, reference image usage, returned task_id, and polling or webhook next steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
