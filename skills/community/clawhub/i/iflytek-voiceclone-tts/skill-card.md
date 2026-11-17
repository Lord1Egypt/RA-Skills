## Description:

Use when user asks to clone a voice, train a custom voice model, or synthesize speech with a cloned voice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iflytek.skills](https://clawhub.ai/user/iflytek.skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to guide iFlytek voice cloning workflows: preparing credentials, training a voice model from consented recordings, checking training status, and synthesizing speech from a trained voice resource.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends voice recordings, synthesis text, and iFlytek API credentials through the implementation.

Mitigation: Use only recordings from speakers who explicitly consent, avoid confidential text, and install only when the publisher and destination service are trusted.

Risk: Security evidence reports unsafe network protections for a workflow that handles voice data, text, and credentials.

Mitigation: Run only on trusted networks and prefer a fixed version that uses HTTPS for training and normal TLS certificate validation for synthesis.

## Reference(s):

- [iFlytek Voice Clone service page](https://www.xfyun.cn/services/voice_clone)
- [iFlytek Voice Clone API documentation](https://www.xfyun.cn/doc/spark/voiceclone.html)
- [iFlytek console](https://console.xfyun.cn)
- [ClawHub skill page](https://clawhub.ai/iflytek.skills/skills/iflytek-voiceclone-tts)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to use local audio files, text input, iFlytek credentials, and a trained voice resource ID.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
