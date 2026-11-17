## Description:

Private AI helps agents set up and use local AI services for LLM inference, image generation, speech-to-text, embeddings, offline operation, and fleet monitoring on user-controlled hardware.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure and operate a private local AI fleet for sensitive prompts, documents, audio, images, and embeddings without relying on cloud inference APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing and running an unpinned third-party Python package can create normal supply-chain exposure.

Mitigation: Install ollama-herd only from the expected publisher or source, preferably in an isolated non-admin environment, and review or pin the package version before use.

Risk: A local AI service may expose sensitive prompts, documents, or audio beyond the intended users if local-network access is broader than expected.

Mitigation: Confirm that the local-network exposure of the service matches the intended privacy boundary before sending sensitive data through it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/twinsgeeks/skills/private-ai)
- [Ollama Herd GitHub repository](https://github.com/geeks-accelerator/ollama-herd)
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md)
- [Configuration Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/configuration-reference.md)
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with bash, Python, curl, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs assume local service endpoints and user-controlled model downloads.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
