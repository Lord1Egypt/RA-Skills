## Description:

Mac Mini AI helps agents set up and use Mac Mini systems for local LLMs, image generation, speech-to-text, embeddings, and multi-node request routing on Apple Silicon.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn one or more Mac Mini systems into a local AI service for chat, image generation, speech-to-text, embeddings, monitoring, and OpenAI-compatible tool integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an unpinned PyPI package can expose users to package supply-chain changes after the release was reviewed.

Mitigation: Install in a virtual environment and pin `ollama-herd` to a reviewed version before operational use.

Risk: The local or LAN AI service may process prompts and uploaded files such as audio locally and expose endpoints to nearby systems.

Mitigation: Run the service only on trusted machines and networks, and review local data-handling requirements before submitting sensitive prompts or files.

Risk: The skill writes disclosed fleet-manager logs and configuration under `~/.fleet-manager/`.

Mitigation: Review retention and access controls for `~/.fleet-manager/latency.db` and `~/.fleet-manager/logs/herd.jsonl`.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/skills/mac-mini-ai)
- [Ollama Herd Project](https://github.com/geeks-accelerator/ollama-herd)
- [PyPI: ollama-herd](https://pypi.org/project/ollama-herd/)
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md)
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md)
- [Configuration Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/configuration-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, Python, JSON, and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance targets macOS on Apple Silicon and local or LAN AI service operation.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
