## Description: <br>
Seedream 4.5 image generation and editing on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `seedream-4.5`, `seedream-4.5-edit`, 2K/4K output, multi-reference editing, and higher image counts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare and submit Seedream 4.5 image generation or image-editing requests through the PoYo API, including 2K/4K output, supported aspect ratios, multi-reference image inputs, and follow-up task polling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, reference image URLs, and request parameters are sent to PoYo using the user's API key. <br>
Mitigation: Review payloads before submission and avoid sending sensitive personal, confidential, or unapproved images or prompts. <br>
Risk: The skill requires a PoYo API key for authenticated requests. <br>
Mitigation: Store POYO_API_KEY securely, avoid committing it to files or chat transcripts, and pass it only through the environment or an approved secret store. <br>


## Reference(s): <br>
- [PoYo Seedream 4.5 API Reference](references/api.md) <br>
- [PoYo Seedream 4.5 Documentation](https://docs.poyo.ai/api-manual/image-series/seedream-4-5) <br>
- [PoYo Seedream 4.5 OpenAPI JSON](https://docs.poyo.ai/api-manual/image-series/seedream-4-5.json) <br>
- [PoYo Task Status Documentation](https://docs.poyo.ai/api-manual/task-management/status) <br>
- [ClawHub Skill Page](https://clawhub.ai/coolhackboy/poyo-seedream-4-5) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with JSON payloads and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include the selected model id, request payload or parameter summary, reference-image status, returned task_id, and polling or webhook next step.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
