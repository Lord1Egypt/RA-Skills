## Description: <br>
Helps agents prepare and optionally submit PoYo Kling 2.1 image-to-video generation jobs, including Standard and Pro payloads, polling guidance, and webhook follow-up. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to prepare PoYo Kling 2.1 image-to-video requests, select Standard or Pro mode, submit prepared payloads when explicitly requested, and plan polling or webhook follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PoYo API keys, prompts, media URLs, callback URLs, or task identifiers could be exposed if copied into client-side code, logs, screenshots, repositories, or chat output. <br>
Mitigation: Keep POYO_API_KEY in a server-side environment variable or secret manager, review payloads before submission, and avoid logging sensitive request or response fields. <br>
Risk: Prepared payloads may submit private prompts or media to PoYo or to a callback receiver. <br>
Mitigation: Submit only when the user explicitly approves the request and trusts PoYo and any callback endpoint receiving job updates. <br>
Risk: Model-specific options can change or be unsupported for the selected Kling 2.1 mode. <br>
Mitigation: Verify current PoYo documentation before relying on model-specific fields, and do not send Pro-only end-frame fields with the Standard model. <br>


## Reference(s): <br>
- [PoYo Kling 2.1 API Reference](references/api.md) <br>
- [PoYo Kling 2.1 documentation](https://docs.poyo.ai/api-manual/video-series/kling-2-1) <br>
- [PoYo Kling 2.1 model page](https://poyo.ai/models/kling-2-1) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Markdown with JSON payloads and curl or shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a returned task_id only after an explicit API submission.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
