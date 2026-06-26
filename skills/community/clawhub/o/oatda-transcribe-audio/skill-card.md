## Description: <br>
Transcribe audio to text through OATDA's unified audio API for meetings, podcasts, voice notes, subtitles, timestamps, and Whisper-style transcription. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devcsde](https://clawhub.ai/user/devcsde) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users who need agent-assisted audio transcription can use this skill to prepare OATDA API calls for local audio files and return transcribed text, subtitles, segments, or word timing data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio selected for transcription is sent to OATDA using an API key. <br>
Mitigation: Use the skill only when OATDA's data handling fits the recording, prefer a dedicated OATDA API key, and avoid highly sensitive audio unless the workflow permits it. <br>
Risk: The skill may read an OATDA API key from the environment or ~/.oatda/credentials.json. <br>
Mitigation: Protect the credentials file, avoid exposing the key in logs or shared terminals, and verify only that a key exists rather than printing it. <br>
Risk: Audio files larger than the supported limit may fail transcription. <br>
Mitigation: Keep audio files under 25MB or split longer recordings before sending them to the transcription endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/devcsde/oatda-transcribe-audio) <br>
- [OATDA](https://oatda.com) <br>
- [OATDA audio models endpoint](https://oatda.com/api/v1/llm/models?type=audio) <br>
- [OATDA transcriptions endpoint](https://oatda.com/api/v1/llm/transcriptions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON response guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include transcription text, subtitles, segments, word timing data, cost fields, and error-handling guidance depending on the requested response format.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
