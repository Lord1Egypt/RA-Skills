## Description:

This skill enables Feishu voice conversations by transcribing voice messages with faster-whisper, passing text to an AI agent, generating speech with Edge TTS, converting audio to OPUS, and sending replies through Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[43622283](https://clawhub.ai/user/43622283)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to add Feishu voice-message input and voice replies to an AI assistant workflow. It is intended for Feishu deployments that can provide least-privilege Feishu application credentials and local audio processing dependencies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Server security evidence marks the release suspicious because unsafe install/runtime code is present.

Mitigation: Review scripts before installing, avoid running installers as root, prefer official dependency and model sources, and deploy first in a test environment.

Risk: The manual fix-debug-leak.sh repair script can modify another OpenClaw extension.

Mitigation: Run fix-debug-leak.sh only when this cross-extension change is intentional, after backing up the target extension and validating the change in a controlled environment.

Risk: Feishu credentials and OpenClaw account configuration can expose sensitive access if stored or read broadly.

Mitigation: Use least-privilege Feishu credentials, prefer environment variables, restrict .env files to mode 600, and audit openclaw.json before multi-account use.

Risk: TTS text and audio paths should be treated as unsafe until the security guidance's interpolation concerns are fixed.

Mitigation: Avoid untrusted TTS text or paths in production, keep temporary audio files scoped and cleaned, and validate patched handling before exposing the workflow to users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/43622283/skills/li-feishu-qq-audio)
- [Feishu Open Platform](https://open.feishu.cn/)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [Hugging Face](https://huggingface.co)
- [Hugging Face mirror used by artifact examples](https://hf-mirror.com/)
- [Microsoft Edge TTS service endpoint noted by artifact](https://speech.platform.bing.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may reference local audio files, Feishu credentials, OpenClaw configuration, and model/dependency setup.]

## Skill Version(s):

0.1.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
