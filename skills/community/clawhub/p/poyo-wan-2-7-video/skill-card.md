## Description: <br>
Helps agents prepare and submit Wan 2.7 video generation and editing jobs on PoYo, including text-to-video, image-to-video, reference-to-video, edit-video, polling, and webhook follow-up. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to choose the correct PoYo Wan 2.7 workflow, prepare request payloads, submit trusted jobs with a server-side API key when requested, and guide follow-up polling or webhook handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PoYo API keys, private prompts, media URLs, or callback URLs could be exposed if used in unsafe environments. <br>
Mitigation: Keep POYO_API_KEY in a server-side environment or secret manager, review payloads before execution, and avoid sharing private inputs unless the user trusts PoYo and any callback receiver. <br>
Risk: The submit script can make live PoYo API calls and create asynchronous video generation jobs. <br>
Mitigation: Run it only from a trusted shell with a reviewed payload and only when the user explicitly wants to submit a job. <br>


## Reference(s): <br>
- [PoYo Wan 2.7 Video API Reference](references/api.md) <br>
- [PoYo Wan 2.7 Video Documentation](https://docs.poyo.ai/api-manual/video-series/wan-2-7-video) <br>
- [PoYo Wan 2.7 Video Model Page](https://poyo.ai/models/wan-2-7-video) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JSON payloads and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a selected model id, workflow type, request payload, concise parameter summary, returned task_id, and next-step polling or webhook guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
