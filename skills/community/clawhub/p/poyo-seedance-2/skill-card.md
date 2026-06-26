## Description: <br>
Seedance 2 helps agents prepare and submit PoYo video generation requests for text-to-video, first/last-frame, and multimodal reference workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and creators use this skill to generate 4 to 15 second PoYo Seedance 2 videos from prompts, first/last-frame image controls, or multimodal references, with optional audio and seed control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PoYo receives submitted prompts, media URLs, callback URLs, and generated task data. <br>
Mitigation: Use the skill only when PoYo is an acceptable processor for that data, avoid sensitive or internal-only media URLs, and use callback URLs you control. <br>
Risk: The skill requires a PoYo API key. <br>
Mitigation: Provide POYO_API_KEY through an environment variable or secret manager and avoid placing credentials in prompts, payload files, or shell history. <br>


## Reference(s): <br>
- [PoYo Seedance 2 API Reference](artifact/references/api.md) <br>
- [PoYo Seedance 2 Documentation](https://docs.poyo.ai/api-manual/video-series/seedance-2) <br>
- [PoYo Task Status Documentation](https://docs.poyo.ai/api-manual/task-management/status) <br>
- [PoYo Seedance 2 Model Page](https://poyo.ai/models/seedance-2) <br>
- [PoYo Seedance 2 OpenAPI JSON](https://docs.poyo.ai/api-manual/video-series/seedance-2.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JSON payloads and curl-compatible shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a returned task_id and a next step to poll status or wait for a webhook when a request is submitted.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
