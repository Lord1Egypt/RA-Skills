## Description: <br>
Helps agents prepare, submit, and track PoYo Wan 2.6 video generation jobs for text-to-video, image-to-video, video-to-video, and multi_shot workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to construct PoYo Wan 2.6 payloads, choose the correct model variant, submit generation jobs with curl, and preserve task IDs for polling or webhook follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts, media URLs, and optional callback URLs to PoYo when submitting generation jobs. <br>
Mitigation: Review payload contents before submission and only include media URLs and callback URLs intended for PoYo processing. <br>
Risk: API credentials could be exposed if passed directly on a command line or embedded in shared payloads. <br>
Mitigation: Store POYO_API_KEY securely and prefer an environment variable for authentication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/coolhackboy/poyo-wan-2-6) <br>
- [PoYo Wan 2.6 API docs](https://docs.poyo.ai/api-manual/video-series/wan-2-6) <br>
- [PoYo task status docs](https://docs.poyo.ai/api-manual/task-management/status) <br>
- [PoYo Wan 2.6 OpenAPI JSON](https://docs.poyo.ai/api-manual/video-series/wan-2-6.json) <br>
- [PoYo API key dashboard](https://poyo.ai/dashboard/api-key) <br>
- [Local API reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON payload examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include selected model id, final payload or parameter summary, reference-media involvement, returned task_id, and polling or webhook next step.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
