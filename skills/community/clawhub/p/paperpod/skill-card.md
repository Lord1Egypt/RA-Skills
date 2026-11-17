## Description:

Isolated agent runtime for code execution, live preview URLs, browser automation, 50+ tools (ffmpeg, sqlite, pandoc, imagemagick), LLM inference, and persistent memory — all via CLI or HTTP, no SDK or API keys required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shassingh09](https://clawhub.ai/user/shassingh09)

### License/Terms of Use:


## Use Case:

Developers and agents use PaperPod to run code, automate browsers, expose live preview URLs, manage files and processes, invoke AI endpoints, and persist small amounts of runtime state through CLI or HTTP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to install and update a global PaperPod CLI and send work to a hosted service.

Mitigation: Install only when the publisher is trusted and prefer a pinned CLI version or reviewed installation path.

Risk: PaperPod tokens, credentials, and private data could be exposed through command execution, environment variables, or persistent memory.

Mitigation: Treat PaperPod tokens as secrets and avoid storing credentials or sensitive private data in persistent memory.

Risk: Background processes and public preview URLs can expose non-public services or data.

Mitigation: Expose only non-sensitive services and clean up background processes and memory when work is complete.

## Reference(s):

- [PaperPod Homepage](https://paperpod.dev)
- [PaperPod Documentation](https://paperpod.dev/docs)
- [PaperPod API Reference](artifact/references/api-reference.md)
- [Shell Tools Reference](artifact/references/shell-tools.md)
- [ClawHub PaperPod Skill](https://clawhub.ai/shassingh09/skills/paperpod)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with CLI commands, HTTP examples, and JSON request snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include credential handling, command execution, file operations, browser automation, public URL exposure, AI calls, and persistent memory instructions.]

## Skill Version(s):

2.0.3 (source: server release and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
