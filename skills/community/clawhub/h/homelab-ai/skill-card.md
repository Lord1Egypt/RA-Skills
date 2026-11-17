## Description:

Homelab Ai helps agents and users set up a local home lab AI cluster across macOS, Linux, and Windows machines for LLM inference, image generation, speech-to-text, and embeddings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and home lab operators use this skill to configure spare local machines as a private AI router for chat, image generation, transcription, and embeddings. It provides setup commands, API examples, dashboard guidance, and operational guardrails for a local network deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup uses package installation commands and references optional tools without pinned versions.

Mitigation: Use a virtual environment or non-admin account, verify package names and versions before installation, and install only from trusted package indexes.

Risk: The skill describes running a local AI router on a home network.

Mitigation: Expose endpoints only on trusted networks, review firewall and bind-address settings, and avoid sending sensitive files or audio until the services and network exposure are trusted.

Risk: Large local model downloads can consume substantial disk space and bandwidth.

Mitigation: Require explicit confirmation for model pulls and deletion, and check model size and available storage before downloading.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/skills/homelab-ai)
- [Ollama Herd Repository](https://github.com/geeks-accelerator/ollama-herd)
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md)
- [Image Generation Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/image-generation.md)
- [Configuration Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/configuration-reference.md)
- [Troubleshooting](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with bash, Python, and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local endpoint examples, dashboard paths, model recommendations, and home lab guardrails.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
