## Description:

Records microphone audio and sends the resulting file to Feishu, covering both voice and background sound.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tazio7](https://clawhub.ai/user/tazio7)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to capture local microphone audio on macOS, denoise it, place the processed WAV file in the workspace, and send it to Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Microphone recordings may capture private background speech or other sensitive audio.

Mitigation: Use only with consent from affected people, keep recording duration minimal, and review or delete recordings when appropriate.

Risk: The local RecordMic.app used for recording is outside the published skill artifact.

Mitigation: Verify the local Automator app and its FFmpeg command before relying on the skill.

Risk: Processed audio is sent to Feishu and may be exposed to unintended recipients or channels.

Mitigation: Confirm the intended Feishu destination and send only workspace-copied files that are appropriate to share.

## Reference(s):

- [Mic Recorder ClawHub Skill Page](https://clawhub.ai/tazio7/skills/mic-recorder)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance centers on local WAV recordings, denoising with FFmpeg, workspace file placement, and Feishu delivery.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
