## Description: <br>
Poyo Nano Banana 2 Lite helps agents prepare Nano Banana 2 Lite text-to-image and lightweight image-editing requests for PoYo, including payloads, curl commands, async task submission, and polling or webhook next steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare and submit PoYo Nano Banana 2 Lite generation and edit jobs, choose the correct model id, protect POYO_API_KEY, and track asynchronous task status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: POYO_API_KEY or authorization headers could be exposed through browser code, logs, screenshots, repositories, or chat output. <br>
Mitigation: Keep credentials in server-side environment variables or a secret manager, and never print raw authorization headers or API keys. <br>
Risk: Live PoYo submissions may create external tasks or consume account resources. <br>
Mitigation: Submit requests only when the user explicitly asks and provides a trusted shell or server-side environment. <br>
Risk: Private prompts, source image URLs, callback URLs, or generated outputs may contain sensitive user data. <br>
Mitigation: Avoid logging or sharing those values unless the user or product policy explicitly allows it. <br>


## Reference(s): <br>
- [PoYo Nano Banana 2 Lite model page](https://poyo.ai/models/nano-banana-2-lite) <br>
- [PoYo API key dashboard](https://poyo.ai/dashboard/api-key) <br>
- [Skill API reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON payloads and bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include model id, request type, source-image usage, task_id, and polling or webhook next step.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
