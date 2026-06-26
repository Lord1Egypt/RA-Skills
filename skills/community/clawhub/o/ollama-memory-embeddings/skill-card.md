## Description: <br>
Configure OpenClaw memory search to use Ollama as the embeddings server (OpenAI-compatible /v1/embeddings) instead of the built-in node-llama-cpp local GGUF loading, with interactive model selection and optional import of an existing local embedding GGUF into Ollama. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vidarbrekke](https://clawhub.ai/user/vidarbrekke) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to route memory-search embedding generation through a local Ollama embeddings endpoint, choose an embedding model, verify the endpoint, and keep the OpenClaw memorySearch config aligned. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill changes local OpenClaw memorySearch configuration, so an incorrect config path, base URL, or model can disrupt memory search. <br>
Mitigation: Review the target config path and model choice before install, use audit or dry-run modes where appropriate, and rely on the documented backup and uninstall paths if a revert is needed. <br>
Risk: Changing embedding models can make existing memory vectors incompatible with the new vector space. <br>
Mitigation: Use the documented reindex option after model changes, including auto reindexing when the embedding fingerprint changes. <br>
Risk: The optional watchdog creates ongoing drift-healing persistence on macOS. <br>
Mitigation: Enable the watchdog only when persistent config enforcement is desired, and remove it with the documented uninstall command. <br>
Risk: Passing a real secret as --api-key-value is unnecessary for local Ollama and can expose sensitive material in local configuration. <br>
Mitigation: Use the default local placeholder value unless there is a documented reason to use another non-secret value. <br>
Risk: Dry-run mode may still interact with Ollama before printing the plan. <br>
Mitigation: Run dry-run only against a trusted local Ollama endpoint and inspect the configured endpoint before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vidarbrekke/ollama-memory-embeddings) <br>
- [README](artifact/README.md) <br>
- [Security and Behavior Notes](artifact/SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify local OpenClaw configuration when installation or enforcement scripts are run; dry-run, audit, backup, and uninstall paths are documented.] <br>

## Skill Version(s): <br>
1.0.4 (source: SKILL.md frontmatter, VERSION.txt, and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
