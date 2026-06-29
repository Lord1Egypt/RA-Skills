## Description: <br>
Kling 2.5 Turbo Pro video generation on PoYo, helping agents prepare text-to-video and frame-guided payloads, submit async tasks, and plan polling or webhook follow-up. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill to generate PoYo Kling 2.5 Turbo Pro video payloads, submit trusted jobs, and decide whether to poll status or wait for a webhook. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PoYo API keys may be exposed if copied into client code, public repositories, logs, screenshots, or chat output. <br>
Mitigation: Keep POYO_API_KEY server-side in an environment variable or secret manager and avoid echoing it in generated commands or responses. <br>
Risk: Prompts, source image URLs, callback URLs, or generated media may contain confidential information sent to PoYo or a webhook receiver. <br>
Mitigation: Review payloads before submission and avoid sending confidential prompts, private image URLs, callback URLs, or media unless the user trusts PoYo and the receiving webhook. <br>
Risk: The skill can submit live asynchronous video-generation jobs when used with a prepared payload and POYO_API_KEY. <br>
Mitigation: Submit only from a trusted shell after explicit user intent, then save the returned task_id and use polling or webhook handling for follow-up. <br>


## Reference(s): <br>
- [PoYo Kling 2.5 Turbo Pro API Reference](references/api.md) <br>
- [PoYo Kling 2.5 Turbo Pro documentation](https://docs.poyo.ai/api-manual/video-series/kling-2-5-turbo-pro) <br>
- [PoYo Kling 2.5 Turbo Pro model page](https://poyo.ai/models/kling-2-5-turbo-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON payloads and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include PoYo request payload summaries, curl examples, task IDs when a submission is made, and polling or webhook next steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
