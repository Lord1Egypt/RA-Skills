## Description: <br>
Use PoYo AI's Sora 2 video generation models through the `https://api.poyo.ai/api/generate/submit` endpoint to prepare, submit, and track text-to-video or image-to-video jobs for `sora-2` and `sora-2-private`. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to build PoYo-compatible Sora 2 video generation payloads, submit jobs with a PoYo API key, and report task IDs for follow-up polling or webhook handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill submits prompts and optional image URLs to PoYo's external API. <br>
Mitigation: Use it only when PoYo API use is intended, review request payloads before submission, and avoid sending sensitive prompts or private image URLs unless sharing them with PoYo is acceptable. <br>
Risk: The skill requires a PoYo API key for authenticated requests. <br>
Mitigation: Keep POYO_API_KEY private and prefer supplying it through the environment rather than as a command argument. <br>


## Reference(s): <br>
- [PoYo Sora 2 API Reference](references/api.md) <br>
- [PoYo Sora 2 Documentation](https://docs.poyo.ai/api-manual/video-series/sora-2) <br>
- [PoYo Task Status Documentation](https://docs.poyo.ai/api-manual/task-management/status) <br>
- [ClawHub Skill Page](https://clawhub.ai/coolhackboy/poyo-sora-2) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JSON payload examples and curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include the chosen model, workflow type, request payload or summarized parameters, returned task_id, and next polling or webhook step.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
