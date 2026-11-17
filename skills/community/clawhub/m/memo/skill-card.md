## Description:

Transcribe and organize voice memos with automatic categorization and information extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scikkk](https://clawhub.ai/user/scikkk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn voice notes or spoken memos into organized text, structured memo data, summaries, categories, and action items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Voice memo audio is sent to the SenseAudio third-party API for transcription.

Mitigation: Use the skill only for recordings you are comfortable uploading, and check SenseAudio data handling terms before processing confidential, regulated, or highly personal audio.

Risk: The SenseAudio API key is required for use and could be exposed if handled directly in prompts or files.

Mitigation: Store the key in the SENSEAUDIO_API_KEY environment variable and avoid embedding it in shared code, transcripts, or logs.

Risk: A mistaken file path could upload unintended local audio.

Mitigation: Confirm each audio file path before sending it to the transcription API.

## Reference(s):

- [SenseAudio Platform](https://senseaudio.cn)
- [SenseAudio API Key](https://senseaudio.cn/platform/api-key)
- [SenseAudio ASR API](https://senseaudio.cn/docs/speech_recognition/http_api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell code blocks plus structured JSON memo examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cleaned transcription text, structured memo JSON, extracted dates, tasks, contacts, category classification, summaries, and Markdown exports.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
