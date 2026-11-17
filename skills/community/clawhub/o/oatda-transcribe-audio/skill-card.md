## Description:

Transcribes audio to text through OATDA's unified audio API for speech-to-text, meetings, podcasts, voice notes, subtitles, timestamps, and Whisper-style transcription.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devcsde](https://clawhub.ai/user/devcsde)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to transcribe user-selected audio files through OATDA and return transcript text, subtitles, timestamps, or segment details when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected audio files and their contents are sent to OATDA for transcription.

Mitigation: Use only when the user's OATDA account, consent requirements, and data-handling expectations are appropriate; avoid highly sensitive recordings unless those requirements are satisfied.

Risk: The skill uses an OATDA API key for authenticated requests.

Mitigation: Keep the key in OATDA_API_KEY or the local credentials file and do not print the full key in responses or logs.

Risk: Large or unsupported audio files can fail transcription requests.

Mitigation: Keep files under the documented 25MB limit, prefer multipart upload for local files, and query available audio models when model IDs fail.

## Reference(s):

- [OATDA](https://oatda.com)
- [OATDA audio models endpoint](https://oatda.com/api/v1/llm/models?type=audio)
- [OATDA transcription endpoint](https://oatda.com/api/v1/llm/transcriptions)
- [ClawHub skill page](https://clawhub.ai/devcsde/skills/oatda-transcribe-audio)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON response excerpts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OATDA_API_KEY; uploads selected audio files to OATDA; maximum audio file size is 25MB.]

## Skill Version(s):

1.1.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
