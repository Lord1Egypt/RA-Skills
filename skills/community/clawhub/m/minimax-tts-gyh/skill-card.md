## Description:

Converts text to high-quality speech using MiniMax TTS speech-02 and speech-01 models with the MINIMAX_API_KEY environment variable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skydream9527-ctrl](https://clawhub.ai/user/skydream9527-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate MP3 speech from Chinese, English, or other text through the MiniMax TTS API with selectable model, voice, speed, pitch, volume, emotion, language, and output path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text provided for speech synthesis is sent to the MiniMax API.

Mitigation: Avoid submitting confidential or regulated text unless MiniMax use is approved for that data.

Risk: The script requires MINIMAX_API_KEY and exposes that credential to the local Python process.

Mitigation: Run in an isolated environment, scope the key appropriately, and avoid logging or sharing command environments that contain the key.

Risk: The script downloads generated audio through a vendor-provided URL.

Mitigation: Use network controls appropriate for the environment and avoid running it where a compromised vendor download URL could reach sensitive internal services.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/skydream9527-ctrl/skills/minimax-tts-gyh)
- [MiniMax API Host](https://api.minimaxi.com)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Files, Guidance]

**Output Format:** [Markdown with inline bash commands and MP3 audio file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3, the requests package, and MINIMAX_API_KEY; generated audio is written to the requested local output path.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
