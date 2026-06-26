## Description: <br>
MOSS multi-speaker transcription skill that accepts URL, local file, or Base64 audio input and produces timestamped, speaker-labeled transcription outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[helloeveryworlds](https://clawhub.ai/user/helloeveryworlds) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and content teams use this skill to transcribe meetings, interviews, and multi-speaker conversations through the MOSS transcription service and save structured diarized results for downstream review or summarization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio is sent to the remote MOSS transcription service, so recordings may leave the user's machine. <br>
Mitigation: Use the skill only with recordings the user is authorized to process, avoid confidential or regulated audio unless provider handling is understood, and use a dedicated API key. <br>
Risk: Generated transcription and diarization files may contain sensitive spoken content. <br>
Mitigation: Choose output paths deliberately and review generated JSON, segment, and by-speaker text files before sharing or committing them. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Files, JSON, Text] <br>
**Output Format:** [JSON result files, speaker-segment files in JSON/compact JSON/text, by-speaker text summaries, and a JSON command status message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and one of MOSS_API_KEY, MOSI_TTS_API_KEY, or MOSI_API_KEY; sends audio data to the MOSS remote transcription endpoint.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
