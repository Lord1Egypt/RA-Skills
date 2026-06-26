## Description: <br>
Transcribes URL, local-file, or Base64 audio with MOSI Studio and produces diarized transcript outputs with timestamps and speaker labels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mkkb473](https://clawhub.ai/user/mkkb473) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to submit meeting, interview, or multi-speaker conversation audio to MOSI Studio and collect diarized transcripts for review or summarization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio recordings or audio URLs are sent to MOSI Studio for transcription. <br>
Mitigation: Submit only recordings or URLs the user is allowed to share with MOSI Studio. <br>
Risk: The MOSI Studio API key can grant access if reused or exposed. <br>
Mitigation: Use a dedicated revocable API key through MOSS_API_KEY, MOSI_TTS_API_KEY, or MOSI_API_KEY. <br>
Risk: Generated transcript files may contain sensitive meeting or interview content. <br>
Mitigation: Choose an output location suitable for sensitive transcript data. <br>


## Reference(s): <br>
- [MOSI Studio](https://studio.mosi.cn) <br>
- [ClawHub skill release](https://clawhub.ai/mkkb473/mosi-transcribe-diarize) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Text] <br>
**Output Format:** [Markdown guidance with shell commands; local JSON and text transcript files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes the raw JSON response, a segment timeline text file, and a speaker-grouped text file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
