## Description: <br>
Helps agents prepare PoYo Flux Kontext image generation and editing requests, including model selection, payload construction, submission, polling, and webhook guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to assemble PoYo Flux Kontext text-to-image or single-image editing jobs, submit trusted payloads, and explain follow-up polling or webhook handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PoYo API keys, private prompts, source image URLs, or callback URLs could be exposed if copied into browser code, logs, screenshots, repositories, or chat output. <br>
Mitigation: Keep POYO_API_KEY in server-side environment variables or a secret manager, avoid logging sensitive request data, and redact private values before sharing examples. <br>
Risk: Submitting a payload sends image generation or editing data to PoYo and may process confidential source images or prompts. <br>
Mitigation: Make live API calls only after explicit user approval, inspect the prepared payload first, and use confidential inputs only when the user trusts PoYo and the callback receiver. <br>


## Reference(s): <br>
- [PoYo Flux Kontext API documentation](https://docs.poyo.ai/api-manual/image-series/flux-kontext) <br>
- [PoYo Flux Kontext model page](https://poyo.ai/models/flux-kontext) <br>
- [Bundled API reference](artifact/references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and bash examples when useful] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include model choice, generation or editing mode, payload fields, selected size, output format, task ID, and next-step polling or webhook guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
