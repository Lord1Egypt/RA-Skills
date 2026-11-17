## Description:

Complete Open WebUI API integration for managing LLM models, chat completions, Ollama proxy operations, file uploads, knowledge bases (RAG), image generation, audio processing, and pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0x7466](https://clawhub.ai/user/0x7466)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to interact with configured Open WebUI instances for model listing, chat completions, RAG file workflows, knowledge base management, Ollama proxy operations, image generation, audio processing, and pipeline management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote HTTP Open WebUI configurations can expose API tokens and uploaded content.

Mitigation: Use localhost or HTTPS for configured Open WebUI servers and avoid remote HTTP URLs.

Risk: Passing API tokens on the command line can expose credentials on shared systems.

Mitigation: Prefer environment variables for credentials and avoid displaying or logging full tokens.

Risk: RAG uploads can send sensitive files to the configured Open WebUI server.

Mitigation: Review files before upload and confirm intent before sending sensitive content.

Risk: Model deletion and large model pulls can be destructive, costly, or bandwidth intensive.

Mitigation: Require explicit user confirmation before delete operations or large model downloads.

## Reference(s):

- [Open WebUI skill release](https://clawhub.ai/0x7466/skills/open-webui)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API responses and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May issue authenticated API calls to the configured Open WebUI server and may upload user-selected files for RAG workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
