## Description: <br>
Poyo Image Translator helps agents prepare and submit PoYo image translation tasks, including request payloads, curl commands, async status checks, and webhook guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when a workflow needs PoYo's Image Translator API to translate text inside images and manage the resulting async task lifecycle. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PoYo API keys and authorization headers could be exposed if copied into client code, logs, screenshots, public repositories, or chat output. <br>
Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager and redact credentials from examples and logs. <br>
Risk: Private image URLs, translated outputs, callback URLs, and task ids may disclose sensitive workflow data. <br>
Mitigation: Use public or approved image URLs for submission and avoid logging or sharing task artifacts unless product policy permits it. <br>
Risk: Live submissions can send image data to PoYo before the user intends to execute the workflow. <br>
Mitigation: Make live API calls only after the user explicitly confirms the payload and a safe server-side environment is available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-image-translator) <br>
- [PoYo Image Translator model page](https://poyo.ai/models/image-translator) <br>
- [PoYo API key dashboard](https://poyo.ai/dashboard/api-key) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON payload examples and bash curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include PoYo model id, image URL summary, source and target language choices, request payload, returned task_id, and status or webhook next steps.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
