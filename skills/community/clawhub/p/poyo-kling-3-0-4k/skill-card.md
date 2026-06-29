## Description: <br>
Helps agents prepare, submit, and follow up on PoYo Kling 3.0 4K video generation jobs for text-to-video, image-to-video, multi-shot, audio-enabled, and webhook-based workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to construct PoYo Kling 3.0 4K video generation payloads, submit trusted asynchronous jobs with curl, and guide polling or webhook follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: POYO_API_KEY could be exposed if copied into browser code, public repositories, logs, screenshots, or chat output. <br>
Mitigation: Keep POYO_API_KEY private in a server-side environment variable or backend secret manager. <br>
Risk: Private prompts, source images, videos, or callback URLs may be sent to PoYo or a webhook receiver. <br>
Mitigation: Submit private inputs only when the user trusts PoYo and the callback receiver. <br>
Risk: The helper can submit live video generation jobs through curl when a prepared payload and API key are present. <br>
Mitigation: Review payloads before submission and make live API calls only from a trusted shell. <br>


## Reference(s): <br>
- [PoYo Kling 3.0 4K API Reference](references/api.md) <br>
- [PoYo Kling 3.0 4K Documentation](https://docs.poyo.ai/api-manual/video-series/kling-3-0-4k) <br>
- [PoYo Kling 3.0 4K Model Page](https://poyo.ai/models/kling-3-0-4k) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON payloads and curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include PoYo task IDs after live submission; live calls require POYO_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
