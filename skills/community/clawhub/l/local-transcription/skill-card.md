## Description:

Local Transcription helps agents guide users through local speech-to-text transcription with Qwen ASR routed across an Apple Silicon fleet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to set up and operate local transcription for meetings, voice notes, podcasts, and other audio while keeping audio on their own devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup uses unpinned package installs and starts local services.

Mitigation: Install in an isolated environment, pin package versions where possible, and use the skill only when the package sources are trusted.

Risk: The documented router also exposes LLM, image, and embeddings endpoints beyond transcription.

Mitigation: Keep the service localhost-only or otherwise intentionally scoped, and enable only the endpoints needed for the deployment.

Risk: Transcription inputs may contain sensitive audio.

Mitigation: Keep audio local as described by the skill, avoid external upload paths, and review local logs and configuration paths for sensitive data handling.

## Reference(s):

- [Local Transcription on ClawHub](https://clawhub.ai/twinsgeeks/skills/local-transcription)
- [ollama-herd package](https://pypi.org/project/ollama-herd/)
- [ollama-herd repository](https://github.com/geeks-accelerator/ollama-herd)
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python examples, curl/API examples, and JSON response shapes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may reference local HTTP endpoints and local configuration or log paths.]

## Skill Version(s):

1.0.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
