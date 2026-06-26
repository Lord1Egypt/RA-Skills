## Description: <br>
Complete Open WebUI API integration for managing LLM models, chat completions, Ollama proxy operations, file uploads, knowledge bases (RAG), image generation, audio processing, and pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0x7466](https://clawhub.ai/user/0x7466) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to interact with Open WebUI instances through REST APIs for model listing, chat completions, RAG file uploads, knowledge-base management, Ollama proxy operations, image generation, audio processing, and pipeline management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a bearer token to access an Open WebUI instance. <br>
Mitigation: Treat OPENWEBUI_TOKEN as sensitive, avoid exposing it in logs, and prefer HTTPS for remote Open WebUI servers. <br>
Risk: The skill can upload files for RAG and may handle private or sensitive documents. <br>
Mitigation: Review file contents before upload and confirm before sending private files to an Open WebUI instance. <br>
Risk: The skill can pull or delete models through the Ollama proxy, which can consume substantial bandwidth or remove local assets. <br>
Mitigation: Confirm with the user before pulling large models or deleting models. <br>


## Reference(s): <br>
- [Open WebUI skill page](https://clawhub.ai/0x7466/open-webui) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an Open WebUI URL and bearer token supplied through environment variables or explicit CLI parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
