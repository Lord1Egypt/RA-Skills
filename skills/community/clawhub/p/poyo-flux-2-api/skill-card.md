## Description: <br>
Use PoYo AI Flux 2 through the `https://api.poyo.ai/api/generate/submit` endpoint to generate or edit media, prepare PoYo-compatible payloads, submit jobs, and poll task status for supported Flux 2 models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to build PoYo Flux 2 generation or editing payloads, submit them to PoYo's API, and track returned task IDs through polling or callbacks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payloads, prompts, image URLs, and callback URLs are sent to PoYo's API. <br>
Mitigation: Review each payload before submission, avoid sensitive prompts or private/internal image URLs, and use callback URLs only for endpoints you control. <br>
Risk: API key exposure can occur if credentials are passed through command arguments or shared logs. <br>
Mitigation: Keep POYO_API_KEY in an environment variable and avoid pasting bearer tokens into prompts, scripts, or logs. <br>


## Reference(s): <br>
- [PoYo Flux 2 API Reference](references/api.md) <br>
- [PoYo Flux 2 Documentation](https://docs.poyo.ai/api-manual/image-series/flux-2) <br>
- [PoYo Flux 2 OpenAPI JSON](https://docs.poyo.ai/api-manual/image-series/flux-2.json) <br>
- [PoYo Task Status Documentation](https://docs.poyo.ai/api-manual/task-management/status) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON payloads and curl or shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include the selected model ID, payload summary, reference-image usage, returned task_id, and next polling or webhook step.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
