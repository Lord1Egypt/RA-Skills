## Description: <br>
Kling 3.0 video generation on PoYo / poyo.ai via https://api.poyo.ai/api/generate/submit for standard or pro text-to-video, image-to-video, multi-shot, reference-element, polling, and webhook workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare PoYo Kling 3.0 video-generation payloads, submit trusted payload files with curl, and track follow-up polling or webhook handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PoYo receives generation prompts, reference image URLs, callback URLs, and submitted requests. <br>
Mitigation: Use the skill only when the user intends to use PoYo Kling 3.0, and avoid private or proprietary inputs unless the user trusts PoYo and any webhook receiver. <br>
Risk: The PoYo API key is required for live submission. <br>
Mitigation: Keep POYO_API_KEY server-side in an environment variable or secret manager, and do not expose it in browser code, logs, screenshots, repositories, command-line arguments, or chat output. <br>
Risk: The helper can make live network requests to the PoYo generation API. <br>
Mitigation: Submit only trusted payload files from a safe shell environment after the user explicitly asks for a live API call. <br>


## Reference(s): <br>
- [PoYo Kling 3.0 API Reference](references/api.md) <br>
- [PoYo Kling 3.0 documentation](https://docs.poyo.ai/api-manual/video-series/kling-3-0) <br>
- [PoYo Kling 3.0 model page](https://poyo.ai/models/kling-3-0) <br>
- [ClawHub skill page](https://clawhub.ai/coolhackboy/kling-3) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON payload examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include model id, request mode, payload summary, reference-image or element usage, returned task_id, and polling or webhook next steps.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
