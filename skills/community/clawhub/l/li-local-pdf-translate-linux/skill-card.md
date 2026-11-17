## Description:

This skill helps agents translate text-layer PDFs and related text documents on Ubuntu/Linux by using a local llama.cpp-compatible translation model with configurable language direction and translation depth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[43622283](https://clawhub.ai/user/43622283)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and document-processing users use this skill to translate batches of academic or technical PDFs into Markdown outputs while keeping the model endpoint local by default. It is suited to Linux environments where the user can provide llama-server, a compatible GGUF model, and Python dependencies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document text may leave the local machine if the API URL is changed from the default localhost endpoint to a remote translation service.

Mitigation: Keep the API URL on localhost for private documents unless the user intentionally trusts the remote endpoint.

Risk: The default API key is suitable only for a loopback-only local service and should not protect an exposed endpoint.

Mitigation: Bind llama-server to 127.0.0.1 and use environment variables or restricted configuration files for real API keys.

Risk: The skill depends on user-provided llama.cpp, Python packages, and GGUF model files.

Mitigation: Install dependencies from trusted sources, review planned installation commands before execution, and provide model files deliberately.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/43622283/skills/li-local-pdf-translate-linux)
- [README.md](README.md)
- [SKILL.md](SKILL.md)
- [Default configuration](config/default.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files, terminal text, and optional JSON extraction output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are generated per input file or directory, usually using the target language code in the output filename.]

## Skill Version(s):

1.0.4 (source: server release, SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
