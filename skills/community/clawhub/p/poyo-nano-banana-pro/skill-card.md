## Description: <br>
Poyo Nano Banana Pro helps agents prepare Nano Banana Pro image generation and editing workflows on PoYo, including model selection, payload construction, polling guidance, and output options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and creative teams use this skill to prepare Nano Banana Pro generation or editing requests, choose PoYo model parameters, and submit trusted payloads when a server-side API key is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PoYo API keys, private prompts, source image URLs, and callback URLs can be exposed if included in browser code, public repositories, logs, screenshots, or chat output. <br>
Mitigation: Keep POYO_API_KEY in a server-side environment variable or secret manager, avoid logging sensitive request data, and review payloads before sharing or submitting them. <br>
Risk: Submitting a prepared payload can make a live outbound PoYo API request and start an image generation or editing task. <br>
Mitigation: Run the submit script only from a trusted shell, only after explicit user approval, and report the returned task_id so the task can be tracked by polling or webhook. <br>
Risk: PoYo model fields and supported options may change over time. <br>
Mitigation: Verify current field support in the PoYo documentation before relying on model-specific options such as size, resolution, output_format, or enable_web_search. <br>


## Reference(s): <br>
- [PoYo Nano Banana Pro API Reference](references/api.md) <br>
- [PoYo Nano Banana Pro Documentation](https://docs.poyo.ai/api-manual/image-series/nano-banana-2) <br>
- [PoYo Nano Banana Pro Model Page](https://poyo.ai/models/nano-banana-2-api) <br>
- [PoYo Nano Banana Pro Example Repository](https://github.com/PoyoAPI/nano-banana-pro-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with JSON payload examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a PoYo task_id when a live submission is explicitly requested and succeeds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
