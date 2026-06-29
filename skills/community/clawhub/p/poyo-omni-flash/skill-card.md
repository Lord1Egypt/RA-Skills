## Description: <br>
Helps agents prepare PoYo Omni Flash video-generation requests for text-to-video, image-to-video, three-image reference fusion, and video-input workflows, with polling or webhook follow-up. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare Omni Flash video-generation payloads, optional curl submissions, and follow-up polling or webhook guidance for PoYo jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PoYo API keys could be exposed if placed in browser code, logs, screenshots, repositories, or chat output. <br>
Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager, and avoid echoing or logging it. <br>
Risk: Prompts, source media URLs, and callback URLs are sent to a third-party PoYo API when a job is submitted. <br>
Mitigation: Submit only content approved for third-party processing, and avoid confidential or regulated inputs unless the user has explicitly accepted that processing. <br>
Risk: The submit script can make a live external API request with the provided payload. <br>
Mitigation: Use the script only after reviewing the payload JSON and only when the user explicitly wants a live submission from a trusted shell. <br>


## Reference(s): <br>
- [PoYo Omni Flash API Reference](references/api.md) <br>
- [PoYo Omni Flash documentation](https://docs.poyo.ai/api-manual/video-series/omni-flash) <br>
- [PoYo Omni Flash model page](https://poyo.ai/models/omni-flash) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown with JSON payloads and bash or curl code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes selected model parameters, source media usage, returned task IDs when submitted, and next-step polling or webhook guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
