## Description: <br>
Helps agents prepare and submit Seedream 5.0 Lite image generation or editing jobs to PoYo, including model selection, payload fields, curl-based submission, and task tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to build PoYo Seedream 5.0 Lite request payloads, submit them with curl, and track task IDs for image generation or reference-image editing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, and callback URLs are sent to PoYo when the helper is run. <br>
Mitigation: Review the prompt, image URLs, callback URL, and image count before submission, and avoid sending sensitive or private content unless sharing it with PoYo is acceptable. <br>
Risk: The PoYo API key can be exposed if passed directly on the command line or stored in reusable shell history. <br>
Mitigation: Use a revocable POYO_API_KEY environment variable and rotate or revoke the key if it may have been exposed. <br>


## Reference(s): <br>
- [PoYo Seedream 5.0 Lite API Reference](references/api.md) <br>
- [PoYo Seedream 5.0 Lite documentation](https://docs.poyo.ai/api-manual/image-series/seedream-5-0-lite) <br>
- [PoYo task status documentation](https://docs.poyo.ai/api-manual/task-management/status) <br>
- [PoYo Seedream 5.0 Lite OpenAPI JSON](https://docs.poyo.ai/api-manual/image-series/seedream-5-0-lite.json) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown with JSON payloads and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include the selected model id, payload summary, reference-image use, returned task_id, and polling or webhook next step.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
