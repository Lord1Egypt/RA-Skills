## Description:

MOSS multi-speaker transcription skill that accepts audio by URL, local file, or Base64/data URL and produces timestamped, speaker-attributed transcription outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[helloeveryworlds](https://clawhub.ai/user/helloeveryworlds)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to transcribe meetings, interviews, and multi-speaker conversations through the MOSS/MOSI transcription service and organize the result by segment and speaker.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected audio, audio URLs, or Base64 audio data are sent to the MOSS/MOSI remote transcription service.

Mitigation: Use only with recordings you are authorized to submit, and review the provider's privacy and retention terms before sending confidential, regulated, or third-party audio.

Risk: Returned transcripts and speaker summaries may contain sensitive conversation content saved as local output files.

Mitigation: Store generated transcript files in an approved location, restrict access as needed, and delete outputs when they are no longer required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/helloeveryworlds/skills/moss-transcribe-diarize)
- [MOSS/MOSI transcription API endpoint](https://studio.mosi.cn/v1/audio/transcriptions)

## Skill Output:

**Output Type(s):** [text, json, files, shell commands, configuration]

**Output Format:** [JSON transcript files, JSON or text segment files, by-speaker text summaries, and JSON command status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and one of MOSS_API_KEY, MOSI_TTS_API_KEY, or MOSI_API_KEY; sends selected audio input to the MOSS/MOSI transcription API.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
