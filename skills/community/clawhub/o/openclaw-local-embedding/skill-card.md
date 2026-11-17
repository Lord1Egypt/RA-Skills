## Description:

Initialize and configure OpenClaw local embedding mode on CPU-only machines, including network probing, proxy fallback, GGUF model download, cmake/llama.cpp setup, OpenClaw configuration, and gateway restart.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leegodamn](https://clawhub.ai/user/leegodamn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to enable OpenClaw memory search with a local CPU embedding model, especially on Linux machines where outbound internet access requires an HTTP CONNECT proxy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The model download path may weaken transport security when TLS verification is disabled for proxied downloads.

Mitigation: Use a trusted CA configuration or manually transfer a verified model when possible; if TLS verification must be disabled, keep it limited to the download process and do not persist it.

Risk: Proxy information may be recorded for later reuse.

Mitigation: Avoid authenticated proxy URLs unless the file location and permissions are protected, and review recorded proxy values before reuse.

Risk: OpenClaw configuration and gateway restart commands can change a running local service.

Mitigation: Confirm the generated configuration, run OpenClaw config validation, and review restart commands before executing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leegodamn/skills/openclaw-local-embedding)
- [Embedding GGUF model repository](https://huggingface.co/ggml-org/embeddinggemma-300m-qat-q8_0-GGUF)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local model setup guidance, OpenClaw configuration steps, gateway restart instructions, and troubleshooting notes.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
