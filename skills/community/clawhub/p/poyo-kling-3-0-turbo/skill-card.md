## Description: <br>
This skill helps agents prepare, submit, and follow up on Kling 3.0 Turbo video generation jobs on PoYo for text-to-video, first-frame image-to-video, and multi-shot storyboard workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to construct PoYo Kling 3.0 Turbo request payloads, choose between standard and pro model IDs, submit trusted jobs, and plan polling or webhook follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: POYO_API_KEY or private request details could be exposed if copied into client code, logs, screenshots, repositories, or chat output. <br>
Mitigation: Keep POYO_API_KEY in a server-side environment or secret manager, avoid logging private prompts, image URLs, and callback URLs, and do not echo secrets in agent responses. <br>
Risk: The submission script sends payloads to PoYo and may process prompts, image URLs, or callback URLs outside the user's environment. <br>
Mitigation: Run the script only for payloads the user intended to send, after confirming the user is comfortable using PoYo for the involved data. <br>


## Reference(s): <br>
- [PoYo Kling 3.0 Turbo API Reference](references/api.md) <br>
- [PoYo Kling 3.0 Turbo Documentation](https://docs.poyo.ai/api-manual/video-series/kling-3-0-turbo) <br>
- [PoYo Kling 3.0 Turbo Model Page](https://poyo.ai/models/kling-3-0-turbo) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with JSON payloads and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May submit network requests with curl only when the user explicitly asks and POYO_API_KEY is available in a trusted server-side environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
