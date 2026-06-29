## Description: <br>
Wan 2.7 image generation and editing on PoYo/poyo.ai; prepares payloads for text-to-image and reference-image editing, task submission, polling, and webhook follow-up. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare and submit PoYo Wan 2.7 text-to-image or reference-image editing requests, then guide polling or webhook follow-up using the returned task identifier. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PoYo API keys could be exposed if copied into browser code, public repositories, logs, screenshots, or chat output. <br>
Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager, and redact credentials from outputs and logs. <br>
Risk: Private prompts, source images, or callback URLs may be sent to an external image-generation API. <br>
Mitigation: Submit only data the user is comfortable sharing with PoYo and the callback receiver, and confirm trust boundaries before live calls. <br>
Risk: The skill can submit live asynchronous generation jobs through curl when given a prepared payload. <br>
Mitigation: Make live API calls only after explicit user request in a trusted shell, then preserve the returned task_id for polling or webhook tracking. <br>


## Reference(s): <br>
- [PoYo Wan 2.7 Image API Reference](references/api.md) <br>
- [PoYo Wan 2.7 Image Documentation](https://docs.poyo.ai/api-manual/image-series/wan-2-7-image) <br>
- [PoYo Wan 2.7 Image Model Page](https://poyo.ai/models/wan-2-7-image) <br>
- [ClawHub Skill Page](https://clawhub.ai/coolhackboy/poyo-wan-2-7-image) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON payloads and bash curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include model id, request mode, payload summary, selected size, image count, reference-image use, returned task_id, and next polling or webhook step.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
