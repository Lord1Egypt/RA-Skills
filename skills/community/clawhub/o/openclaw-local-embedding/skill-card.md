## Description: <br>
Initializes and configures OpenClaw local embedding mode on CPU-only machines, including proxy-aware model download, llama.cpp setup, memory-search configuration, and gateway restart. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegodamn](https://clawhub.ai/user/leegodamn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to enable OpenClaw memory search with local CPU embeddings on Linux machines where outbound internet access may require an HTTP CONNECT proxy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow may disable Node.js TLS certificate verification during model download when a proxy performs TLS inspection. <br>
Mitigation: Prefer a trusted proxy CA when possible, keep TLS verification changes process-scoped, and never persist NODE_TLS_REJECT_UNAUTHORIZED=0 in shell profiles or system-wide configuration. <br>
Risk: The setup flow can save a working proxy URL for later runs, which may expose sensitive proxy details if the URL includes credentials. <br>
Mitigation: Inspect the saved .proxy file after setup, remove credentials from proxy URLs, and delete the file when the proxy should not be reused. <br>
Risk: The model download depends on remote content and weakened HTTPS protections can reduce assurance that the downloaded GGUF file is authentic. <br>
Mitigation: Independently verify the downloaded model when possible and install this skill only when local OpenClaw embeddings are needed on a proxy-restricted machine. <br>


## Reference(s): <br>
- [Openclaw Local Embedding on ClawHub](https://clawhub.ai/leegodamn/openclaw-local-embedding) <br>
- [Hugging Face](https://huggingface.co) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides a single setup workflow for local embedding download, OpenClaw configuration, gateway restart, and verification.] <br>

## Skill Version(s): <br>
1.0.4 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
