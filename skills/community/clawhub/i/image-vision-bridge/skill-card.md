## Description:

Image Vision is a local image-understanding bridge that uses an Ollama vision model to turn image files into text descriptions for text-only reasoning agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duchenyu](https://clawhub.ai/user/duchenyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill when a text-only reasoning agent needs to understand screenshots, UI mockups, scanned text, code screenshots, charts, or other local images. The skill reads an image file, sends it to a local Ollama vision model, and returns a text description that the agent can reason over.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup documentation includes a command that pipes a remote Ollama installer directly into a shell.

Mitigation: Review installation steps before use and prefer an official package manager or signed Ollama download.

Risk: Images are read from disk and sent to a local Ollama service for analysis.

Mitigation: Only analyze images that are appropriate to send to the local service configured on the machine.

Risk: The optional clipboard helper can save clipboard images locally under the user's home directory.

Mitigation: Use the helper only for intended clipboard images, consider disabling clipboard copy with the provided option, and delete saved captures when no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duchenyu/skills/image-vision-bridge)
- [Publisher profile](https://clawhub.ai/user/duchenyu)
- [Ollama](https://ollama.com)
- [Qwen3.5 Ollama model](https://ollama.com/library/qwen3.5)
- [Python](https://python.org)
- [DeepSeek](https://deepseek.com)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Plain text image descriptions, with Markdown and inline shell commands for setup or troubleshooting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local Ollama service and a local vision model such as qwen3.5:4b; optional clipboard capture can save images under the user's home directory.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
