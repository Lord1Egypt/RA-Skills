## Description:

LH Edge TTS converts text into speech audio with Microsoft Edge neural voices via Python edge-tts, including voice, language, speed, pitch, and subtitle options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuhedev](https://clawhub.ai/user/liuhedev)

### License/Terms of Use:

MIT

## Use Case:

Developers, agents, and end users use this skill to turn requested text or file content into spoken audio for accessibility, multitasking, previews, and customized voice output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text submitted for conversion is sent to Microsoft Edge's online TTS service.

Mitigation: Do not convert secrets, credentials, private documents, regulated data, or other sensitive content unless that external processing is acceptable.

Risk: The install path uses edge-tts without an exact pinned version.

Mitigation: Install in a virtual environment and review or pin the edge-tts dependency before production use.

Risk: Generated audio and subtitle files may be written to local or temporary paths.

Mitigation: Choose output paths deliberately and clean temporary outputs when converted content should not remain on disk.

## Reference(s):

- [ClawHub LH Edge TTS page](https://clawhub.ai/liuhedev/skills/lh-edge-tts)
- [Voice testing reference](https://tts.travisvn.com/)

## Skill Output:

**Output Type(s):** [files, shell commands, configuration, guidance]

**Output Format:** [MP3 audio files, optional VTT/SRT subtitle files, and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires internet access to Microsoft Edge's online TTS service; default audio output is a unique temporary MP3 unless an output path is supplied.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill-info.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
