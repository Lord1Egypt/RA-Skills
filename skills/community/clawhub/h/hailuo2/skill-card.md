## Description: <br>
Helps agents build, submit, and track PoYo Hailuo 02 video-generation jobs, including prompt-optimized and image-to-video workflows for `hailuo-02` and `hailuo-02-pro`. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to prepare PoYo Hailuo 02 request payloads, submit authenticated video-generation jobs, and preserve the returned task ID for polling or webhook follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided prompts, callback URLs, and image URLs are sent to PoYo during job submission. <br>
Mitigation: Review each payload before submission and avoid including secrets, private data, or private/internal URLs. <br>
Risk: POYO_API_KEY can submit jobs on the configured PoYo account. <br>
Mitigation: Store the API key securely, restrict access to trusted users and environments, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [PoYo Hailuo 02 API Reference](references/api.md) <br>
- [PoYo Hailuo 02 Source Docs](https://docs.poyo.ai/api-manual/video-series/hailuo-02) <br>
- [PoYo Unified Task Status Docs](https://docs.poyo.ai/api-manual/task-management/status) <br>
- [PoYo Hailuo 02 OpenAPI JSON](https://docs.poyo.ai/api-manual/video-series/hailuo-02.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON payload examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include selected model ID, request payload or parameter summary, reference-image notes, returned task_id, and polling or webhook next steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
