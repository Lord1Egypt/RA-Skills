## Description:

iFlytek Voice Clone TTS trains a custom voice model from audio samples and synthesizes speech with the cloned voice through get-text, task creation, audio upload, training submission, status polling, and synthesis commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qingzhe2020](https://clawhub.ai/user/qingzhe2020)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to operate the iFlytek Voice Clone workflow from an agent: prepare training text, submit authorized voice samples, monitor training, and synthesize audio from the resulting voice resource.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs voice cloning and can process sensitive voice recordings and synthesis text.

Mitigation: Use only voices that the operator has explicit permission to clone, avoid sensitive recordings or private synthesis text, and review intended use before training or synthesis.

Risk: Training audio, metadata, API credentials, and text are sent to iFlytek services.

Mitigation: Treat iFlytek as a third-party processor and confirm data handling, retention, consent, and compliance requirements before use.

Risk: The security evidence says the implementation uses insecure training/auth network paths and disables normal TLS certificate validation for synthesis.

Mitigation: Fix the implementation to use authenticated HTTPS for training/auth and normal TLS certificate validation before use on untrusted networks or with valuable accounts.

## Reference(s):

- [iFlytek Voice Clone API documentation](https://www.xfyun.cn/doc/spark/voiceclone.html)
- [iFlytek developer console](https://console.xfyun.cn)
- [One Sentence Voice Clone service console](https://console.xfyun.cn/services/oneSentenceV2)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and Python CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces command guidance and may create audio files when the generated commands are run with valid iFlytek credentials and authorized voice samples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
